import configparser
import os
import sys

def get_option(parser_func, section, option, default=None):
    """Gets the configuration value from a section and option.

    Args:
        parser_func (instancemethod): The parser function.
        section (str): The name of the configuration file section.
        option (str): The name of the configuration file option.
        default (:obj:, optional): The default value assigned if the
            section does not exist (default: None).

    Returns:
        obj: The value of the configuration file, or the default value.

    """
    try:
        return parser_func(section, option)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default

def parse_config(config):
    """Gets a dictionary of options by parsing a configuration file.

    Note:
        This function implicitly generates the configuration file if it
        does not already exist.

    Args:
        config (str): The configuration file.

    Returns:
        dict: The dictionary of sections with their options.

    """
    if not os.path.exists(config):
        gen_config()

    try:
        with open(config) as config_file:
            parser = configparser.ConfigParser()
            parser.readfp(config_file)
    except Exception as ex:
        sys.stderr.write(str(ex))
        sys.stderr.write("\nFailed to read config file.\n")
        sys.exit(1)

    (dict_sec, dict_opt) = ({}, {})
    for section in parser.sections():
        for option in parser.options(section):
            dict_opt[option] = get_option(parser.get, section, option, default=None)
        dict_sec[section] = dict_opt
        dict_opt = {}
    return dict_sec
