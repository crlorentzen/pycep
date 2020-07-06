"""Pycep plugin function load library."""
# coding=utf-8
import os
import glob
import importlib
from logging import info


def load_plugins(input_data, plugin, file_type, output, word_list, input_directory, export_dir, owner_id, input_file):
    """Process CLI input into plugin set variable."""
    modules = glob.glob(os.path.dirname(__file__) + "/*")
    blacklist = {'__pycache__'}
    info(f"Loading data from path {os.path.dirname(__file__)}")
    for module in modules:
        module_name = os.path.basename(module)
        if os.path.isdir(module) and module_name not in blacklist:
            module = '.' + module_name
            module = importlib.import_module(module, package='pycep.plugins')
            # This gets the load function in the __init__.py of the plugin.
            if plugin == ("--help" or "help"):
                module.chelp()
            if module_name == plugin:
                module.load(input_data,
                            plugin,
                            file_type,
                            output,
                            word_list,
                            input_directory,
                            export_dir,
                            owner_id,
                            input_file)
