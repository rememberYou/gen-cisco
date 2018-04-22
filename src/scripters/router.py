from src.scripter import *

ROUTER_PATH = "src/templates/router/"

class Router(Scripter):

    def get_templates(self, config):
        """Gets the templates that need to be used according dictionary
        with the router config.

        Args:
            dict: The dictionary with the router config.

        Returns:
            list: The list of templates to be used.

        """
        tmp = []
        if 'basic' in config:
            tmp.append(ROUTER_PATH + 'basic')
        if 'eigrp' in config:
            tmp.append(ROUTER_PATH + 'eigrp')
        if 'hsrp' in config:
            tmp.append(ROUTER_PATH + 'hsrp')
        if 'ospf' in config:
            tmp.append(ROUTER_PATH + 'ospf')
        if 'ssh' in config:
            tmp.append(ROUTER_PATH + 'ssh')
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
