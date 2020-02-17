"""The pycep python plugin function library."""
# coding=utf-8
import re

from os import mkdir
from logging import info, error

from spellchecker import SpellChecker

from pycep.parser import get_value, get_slide_data, cep_check, get_slide_data_listed, h_one_format
from pycep.render import write_to_file

content_module_string = 'packageExportContentModules'


def linter(raw_data: dict):
    """Process content module for cep standards."""
    package_export_content_modules = get_value(content_module_string, raw_data)[content_module_string]
    for values in package_export_content_modules:
        raw_slide_data, package_name = get_slide_data(package_export_content_modules, values)
        info(f"{package_name}: Processing slides with linter now!")
        cep_check(raw_slide_data, package_name)


def markdown_out(raw_data: dict, output: str):
    """Output package to md format."""
    package_export_content_modules = get_value(content_module_string, raw_data)[content_module_string]
    for values in package_export_content_modules:
        raw_slide_data = get_slide_data_listed(package_export_content_modules, values)
        info("Processing slides with render plugin now!")
        for package in raw_slide_data:
            for slide_item in raw_slide_data[package]:
                try:
                    write_to_file((output + "/" + package.strip(" ") + "/" + slide_item + ".md"),
                                  (h_one_format(slide_item) + raw_slide_data[package][slide_item]))
                except FileNotFoundError:
                    mkdir(output + "/" + package.strip(" ") + "/")
                    write_to_file((output + "/" + package.strip(" ") + "/" + slide_item + ".md"),
                                  (h_one_format(slide_item) + raw_slide_data[package][slide_item]))


def spell_check_slide(spell, line_count, slide_line_item, package, titles):
    words = spell.split_words(slide_line_item)
    test_spelling = spell.unknown(words)
    for item in test_spelling:
        correct_spelling = spell.correction(item)
        if item == correct_spelling:
            correct_spelling = "N\A"
        error(f"Content Module Name: {package}\n"
              f"Slide Title: {titles}\n"
              f"Line Number: {str(line_count)}\n"
              f"Line Data: {slide_line_item}\n"
              f"Spelling Error: {item}\n"
              f"Suggested replacement: {correct_spelling}\n")


def spellcheck(input_data: dict, word_list) -> None:
    """Check package for spelling errors."""
    spell = SpellChecker()
    try:
        spell.word_frequency.load_text_file(word_list)
        with open(word_list, 'r') as data_file:
            word_list_data = data_file.read()
    except FileNotFoundError:
        info("Word list not found searching up a directory...")
        # Search for word list if not found.
        spell.word_frequency.load_text_file("../" + word_list)
        with open("../" + word_list, 'r') as data_file:
            word_list_data = data_file.read()
    known_data_list = word_list_data.split("\n")
    spell.known(known_data_list)
    package_export_content_modules = get_value(content_module_string, input_data)[content_module_string]
    for values in package_export_content_modules:
        raw_slide_data = get_slide_data_listed(package_export_content_modules, values)
        info("Processing slides with spellcheck plugin now!")
        for package in raw_slide_data:
            for titles, slide_item in raw_slide_data[package].items():
                line_count = 0
                line_item = slide_item.split("\n")
                for slide_line_item in line_item:
                    line_count += 1
                    # Search for encoded image data, if found exclude from spellcheck search.
                    # TODO Add optional multi processing support.
                    test_search = "data:image\/\S{1,4};base64"
                    x = re.findall(test_search, slide_line_item)
                    if len(x) < 1:
                        spell_check_slide(spell, line_count, slide_line_item, package, titles)
