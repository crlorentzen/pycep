#!/usr/bin/env python
"""The pycep cli python package."""
# coding=utf-8
import click
import json
import ujson


from logging import DEBUG, ERROR, basicConfig, error
from pycep import __version__
from pycep.plugins import load_plugins
from pycep.render import extract_tar_file


def open_input_file(input_file, file_type):
    """Return raw data from input file string."""
    if input_file:
        if file_type == "tar":
            input_data = extract_tar_file(input_file)
        if file_type == "json":
            with open(input_file, 'rb') as raw_json:
                input_data = raw_json.read()
        return input_data
    else:
        return None


def value_check(value, ctx):
    """Return boolean result from ctx parsing."""
    if not value or ctx.resilient_parsing:
        return True
    return False


def cli(ctx, param, debug):
    """Set command line debug level output to stdout."""
    if value_check(debug, ctx):
        return
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))
    if debug:
        logging_level = DEBUG
        log_format = 'Process Time: %(asctime)s | %(message)s'
    else:
        logging_level = ERROR
        log_format = '%(message)s'
    basicConfig(level=logging_level, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')


def print_version(ctx, param, value):
    """Print pycep version to stdout."""
    if value_check(value, ctx):
        return
    click.echo(str(__version__))
    ctx.exit()


@click.command()
@click.option("--input_file", "-f", help="The Package export tar.gz or the json file .")
@click.option("--file_type", "-t", help="Input File type format json/tar.gz.", default="tar")
@click.option("--output", "-o", help="Output file directory.")
@click.option("--word_list", "-w", help="Input spelling word list.", default="./data/word_list.txt")
@click.option("--plugin", "-p", help="Plugin for pycep to run.", required=True)
@click.option("--input_directory", "-g", help="The Package export directory that generates a package export tar.gz or "
                                              "the json file ")
@click.option('--debug/', "-d",  help="Turn debug mode on.",
              is_flag=True, callback=cli, expose_value=False, is_eager=True, default=False)
@click.option('--version', help="Print Application Version",
              is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option("--export-dir", "-e", help="Export file directory.", envvar='EXPORT_DIR')
@click.option("--owner-id", "-uid", help="User account UID.", envvar='OWNER_ID')
def pycep_cli(input_file, plugin, file_type, output, word_list, input_directory, export_dir, owner_id):
    """Pycep Command line interface."""
    # Parse input archive and return dict type variable.
    if input_file:
        try:
            input_data = ujson.loads(open_input_file(input_file, file_type))
        except:
            input_data = json.loads(open_input_file(input_file, file_type))
    else:
        input_data = None
    # Pass input data to plugins
    load_plugins(input_data, plugin, file_type, output, word_list, input_directory, export_dir, owner_id, input_file)


if __name__ == '__main__':
    pycep_cli()
