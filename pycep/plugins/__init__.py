"""Pycep plugin function load library."""
# coding=utf-8
from pycep.plugins.compile import markdown_in
from pycep.plugins.spellcheck import spellcheck
from pycep.plugins.linter import linter, package_questions, package_info, mapping_tags
from pycep.plugins.parser import parser
from pycep.plugins.new import new_module


def load_plugins(input_data, plugin, file_type, output, word_list, input_directory, export_dir, owner_id, input_file):
    """Process CLI input into plugin set variable."""
    if plugin == "compile":
        markdown_in(output, input_directory, export_dir)
    elif plugin == "spellcheck":
        spellcheck(input_data, word_list)
    elif plugin == "linter":
        linter(input_data)
    elif plugin == "parser":
        parser(input_data, output, input_file)
    elif plugin == "package_questions":
        package_questions(input_data)
    elif plugin == "package_info":
        package_info(input_data)
    elif plugin == "mapping_tags":
        mapping_tags(input_data)
    elif plugin == "new":
        new_module(output)
