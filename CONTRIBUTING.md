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
the appropriate protocol with the YAML file including only the necessary sub
files.

In order to write your Cisco template, it will probably be necessary to use the
[Jinja2](http://jinja.pocoo.org/) syntax which will automatically fill these
fields according to those present in the YAML file.

Example:

```
{% if basic.name %}
  ! Sets system's network name
  hostname {{ basic.name }}
{% endif %}
```

**NOTE:** it is **important to name the file** in the **same way as the word**
present **at the second level of the tree** in the YAML file. Also, for file
names privilege hyphens to underscores.

In the example above, the file name is: `src/templates/router/basic/name`
because this Cisco template concerns a `router`, in the `basic` section of the
YAML file with the `name` as key.

```yaml
basic:
  name: R1
```

One last thing, think every time to the default mode (_User EXEC Mode_) in order to
easily integrate the other scripts, if it's needed.

## Adding new network protocol

To add a new network protocol, you first need to create a suitable section in
the YAML file corresponding to the device supporting the protocol.

```yaml
myprotocol:
  key1: value1
  key2: value2
```

Be careful that the **section name** must have the **same name as** the
corresponding **Cisco templates folder**. Also, respect the syntax of a
[YAML](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)
file in particular by favouring underscores over hyphens.

Finally, you will need to create the Cisco template if this has not already been
done.

It's as simple as that!

## Adding new network device

To add support for a new device (_e.g._: server), you only need to add one YAML
file (_e.g._: `examples/server.yml`) containing the addition of different
network protocols supported for the device.

Also, don't forget to create the `src/templates/device/` folder with Cisco
templates linked to the device.
