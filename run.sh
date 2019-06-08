#!/bin/bash

case "$1" in
  gateway)
    python3 /home/pi/agent/magic/bin/magic-network "$@" &
    freeradius -X
    ;;
  payment|privacy)
    python3 /home/pi/agent/magic/bin/magic-network "$@"
    ;;
  *)
    # The command is something like bash, not an magic subcommand. Just run it in the right environment.
    "$@"
    ;;
esac

