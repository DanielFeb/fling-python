import os

from config.configuration import Configuration, get_configuration_from_yaml_file

config_dir = os.path.abspath(os.path.dirname(__file__))
work_dir = os.path.abspath(os.path.dirname(config_dir))

default_config_prefix = 'application'
default_config_suffix = 'yml'
default_config_file = '{0}.{1}'.format(default_config_prefix, default_config_suffix)


def make_dir_if_not_exist(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)


def add_work_dir_prefix(name):
    return append_path(work_dir, name)


def append_path(path, name):
    return path + os.sep + name


def get_global_configuration():
    default_config = get_configuration_from_yaml_file(add_work_dir_prefix(default_config_file))
    active_profile = default_config.get_config_recursively('profiles.active')
    if active_profile is not None:
        additional_config_file = "{0}-{1}.{2}".format(default_config_prefix, active_profile, default_config_suffix)
        additional_config = get_configuration_from_yaml_file(add_work_dir_prefix(additional_config_file))
        default_config.update(additional_config)
    return default_config


configuration = get_global_configuration()


def log_configuration():
    return Configuration(configuration.get_not_none_property("log"))

