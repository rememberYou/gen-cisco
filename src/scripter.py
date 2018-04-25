import os
import re

from fileinput import FileInput
from src.parser import parse_config

BOOL_KEYS = ['disable-dns', 'password-encryption', 'reset']
COMMON = 'src/templates/common'
SPECIAL_FILES = {'ssh': {'username': 'authentication', 'password': 'authentication'},
                 'eigrp': {'ip': 'routing', 'wild-card': 'routing'},
                 'etherchannel': {'channel-group': 'channel-group', 'channel-mode': 'channel-group'},
                 'ospf': {'ip': 'routing', 'wild-card': 'routing'}
}

class Scripter:
    """Provides methods for Cisco script generation.

    Attributes:
        config (dict): The device configuration.
        dest (str): The name of the file where to save the script.
        device (str): The device name.

    """

    def __init__(self, config, dest, device):
        self.config = parse_config(config)
        self.dest = dest
        self.device = device

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

    def create_header(self, title, delimitor='!', limit=71):
        """Creates a header based on a title, delimiter and line size
        limit.

        Args:
            title (str): The header title.
            delimitor (str): The delimiter symbol.
            limit (int): The maximum font size per line.

        Returns:
            str: The header.

        """
        symbols = round((limit - len(title)) / 2)
        return delimitor * symbols + ' ' + title.upper() + ' ' + delimitor * symbols

    def create_file(self, filename, templates):
        """Creates the file containing all the necessary Cisco
        templates.

        Args:
            filename (str): The absolute path to the file to be created.
            templates (list): The list of Cisco templates.

        """
        with open(filename, "w") as dest_file:
            if len(templates) > 0:
                dest_file.write(self.create_header(templates[0].split('/')[-2] + ' configuration') + '!\n' * 2)

        self.write(filename, COMMON + '/enable')
        self.write(filename, COMMON + '/configure_terminal')

        for i in range(len(templates)):
            section = templates[i].split('/')[-2]
            device_path = 'src/templates/' + self.device + '/' + section
            special_file = False

            if templates[i] == COMMON + '/ssh/username' and templates[i + 1] == COMMON + '/ssh/password':
                special_file = True
                self.write(filename, COMMON + '/ssh/authentication')

            elif templates[i] == device_path + '/ip' and templates[i + 1] == device_path + '/wild-card':
                special_file = True
                self.write(filename, device_path + '/routing')

            elif templates[i] == device_path + '/channel-group' and templates[i + 1] == device_path + '/channel-mode':
                special_file = True
                self.write(filename, device_path + '/channel-group')

            if i >= 1 and templates[i - 1].split('/')[-2] != section:
                self.write(filename, COMMON + '/exit_conft')
                self.write(filename, COMMON + '/exit_enable')
                self.write_text(filename, self.create_header(self.get_section(templates[i]) + ' configuration') + '!\n' * 2)
                self.write(filename, COMMON + '/enable')
                self.write(filename, COMMON + '/configure_terminal')
                self.write(filename, templates[i])

            elif not special_file and 'eigrp/wild-card' not in templates[i] \
                 and 'ospf/wild-card' not in templates[i] \
                 and 'ssh/password' not in templates[i] \
                 and 'etherchannel/channel-mode' not in templates[i]:
                self.write(filename, templates[i])

        self.write(filename, COMMON + '/exit_conft')
        self.write(filename, COMMON + '/exit_enable')
        self.write(filename, COMMON + '/saving')

    def get_key(self, path):
        """Gets the key name according to a relative template paths.

        Args:
            path: The relative template path

        Returns:
            str: The key name.

        """
        return path.split('/')[-1]

    def get_rafters(self, filename):
        """Gets words from a file between rafters.

        Args:
            filename (str): The relative file path to read.

        Returns:
            list: The list of words in the file between rafters.

        """
        section = self.get_section(filename)
        key =  self.get_key(filename)

        if section in SPECIAL_FILES and key in SPECIAL_FILES[section]:
            tmp = 'src/templates/common/' + section
            if os.path.isdir(tmp):
                filename = tmp + '/' +  SPECIAL_FILES[section][key]
            else:
                filename = 'src/templates/' + self.device + '/' +  section + '/' + SPECIAL_FILES[section][key]

        with open(filename,'r') as template_file:
            return re.findall('<.*?>', template_file.read())

    def get_section(self, path):
        """Gets the section name according to a relative template paths.

        Args:
            path: The relative template path

        Returns:
            str: The section name.

        """
        return path.split('/')[-2]

    def get_templates(self, device, config):
        """Gets the relative template paths that need to be used
        according dictionary with the config.

        Args:
            device (str): The device name.
            config (dict): The device configuration.

        Returns:
            list: The list of relative template paths to be used.

        """
        templates = []
        for section in config:
            path = 'src/templates/' + device + '/' + section
            if os.path.isdir(COMMON + '/' + section):
                path = COMMON + '/' + section
            for key in config[section]:
                if key not in BOOL_KEYS and config[section][key] != '':
                    templates.append(path + '/' + key)
                elif key in BOOL_KEYS and config[section][key] == 'true':
                    templates.append(path + '/' + key)
        return templates

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
        """Replaces all occurrences of an old word with a new one in a
        specific file.

        Args:
            filename (str): The filename.
            old (str): The old word.
            new (str): The new word.

        """
        with FileInput(filename, inplace=True) as dest_file:
            for line in dest_file:
                print(line.replace(old, new), end='')

    def run(self, log=False):
        """Generates the script for the device according to a config
        file.

        Args:
           log (bool, optional): Outputs or not the script to the
           console (default: False).

        """
        templates = self.get_templates(self.device, self.config)
        self.create_file(self.dest, templates)
        for template in templates:
            dict_config = self.create_dict(template, self.config,
                                           self.get_section(template))
            self.replace_all(self.dest, dict_config)
        if log:
            with open(self.dest, 'r') as output_file:
               print(output_file.read())

    def write(self, dest, src):
        """Writes the content of a file in a destination file.

        Args:
            dest (str): The destination file.
            text (str): The text file.

        """
        with open(dest, "a") as dest_file:
            with open(src, 'r') as src_file:
                dest_file.write(src_file.read() + '!\n')

    def write_text(self, dest, text):
        """Writes text in a destination file.

        Args:
            dest (str): The destination file.
            text (str): The text file.

        """
        with open(dest, "a") as dest_file:
            dest_file.write(text)
