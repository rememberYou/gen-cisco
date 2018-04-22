Contributing
===============================

Nowaday, it has never been easier to contribute on a project. Inded, the
contribution can be made mainly in two ways:

1. Make any modification, in sending a pull request.
2. Report an issue on the issue tracker if you find bugs, have suggestions or
   any other problems.

Feel free to contact me on [IRC](http://webchat.freenode.net/) with `/q
rememberYou` to ask your questions and/or to discuss contributions.

--------------------

## Adding new Cisco templates

If you want to add other Cisco templates that can easily integrate with other
templates already present, add them to the `src/templates` directory in the
appropriate subfolder.

Check that you have written the words to replace in the template in upper case
surrounded by rafters. If the word is composed, then separate the word by an
underscore (*e.g.*: `<PW_PRIVILEGED>`)

**Note:** think each time back to the default mode (*User EXEC Mode*) in order to
easily integrate the other scripts.

## Adding new network protocol

To add a new network protocol, you first need to create a suitable section in
the INI file corresponding to the device supporting the protocol.

```
[myprotocol]
key1=value1
key2=value2
```

Be careful that the **keys** must have the **same name as** their respective
**word** to be replaced **in the corresponding Cisco template**! Also, respect
the syntax of an [INI](https://www.wikiwand.com/en/INI_file) file in particular
by favouring hyphens over underscores.

Next, you will need to create the Cisco template if this has not already been
done.

Finally, you must go to the Python file of the device supporting the protocol
(*e.g.*: `src/scripter/router.py`) and add a new condition in the
`get_templates` method, to integrate your template.

```python
...

if 'myprotocol' in config:
    tmp.append(ROUTER_PATH + 'myprotocol')

...
```

It's as simple as that!

**NOTE:** always set the password condition last, otherwise it will cause
problems for integrating other scripts.

## Adding new network device

To add support for a new device (*e.g.*: server), you must first add two files :

1. `examples/server.ini` : to add the necessary protocols to the server scripts.
2. `src/scripter/server.py`: to add a link between the server INI file and the
   Cisco templates to load.

Here is the bare minimum to include in your Python file:

```python
from src.scripter import *

DEVICE_PATH = "src/templates/device/"

class Device(Scripter):

    def get_templates(self, config):
        """Gets the templates that need to be used according dictionary
        with the device config.

        Args:
            dict: The dictionary with the device config.

        Returns:
            list: The list of templates to be used.

        """
        tmp = []
        # To be completed.
        if 'password' in config:
            tmp.append('src/templates/common/password')
        tmp.append('src/templates/common/saving')
        return tmp

    def run(self):
        """Generates the Cisco script for the device according to a
        config file.

        """
        templates = self.get_templates(self.config)
        self.create_file(self.dest, templates)
        for template in templates:
            dict_config = self.create_dict(template, self.config, template.split('/')[-1])
            self.replace_all(self.dest, dict_config)
```

Finally, don't forget to create the `src/templates/device/` folder with
Cisco templates linked to the device.
