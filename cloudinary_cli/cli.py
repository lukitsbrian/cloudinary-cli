#!/usr/bin/env python3
import click
from .utils import *
import cloudinary
from json import loads, dumps
from .core import config, search, uploader, admin, url
from .samples import sample, couple, dog
from .modules.make import make
from .modules.migrate import migrate
from .modules.sync import sync
from .modules.upload_dir import upload_dir
from .modules.delete_resources_from_file import delete_resources_from_file
# from .extensions import upload_dir, make, sync, migrate
# import csv as _csv
from .defaults import CLOUDINARY_CLI_CONFIG_FILE

CONTEXT_SETTINGS = dict(max_content_width=click.get_terminal_size()[0], terminal_width=click.get_terminal_size()[0])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("-c", "--config", help="""Temporary configuration to use. To use permanent config:
echo \"export CLOUDINARY_URL=YOUR_CLOUDINARY_URL\" >> ~/.bash_profile && source ~/.bash_profile
""")
@click.option("-C", "--config_saved", help="""Saved configuration to use - see `config` command""")
def cli(config, config_saved):
    if config:
        cloudinary._config._parse_cloudinary_url(config)
    elif config_saved:
        cloudinary._config._parse_cloudinary_url(loads(open(CLOUDINARY_CLI_CONFIG_FILE).read())[config_saved])
    pass

# Basic commands

cli.add_command(config)
cli.add_command(search)
cli.add_command(admin)
cli.add_command(uploader)
cli.add_command(url)

# Custom commands

cli.add_command(upload_dir)
cli.add_command(make)
cli.add_command(migrate)
cli.add_command(sync)
cli.add_command(delete_resources_from_file)

# Sample resources

cli.add_command(sample)
cli.add_command(couple)
cli.add_command(dog)

def main():
    cli()