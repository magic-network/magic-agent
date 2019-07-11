import os
import collections
import hjson


class ConfigLoader(collections.UserDict):

    def __init__(self):
        self.data = {}
        super().__init__()

    def load(self, default_config_path, user_config_path):

        self.data.clear()

        # Load default/base config.
        try:
            with open(default_config_path) as f:
                self.data = hjson.load(f)
        except FileNotFoundError:
            raise Exception(
                'Default config is missing. Expected file to exist: %s' %
                default_config_path)

        # Apply user-specific config file:
        try:
            with open(user_config_path) as f:
                user_config = hjson.load(f)
                for config_group_key in self.data:
                    config_group_value = self.data[config_group_key]
                    for config_key in config_group_value:
                        try:
                            user_config_item = user_config[config_group_key][config_key]
                            self.data[config_group_key][config_key] = self.translate_value(
                                user_config_item)
                        except KeyError:
                            pass

        except FileNotFoundError:
            pass

        # Apply environment variables:
        for config_group_key in self.data:
            config_group_value = self.data[config_group_key]
            for config_key in config_group_value:
                env_var_key = config_group_key.upper() + "_" + config_key.upper()
                try:
                    env_var_value = os.environ[env_var_key]
                    self.data[config_group_key][config_key] = self.translate_value(
                        env_var_value)
                except KeyError:
                    # don't do anything if an environment variable is not
                    # found.
                    pass

    def translate_value(self, value):
        if value == "True":
            return True
        if value == "False":
            return False
        return value
