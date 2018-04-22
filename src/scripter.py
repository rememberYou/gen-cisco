import re

from fileinput import FileInput
from src.parser import parse_config

class Scripter:
    """Provides methods for Cisco script generation.

    Attributes:
        config (dict): Switch configuration.
        dest (str): Name of the file where to save the script.

    """

    def __init__(self, ini_file, dest):
        self.config = parse_config(ini_file)
        self.dest = dest

    def create_dict(self, template, config, section):
        """Create a dictionary where keys are words between rafters and
        its values are those present in the config file.

        Args:
            template (str): The Cisco template.
            config (dict): The device configuration.
            section (str): The section name of an INI file.

        Returns:
            dict: The dictionary containing the keys to replace in the
            Cisco template by its values.

        """
        rafters = self.get_rafters(template)
        dict_config = {}
        for rafter in rafters:
            if '_' in rafter:
                value = rafter.replace('_', '-')
            else:
                value = rafter
            dict_config[rafter] = config[section][value[1:-1].lower()]
        return dict_config

    def create_file(self, filename, templates):
        """ Creates the file containing all the necessary Cisco
        templates.

        Args:
            filename (str): The absolute path to the file to be created.
            templates (list): The list of Cisco templates.

        """
        with open(filename, "w") as dest_file:
            for template in templates:
                with open(template, 'r') as template_file:
                    dest_file.write(template_file.read())

    def get_rafters(self, filename):
        """Gets words from a file between rafters.

        Args:
            filename (str): The absolute path of the file to read.

        Returns:
            list: The list of words in the file between rafters.

        """
        with open(filename,'r') as template_file:
            return re.findall('<.*?>', template_file.read())

    def replace_all(self, filename, dict_config):
        """Replaces the words of a file found as key of a dictionary,
        by their corresponding value.

        Args:
            filename (str): The filename.
            dict_config (dict): The word replacement dictionary.

        """
        for key, value in dict_config.items():
            self.replace_in_file(filename, key, value)

    def replace_in_file(self, filename, old, new):
        """Replaces all occurrences of an old word with a new one.

        Args:
            old (str): The old word.
            new (str): The new word.

        """
        with FileInput(filename, inplace=True) as file:
            for line in file:
                print(line.replace(old, new), end='')
