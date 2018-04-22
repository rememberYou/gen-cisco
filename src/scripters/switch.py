from src.scripter import *

SWITCH_PATH = "src/templates/switch/"

class Switch(Scripter):

    def get_templates(self, config):
        """Gets the templates that need to be used according dictionary
        with the switch config.

        Args:
            dict: The dictionary with the switch config.

        Returns:
            list: The list of templates to be used.

        """
        tmp = []
        if 'basic' in config:
            tmp.append(SWITCH_PATH + 'basic')
        if 'etherchannel' in config:
            tmp.append(SWITCH_PATH + 'etherchannel')
        if 'spanning-tree' in config:
            tmp.append(SWITCH_PATH + 'spanning-tree')
        if 'password' in config:
            tmp.append('src/templates/common/password')
        tmp.append('src/templates/common/saving')
        return tmp

    def run(self):
        """Generates the Cisco script for the switch according to a
        config file.

        """
        templates = self.get_templates(self.config)
        self.create_file(self.dest, templates)
        for template in templates:
            dict_config = self.create_dict(template, self.config, template.split('/')[-1])
            self.replace_all(self.dest, dict_config)
