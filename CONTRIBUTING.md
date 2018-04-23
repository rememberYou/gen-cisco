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
underscore (_e.g._: `<PW_PRIVILEGED>`)

**Note:** think each time back to the default mode (_User EXEC Mode_) in order to
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

Finally, you will need to create the Cisco template if this has not already been
done.

It's as simple as that!

## Adding new network device

To add support for a new device (_e.g._: server), you only need to add one INI
file (_e.g._: `examples/server.ini`) containing the addition of different
network protocols supported for the device (SEE: [Adding new network device](##adding-new-network-protocol)).

Finally, don't forget to create the `src/templates/device/` folder with
Cisco templates linked to the device.
