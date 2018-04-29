#!/usr/bin/env python3

import click
import sys

from pathlib import Path
from src.scripter import *

@click.command()
@click.option('--src', '-i', type=click.File('r'), help='The YAML file.')
@click.option('--dest', '-o', type=str, help='The name of the generated script file.')
@click.option('--override/--no-override', default=True, help='Deletes the old file if it is overwritten.')
@click.option('--verbose', '-v', is_flag=True, help='Outputs the final script to the console.')
@click.pass_context
@click.version_option('1.2.0', '--version')
def cli(ctx, src, dest, override, verbose):
    """Generates Cisco scripts based on YAML files

    \b
    Examples:
      python gen-cisco.py -i examples/router.yml
      python gen-cisco.py -i examples/router.yml -o r1.txt
      python gen-cisco.py -i examples/router.yml -o r1.txt -v
      python gen-cisco.py -i examples/router.yml -o r1.txt --no-override

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
            Scripter('./examples/router.yml', dest, 'router').run(verbose)
        elif 'switch' in src.name:
            Scripter('./examples/switch.yml', dest, 'switch').run(verbose)
        else:
            print("Error: Invalid YAML file ({})".format(src.name))
            sys.exit(1)
    else:
        click.echo(ctx.get_help())

cli()
