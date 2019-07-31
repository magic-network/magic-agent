import os
import hjson
import json


class ConfigLoader(dict):

    def load(self, default_config_path, user_config_path):

        self.clear()
        # Load default/base config.
        try:
            with open(default_config_path) as f:
                conf = hjson.load(f)
                for key, value in conf.items():
                    self[key] = value

        except FileNotFoundError:
            raise Exception(
                'Default config is missing. Expected file to exist: %s' %
                default_config_path)

        # Apply user-specific config file:
        try:
            with open(user_config_path) as f:
                user_config = hjson.load(f)
                for config_group_key in self:
                    config_group_value = self[config_group_key]
                    for config_key in config_group_value:
                        try:
                            user_config_item = user_config[config_group_key][config_key]
                            self[config_group_key][config_key] = self.determine_valid_mapping(
                                user_config_item, self[config_group_key][config_key])
                        except KeyError:
                            pass

        except FileNotFoundError:
            pass

        # Apply environment variables:
        self.parse_env_keys_r(self, [])

    def parse_env_keys_r(self, d, key_str):
        for k in d:
            v = d[k]
            if isinstance(v, dict):
                key_str.append(k.upper())
                self.parse_env_keys_r(v, key_str)
            else:
                try:
                    env_key = '_'.join(str(s) for s in key_str) + "_" + k.upper()
                    env_var_value = self.determine_valid_mapping(os.environ[env_key], v)
                    d[k] = env_var_value
                except KeyError:
                    # don't do anything if an environment variable is not found.
                    pass
        if len(key_str) > 0:
            key_str.pop()

    def determine_valid_mapping(self, value, conversion_class):
        """
        determine what value to map the passed in value, environment variables are always strings
        so we need to map them to the proper data type
        :param value: the value to be converted
        :param conversion_class: value with the type we want to convert to
        :return the value mapped to its proper type
        """
        if isinstance(conversion_class, str):
            return self.map_to_valid_value(str, value, conversion_class).strip()
        if type(conversion_class) is int:
            return self.map_to_valid_value(int, value, conversion_class)
        if type(conversion_class) is float:
            return self.map_to_valid_value(float, value, conversion_class)
        if type(conversion_class) is bool:
            return self.map_to_valid_value(self.to_bool, value, conversion_class)
        if isinstance(conversion_class, list):
            return self.convert_str_to_list(value, conversion_class)
        if isinstance(conversion_class, dict):
            if isinstance(value, str):
                return json.loads(value.strip())
            elif isinstance(value, dict):
                return value
            raise ValueError(
                "Passed in value {0} connot be converted to a dictionary, must be a string or dictionary".format(value))

    def convert_str_to_list(self, value, conversion_class):
        """
        Converts a comma separated value string into a list of strings
        :param value: the string to be converted to a list
        :return a list of the split string
        """
        if isinstance(value, str):
            # remove the brackets if they exist
            if value[0] == '[':
                value = value[1:-1]
            string_vals = value.split(",")
            retval = []
            if len(string_vals) == len(conversion_class):
                for i in range(len(string_vals)):
                    #                     this should dig down into multidimensional lists
                    retval.append(self.determine_valid_mapping(
                        string_vals[i].strip(), conversion_class[i]))
                return retval
            return string_vals
        return value

    def map_to_valid_value(self, type_func, value, default):
        """
        Map the passed in value to one that is valid for the salesforce field
        :param type_func: the function for converting the value, like int(), float() etc...
        :param value: the value to convert to the passed in data type
        :param default: the default value if it is none
        :return: the newly mapped value 
        """
        try:
            return default if (value is None or type_func(value) is None or (not isinstance(default, bool) and not type_func(value))) else type_func(value)
        except TypeError:
            return default

    def to_bool(self, val):
        """
        Converts a value to boolean, handles non empty strings as well
        :param val: value to be converted to a boolean
        :return the boolean value
        """
        if isinstance(val, str):
            return val.lower() in ("yes", "true", "t", "1")
        return bool(val)
