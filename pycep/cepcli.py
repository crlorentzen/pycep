"""pycep python cli python package."""
# coding=utf-8
import click
import json

from logging import DEBUG, ERROR, basicConfig, info

from pycep import __version__
from pycep.parser import extract_tar_file
from pycep.plugin import linter


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


def open_input_file(input_file, file_type):
    """Return raw data from input file string."""
    if file_type is "tar":
        input_data = extract_tar_file(input_file)
    if file_type == "json":
        with open(input_file, 'rb') as raw_json:
            input_data = raw_json.read()
    return input_data


@click.command()
@click.option("--input_file", "-f", help="The Package export tar.gz file.", required=True)
@click.option("--file_type", "-t", help="Input File type format json/tar.gz .", default="tar")
@click.option("--plugin", "-p", help="pycep function to run.", required=True)
@click.option('--debug/', "-d",  help="pycep function to run.",
              is_flag=True, callback=cli, expose_value=False, is_eager=True, default=False)
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def pycep_cli(input_file, plugin, file_type):
    """Pycep Command line interface."""
    if "linter" == plugin:
        info("pycep linter plugin running now...")
        linter(json.loads(open_input_file(input_file, file_type)))


if __name__ == '__main__':
    pycep_cli()
