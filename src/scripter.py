from fileinput import FileInput
from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

import os
import re
import sys
import yaml

COMMON = 'src/templates/common'

class Scripter:
    """Provides methods for Cisco script generation.

    Attributes:
        config (dict): The device configuration.
        dest (str): The name of the file where to save the script.
        device (str): The device name.

    """

    def __init__(self, src, dest, device):
        with open(src, 'r') as stream:
            try:
                self.config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        self.path = 'templates/'
        self.dest = dest
        self.mode = 'user'
        self.device = device

    def clean_file(self, dest):
        """Allows to delete the different indentations of lines present
        in a given file.

        Args:
            dest (str): The destination file.

        """
        clean_lines = []
        with open(dest, "r") as f:
            lines = f.readlines()
            clean_lines = []
            for l in lines:
                if 'copy' not in l:
                    clean_lines.append(l.strip())
                else:
                    clean_lines.append(l)

        with open(dest, "w") as f:
            f.writelines('\n'.join(clean_lines))

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

    def create_file(self, dest, config, env):
        """Creates the file containing all the necessary Cisco
        templates.

        Args:
            dest (str): The absolute path to the file to be created.
            config (dict): The configuration file.
            env (Environment): The Jinja2 environnement.

        """
        if len(env.list_templates()) > 0:
            open(dest, 'w').close()
        else:
            print("Error: No sections in YAML file ({})".format(self.src))
            sys.exit(1)

        for section in config:
            self.write_text(dest, self.create_header(section + ' configuration') + '\n!\n')
            self.enter_enable(dest)

            if section != 'special':
                self.enter_conft(dest)

            if section == 'rip':
                template = env.get_template(self.device + '/' + section + '/routing.txt')
                self.write_text(dest, template.render(self.config) + '!\n')

            for key in config[section]:
                if '_' in key:
                    key = key.replace('_', '-')
                if key == 'reset':
                    self.exit_specific(dest)
                    self.exit_conft(dest)

                template = env.get_template(self.device + '/' + section + '/' + key + '.txt')
                if len(template.render(self.config)) > 0:
                    if key != 'save':
                        self.write_text(dest, template.render(self.config) + '!\n')
                    else:
                        self.write_text(dest, template.render(self.config) + '\n')

            if section != 'special':
                if self.mode == 'conft':
                    self.exit_conft(dest)

            if self.mode == 'enable':
                self.exit_enable(dest)

    def enter_enable(self, dest):
        """Adds the enable mode to the specified file and updates the
        current mode.

        Args:
            dest: The destination filename to write.

        """
        self.mode = 'enable'
        self.write(dest, COMMON + '/enable.txt')

    def enter_conft(self, dest):
        """Adds the configuration terminal mode to the specified file
        and updates the current mode.

        Args:
            dest: The destination filename to write.

        """
        self.mode = 'conft'
        self.write(dest, COMMON + '/conft.txt')

    def exit_conft(self, dest):
        """Exits the configuration terminal mode to the specified file
        and updates the current mode.

        Args:
            dest: The destination filename to write.

        """
        self.mode = 'enable'
        self.write(dest, COMMON + '/exit_conft.txt')

    def exit_enable(self, dest):
        """Exits the enable mode to the specified file and updates the
        current mode.

        Args:
            dest: The destination filename to write.

        """
        self.mode = 'user'
        self.write(dest, COMMON + '/exit_enable.txt')

    def exit_specific(self, dest):
        """Exits the specifc mode to the specified file and updates the current
        mode.

        Args:
            dest: The destination filename to write.

        """
        self.mode = 'conft'
        self.write(dest, COMMON + '/exit_spec.txt')

    def run(self, verbose=False):
        """Generates the script for the device according to a config
        file.

        Args:
           verbose (bool, optional): Outputs or not the script to the
           console (default: False).

        """
        env = Environment(
            loader=PackageLoader('src', self.path),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.create_file(self.dest, self.config, env)
        self.clean_file(self.dest)

        if verbose:
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
