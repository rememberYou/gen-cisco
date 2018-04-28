import os
import re
import sys

from fileinput import FileInput
from src.parser import parse_config

BOOL_KEYS = ['auto-summary', 'bpduguard', 'debug', 'disable-dns',
'password-encryption', 'portfast', 'reset', 'routing']
COMMON = 'src/templates/common'

class Scripter:
    """Provides methods for Cisco script generation.

    Attributes:
        config (dict): The device configuration.
        dest (str): The name of the file where to save the script.
        device (str): The device name.

    """

    def __init__(self, config, dest, device):
        self.src = config
        self.config = parse_config(config)
        self.dest = dest
        self.device = device

    def create_dict(self, templates, config):
        """Create a dictionary where keys are words between rafters and
        its values are those present in the config file.

        Args:
            templates (dict): The Cisco templates with their rafter words.
            config (dict): The device configuration.

        Returns:
            dict: The dictionary containing the keys to replace in the
            Cisco template by its values.

        """
        dict_config = {}
        for section in templates:
            for rafter in templates[section].values():
                if rafter is not None:
                    if isinstance(rafter, list):
                        for r in rafter:
                            if '_' in r:
                                tmp = r.replace('_', '-')
                                dict_config[r] = config[section][tmp[1:-1].lower()]
                            else:
                                dict_config[r] = config[section][r[1:-1].lower()]
                    elif '_' in rafter:
                        tmp = rafter.replace('_', '-')
                        dict_config[rafter] = config[section][tmp[1:-1].lower()]
                    else:
                        dict_config[rafter] = config[section][rafter[1:-1].lower()]
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

    def create_file(self, dest, templates):
        """Creates the file containing all the necessary Cisco
        templates.

        Args:
            dest (str): The absolute path to the file to be created.
            templates (list): The list of Cisco templates.

        """
        if len(templates) > 0:
            open(dest, 'w').close()
        else:
            print("Error: No sections in INI file ({})".format(self.src))
            sys.exit(1)

        for section in templates:
            self.write_text(dest, self.create_header(section + ' configuration') + '!\n' * 2)
            self.write(dest, COMMON + '/enable')
            self.write(dest, COMMON + '/configure_terminal')
            for path in templates[section]:
                self.write(dest, path)
            self.write(dest, COMMON + '/exit_conft')
            self.write(dest, COMMON + '/exit_enable')

        self.write(dest, COMMON + '/saving')

    def find_filename(self, path, rafter):
        """Finds a filename according to a word between rafters.

        Args:
            path (str): The path to start the search.
            rafter (str): The word between rafters.

        Returns:
            str: The filename.

        """
        for filename in os.listdir(path):
            filename = path + '/' + filename
            with open(filename, 'r') as template_file:
                if rafter in template_file.read():
                    return filename

    def get_rafter(self, filename):
        """Gets word between rafters from a file.

        Args:
            filename (str): The relative file path to read.

        Returns:
            str: The words from a file between rafters.

        """
        with open(filename,'r') as template_file:
            rafter = re.findall('<.*?>', template_file.read())
            if len(rafter) > 0:
                return rafter[0]

    def get_rafters(self, filename):
        """Gets words from a file between rafters.

        Args:
            filename (str): The relative file path to read.

        Returns:
            list: The list of words in the file between rafters.

        """
        with open(filename,'r') as template_file:
            return re.findall('<.*?>', template_file.read())

    def get_templates(self, device, config):
        """Gets the relative template paths with their words between
        rafters that need to be used, according dictionary with the
        config.

        Args:
            device (str): The device name.
            config (dict): The device configuration.

        Returns:
            dict: The dict that contains the rafted words according to a
            relative template paths to be used.

        """
        templates = {}
        for section in config:
            other = {}
            path = 'src/templates/' + device + '/' + section
            if section in next(os.walk(COMMON))[1]:
                path = COMMON + '/' + section
            for key in config[section]:
                if (os.path.isfile(path + '/' + key)):
                    if key not in BOOL_KEYS and config[section][key] != '':
                        other[path + '/' + key] = self.get_rafter(path + '/' + key)
                    elif key in BOOL_KEYS and config[section][key] == 'true':
                        other[path + '/' + key] = self.get_rafter(path + '/' + key)
                elif (path + '/' + key not in other):
                    if '-' in key:
                        key = key.replace('-', '_')
                    filename = self.find_filename(path, self.word_to_rafter((path + '/' + key).split('/')[-1]))
                    other[filename] = self.get_rafters(filename)
            templates[section] = other
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

    def run(self, verbose=False):
        """Generates the script for the device according to a config
        file.

        Args:
           log (bool, optional): Outputs or not the script to the
           console (default: False).

        """
        templates = self.get_templates(self.device, self.config)
        self.create_file(self.dest, templates)
        dict_config = self.create_dict(templates, self.config)
        self.replace_all(self.dest, dict_config)
        if verbose:
            with open(self.dest, 'r') as output_file:
               print(output_file.read())

    def word_to_rafter(self, word):
        """Transforms a given word into an uppercase word between
        rafter.

        Args:
            word (str): The word to transform.

        Returns:
            str: The uppercase word between rafter.

        """
        return '<{}>'.format(word.upper())

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
