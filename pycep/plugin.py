"""The pycep plugin function library."""
# coding=utf-8
import re
import nltk

from os import mkdir
from logging import info, error
from spellchecker import SpellChecker
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from pycep.render import write_to_file
from pycep.parse import get_slide_data, package_export_module_info, package_export_package_info, \
    get_slide_data_listed, cep_check
from pycep.model import content_module_string, ModuleExportContentModule, get_value, dir_character
from pycep.formatter import format_table, strip_unsafe_file_names, h_one_format


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
    main_package_data = package_export_package_info(raw_data)
    file_name = f"{strip_unsafe_file_names(main_package_data['name'].strip(' '))}.md"
    #if "contentModules" in main_package_data:
     #   main_package_data["contentModules"] = ""

    write_to_file(f"{output}{dir_character}{file_name}", format_table(main_package_data))
    for values in package_export_content_modules:
        raw_slide_data = get_slide_data_listed(package_export_content_modules, values)
        info("Processing slides with render plugin now!")
        for package in raw_slide_data:
            package_name_value = strip_unsafe_file_names(package)
            write_to_file(f"{output}{dir_character}{package_name_value}.md",
                          format_table(ModuleExportContentModule(package_export_content_modules[values][
                                                                     'contentModuleExportContentModule']).to_dict()))
            for slide_item in raw_slide_data[package]:
                try:
                    slide_name_string = strip_unsafe_file_names(slide_item)
                    write_to_file(f"{output}{dir_character}{package_name_value}{dir_character}{slide_name_string}.md",
                                  (h_one_format(slide_item) + raw_slide_data[package][slide_item]))
                except FileNotFoundError:
                    try:
                        mkdir(f"{output}{dir_character}{package_name_value}{dir_character}")
                        slide_name_string_value = strip_unsafe_file_names(slide_item)
                        write_to_file(
                            f"{output}{dir_character}{package_name_value}{dir_character}{slide_name_string_value}.md",
                            (h_one_format(slide_item) +
                            raw_slide_data[package][slide_item]))
                    except FileExistsError:
                        try:
                            slide_name_string_value = strip_unsafe_file_names(slide_item)
                            write_to_file(
                                f"{output}{dir_character}{package_name_value}{dir_character}{slide_name_string_value}"
                                f".md",
                                (h_one_format(slide_item) +
                                 raw_slide_data[package][slide_item]))
                        except FileExistsError:
                            error(f"{package} {slide_item} duplicate slide names found.")


def spell_check_slide(spell, line: dict, titles: str, package: str) -> None:
    for line_number in line:
        item = line[line_number]
        words = spell.split_words(item)
        test_spelling = spell.unknown(words)
        for slide_line_item in test_spelling:
            correct_spelling = spell.correction(slide_line_item)
            if slide_line_item == correct_spelling:
                correct_spelling = "N\A"
            error(f"Content Module Name: {package}\n"
                  f"Slide Title: {titles}\n"
                  f"Line Number: {str(line_number)}\n"
                  f"Line Data: {item}\n"
                  f"Spelling Error: {slide_line_item}\n"
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
    slide_data = return_non_data_slide(input_data)
    for package in slide_data:
        for values, lines in slide_data[package].items():
            spell_check_slide(spell, lines, values, package)


def sentiment_analyzer(input_data) -> None:
    """Check package for spelling errors."""
    nltk.download('vader_lexicon')
    info("Processing slides with sentimentanalyzer plugin now!")
    sid = SentimentIntensityAnalyzer()
    package_export_content_modules = get_value(content_module_string, input_data)[content_module_string]
    for values in package_export_content_modules:
        raw_slide_data = get_slide_data_listed(package_export_content_modules, values)
        for package in raw_slide_data:
            for titles, slide_item in raw_slide_data[package].items():
                line_count = 0
                line_item = slide_item.split("\n")
                for slide_line_item in line_item:
                    line_count += 1
                    test_search = "data:image\/\S{1,4};base64"
                    x = re.findall(test_search, slide_line_item)
                    if len(x) < 1 < len(slide_line_item):
                        print(f"Package: {package}\nSlide Title: {titles}\nLine Count: {line_count}\nSentence Analyzed:"
                              f" {slide_line_item}")
                        kvp = sid.polarity_scores(slide_line_item)
                        for k in kvp:
                            print(f"{k}: {kvp[k]}")
                        print()


def return_non_data_slide(input_data) -> dict:
    """Return structured data dict."""
    package_export_content_modules = get_value(content_module_string, input_data)[content_module_string]
    slide_dict = {}
    for values in package_export_content_modules:
        raw_slide_data = get_slide_data_listed(package_export_content_modules, values)
        for package in raw_slide_data:
            slide_dict[package] = {}
            for titles, slide_item in raw_slide_data[package].items():
                slide_dict[package][titles] = {}
                line_count = 0
                line_item = slide_item.split("\n")
                for slide_line_item in line_item:
                    line_count += 1
                    test_search = "data:image\/\S{1,4};base64"
                    x = re.findall(test_search, slide_line_item)
                    if len(x) < 1 < len(slide_line_item):
                        slide_dict[package][titles][line_count] = slide_line_item

    return slide_dict


def package_info(raw_data: dict):
    """Process content module for cep standards."""
    print(package_export_module_info(raw_data))
