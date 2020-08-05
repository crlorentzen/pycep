"""Pycep plugin function load library."""
# coding=utf-8
from pycep.plugins.compile import markdown_in
from pycep.plugins.spellcheck import spellcheck
from pycep.plugins.linter import linter, package_questions, package_info
from pycep.plugins.parser import parser


def load_plugins(input_data, plugin, file_type, output, word_list, input_directory, export_dir, owner_id, input_file):
    """Process CLI input into plugin set variable."""
    if plugin == "compile":
        markdown_in(input_data, plugin, file_type, output, word_list, input_directory, export_dir, owner_id, input_file)
    elif plugin == "spellcheck":
        spellcheck(input_data, plugin, file_type, output, word_list, input_directory, export_dir, owner_id, input_file)
    elif plugin == "linter":
        linter(input_data)
    elif plugin == "parser":
        parser(input_data, plugin, file_type, output, word_list, input_directory, export_dir, owner_id, input_file)
    elif plugin == "package_questions":
        package_questions(input_data)
    elif plugin == "package_info":
        package_info(input_data)
