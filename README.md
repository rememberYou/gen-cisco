# ![Cisco Logo](assets/cisco.png "Cisco logo") gen-cisco

`gen-cisco` is an API and CLI to facilitate the creation of your Cisco scripts
using an INI file. This file groups a section for each protocol including the
values to be replaced in the appropriate Cisco template.

The creation of these templates has been done during the various _CCNA_ training
courses offered by Cisco, using [Packet
Tracer](https://www.netacad.com/courses/packet-tracer-download/), a network
simulation and visualization tool. Therefore, some commands may need to be
modified on real hardware.

---

### Installation

It's as simple as that:

```
pip install gen-cisco
```

---

### Usage

```
Usage: gen-cisco.py [OPTIONS]

  Generates Cisco scripts based on INI files

  Examples:
    python gen-cisco.py -i examples/router.ini
    python gen-cisco.py -i examples/router.ini -o r1.txt
    python gen-cisco.py -i examples/router.ini -o r1.txt -l
    python gen-cisco.py -i examples/router.ini -o r1.txt --override

Options:
  -i, --src FILENAME  The INI file.
  -o, --dest TEXT     The name of the generated script file.
  --override          Deletes the old file if it is overwritten.
  -l, --log           Outputs the final script to the console.
  -v, --version       Show the version and exit.
  --help              Show this message and exit.
```

Alternatively you can run this tool using Docker:

```bash
# Build the image
docker build -t gen-cisco .

# Run the image
docker run -v $(pwd):/app gen-cisco python gen-cisco.py [OPTIONS]
```

---

### Supported Features

Here is a list of features configurable by the scripts:

```
 basic ➔ basic configuration for routers and switches
 eigrp ➔ advanced distance-vector routing protocol
 ospf  ➔ routing protocol for Internet Protocol networks
 ssh   ➔ cryptographic network protocol for operating network services securely over an unsecured network
```

For a complete list sorted by device, please visit the [wiki](https://github.com/rememberYou/gen-cisco/wiki/Supported-Features).

---

### Contributions

Adding a new protocol to script as well as supporting a new device is easy. To
do that, first take a look at the [CONTRIBUTING](https://github.com/rememberYou/gen-cisco/blob/master/CONTRIBUTING.md)
file. Also, feel free to submit your bugs and suggestions by opening an issue in
the issue tracker, it would help us a lot.

---

### License

Code is under the [MIT License](https://github.com/rememberYou/gen-cisco/blob/master/LICENSE).
