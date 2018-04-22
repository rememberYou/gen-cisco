#!/usr/bin/env python3

import click
import sys

from pathlib import Path

from src.scripters.switch import *
from src.scripters.router import *

@click.command()
@click.option('--src', '-i', type=click.File('r'), help='The INI file.')
@click.option('--dest', '-o', type=str, help='The name of the generated script file.')
@click.option('--override', is_flag=True, help='Deletes the old file if it is overwritten.')
@click.pass_context
@click.version_option('1.0.0', '-v', '--version')
def cli(ctx, src, dest, override):
    """Generates Cisco scripts based on one of the INI files from the
    examples folder.

    \b
    Examples:
      python gen-cisco.py -i examples/router.ini
      python gen-cisco.py -i examples/router.ini -o r1.txt
      python gen-cisco.py -i examples/router.ini -o r1.txt --override

    """

    if src:
        if not dest:
            if '/' in src.name:
                dest = src.name.split('/')[1].split('.')[0] + '.txt'
            else:
                dest = src.name.split('.')[0] + '.txt'

        if not override and Path(dest).is_file():
            print("Error: Existing file ({})".format(dest))
            sys.exit(1)

        if 'router' in src.name:
            Router(src.name, dest).run()
        elif 'switch' in src.name:
            Switch(src.name, dest).run()
        else:
            print("Error: Invalid INI file ({})".format(src.name))
            sys.exit(1)
    else:
        click.echo(ctx.get_help())

cli()
