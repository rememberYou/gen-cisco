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

It is important to separate your Cisco template into several subfiles containing
a line or a piece of code used as a command. This allows the user to easily use
the appropriate protocol with the INI file including only the necessary sub
files.

Example:

```
! Enables EIGRP protocol routing for a specific autonomous system and/or
! switches to router configuration mode.
router eigrp <PROCESS>

! Suppress routing updates on an interface
passive-interface <PASSIVE_INTERFACE>
```

For this example, you must separate these two pieces of code in two separate
files (`src/templates/router/eigrp/process` and
`src/templates/router/eigrp/passive-interface`).

**NOTE:** it is **important to name the file** in the **same way as** the **word
between the rafters**, **except if** this **file contains several words between
rafters**. In this case, free to you for the file name, but in any case avoid
file names with underscores, pre-set dashes.

Check that you have written the words to replace in the templates in upper case
surrounded by rafters. If the word is composed, then separate the word by an
underscore (_e.g._: `<PW_PRIVILEGED>`).

**NOTE:** think each time back to the default mode (_User EXEC Mode_) in order to
easily integrate the other scripts.

## Adding new network protocol

To add a new network protocol, you first need to create a suitable section in
the INI file corresponding to the device supporting the protocol.

```
[myprotocol]
key1=value1
key2=value2
```

Be careful that the **section name** must have the **same name as** the
corresponding **Cisco template file**. The same goes for the name of the
**keys**, they must have the **same name as** their respective **word** to be
replaced **in the corresponding Cisco template**! Also, respect the syntax of an
[INI](https://www.wikiwand.com/en/INI_file) file in particular by favouring
hyphens over underscores.

**NOTE:** think each time back to the default mode (_User EXEC Mode_) in order to
easily integrate the other scripts.

Finally, you will need to create the Cisco template if this has not already been
done.

**NOTE:** if one of the keys has a Boolean value, it is necessary to enter the
key name in the `BOOL_KEYS` from the `src/scripter.py` file.

It's as simple as that!

## Adding new network device

To add support for a new device (_e.g._: server), you only need to add one INI
file (_e.g._: `examples/server.ini`) containing the addition of different
network protocols supported for the device (SEE: [Adding new network device](##adding-new-network-protocol)).

Finally, don't forget to create the `src/templates/device/` folder with
Cisco templates linked to the device.
