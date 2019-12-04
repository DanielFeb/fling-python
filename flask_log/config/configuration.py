import json
import logging


class Configuration:
    def __init__(self, config_dict) -> None:
        super().__init__()
        self.config = config_dict

    def get_config_recursively(self, name):
        names = name.split(".")
        current_dict = self.config
        for loop_name in names:
            current_dict = current_dict.get(loop_name)
            if current_dict is None:
                return None
        return current_dict

    def get_not_none_property(self, name):
        result = self.get_config_recursively(name)
        if result is None:
            message = "Property {0} is required!".format(name)
            logging.error(message)
            raise RuntimeError(message)
        return result

    def get_optional_property_with_default(self, name, default):
        result = self.get_config_recursively(name)
        if result is None:
            result = default
        return result

    def has_config(self, name):
        return self.config.get(name) is not None

    def update(self, other):
        self.config = Configuration.merge_data(self.config, other.config)

    @staticmethod
    def merge_data(data_1, data_2):
        """
        使用 data_2 和 data_1 合成一个新的字典。
        对于 data_2 和 data_1 都有的 key，合成规则为 data_2 的数据覆盖 data_1。
        :param data_1:
        :param data_2:
        :return:
        """
        if isinstance(data_1, dict) and isinstance(data_2, dict):
            new_dict = {}
            d2_keys = list(data_2.keys())
            for d1k in data_1.keys():
                if d1k in d2_keys:  # d1,d2都有。去往深层比对
                    d2_keys.remove(d1k)
                    new_dict[d1k] = Configuration.merge_data(data_1.get(d1k), data_2.get(d1k))
                else:
                    new_dict[d1k] = data_1.get(d1k)  # d1有d2没有的key
            for d2k in d2_keys:  # d2有d1没有的key
                new_dict[d2k] = data_2.get(d2k)
            return new_dict
        else:
            return data_2


def get_configuration_from_json(json_str):
    config_dict = json.loads(json_str)
    return Configuration(config_dict=config_dict)


def get_configuration_from_json_file(json_file):
    file = open(json_file, "r")
    json_str = file.read()
    file.close()
    return get_configuration_from_json(json_str)

