from magic.gateway.authobject import AuthObject
from magic.utils.eth import verify_sig
import logging
import os
import socket
import threading
import asyncio


class RadiusDaemon(threading.Thread):

    def __init__(self, gateway):
        self.gateway = gateway
        self.logger = logging.getLogger(__name__)
        self.config = gateway.config
        self.shutdown = False
        threading.Thread.__init__(self)

    def read_data_from_conn(self, conn):
        buf = bytes()
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buf += data
            # stop at line break and some protection against something
            # sending us too much data for some reason
            if b'\n' in data or len(buf) > 8192:
                break
        return buf

    def gen_auth_response(self, auth_succeed):
        return b'\x01' if auth_succeed else b'\x00'

    def static_auth(self, auth_object):
        return (auth_object.address == self.config["dev"]['address']
                and auth_object.password == self.config["dev"]['password'])

    def check_identity(self, auth_object):

        # for debugging purposes allow option of using
        # static address and password
        if self.config['dev']['address'] and \
                self.config['dev']['password']:
            return self.static_auth(auth_object)

        address = auth_object.address
        password_tokens = auth_object.password.split("-")

        # Check for all components of password to be present.
        if len(password_tokens) < 2:
            return False

        timestamp = password_tokens[0]
        signature = password_tokens[1]

        # TODO: Add: Check if timestamp is within a window... Will this require
        # the client to remake a profile?
        return verify_sig("auth_" + timestamp, signature, address)

    def run(self):

        self.logger.warning("Magic Radius Service started")

        ipc_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sockpath = self.config['dev']['sockpath']

        try:
            os.unlink(sockpath)
        except FileNotFoundError:
            pass
        ipc_sock.bind(sockpath)
        os.chmod(sockpath, 666)
        ipc_sock.listen(1)

        self.logger.warning("Listening on %s", sockpath)

        while True:
            try:
                conn, address = ipc_sock.accept()
            except KeyboardInterrupt:
                self.logger.warning('Shutting down')
                break

            conn.settimeout(2)
            authbuf = self.read_data_from_conn(conn)
            try:
                ao = AuthObject()
                ao.decode(authbuf)
            except ValueError as e:
                self.logger.warning('Got invalid string via socket')
                continue
            self.logger.info("AO=%s", repr(ao))

            identity_verified = self.check_identity(ao)

            if identity_verified:
                success_future = asyncio.run_coroutine_threadsafe(
                    self.gateway.on_user_auth(ao), self.gateway.loop)
                # TODO: Refactor: This potentially blocks the thread for other
                # users until the result is returned.
                validated = success_future.result()
                conn.send(self.gen_auth_response(validated))
            else:
                conn.send(self.gen_auth_response(False))

            conn.close()

        ipc_sock.close()
