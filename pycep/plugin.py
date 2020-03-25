"""The pycep plugin function library."""
# coding=utf-8
import re
import nltk
from os import mkdir
from json import dumps
from spellchecker import SpellChecker
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pycep.render import write_to_file
from pycep.parse import get_slide_data, package_export_module_info, package_export_package_info, \
    get_slide_data_listed, cep_check
from pycep.formatter import strip_unsafe_file_names, h_one_format, compile_package_data
from pycep.model import *


def linter(raw_data: dict):
    """Process content module for cep standards."""
    package_export_content_modules = get_value(CONTENT_MOD_STRING, raw_data)[CONTENT_MOD_STRING]
    for values in package_export_content_modules:
        raw_slide_data, package_name = get_slide_data(package_export_content_modules, values)
        info(f"{package_name}: Processing slides with linter now!")
        cep_check(raw_slide_data, package_name)


def get_content_module_names(content_list, package_export_content_modules):
    new_list = []
    for items in content_list:
        new_list.append(package_export_content_modules[items][EXPORT_MOD_STRING][N_STR])
    return new_list


def json_format_str(answer_data, slide_item):
    slide_answer_key = None
    for title in answer_data.items():
        if title[1]['title'] is slide_item:
            slide_answer_key = str({"question": title[1]['question']}).replace("'", '"')
            slide_answer_key = slide_answer_key.replace("True", "true")
            slide_answer_key = slide_answer_key.replace("False", "false")

    return slide_answer_key


def markdown_out(raw_data: dict, output: str):
    """Output package to md format."""
    package_export_content_modules = get_value(CONTENT_MOD_STRING, raw_data)[CONTENT_MOD_STRING]
    main_package_data = package_export_package_info(raw_data)
    file_name = f"{strip_unsafe_file_names(main_package_data[N_STR].strip(' '))}{JS_EXT}"
    if CONTENT_MODS in main_package_data:
        main_package_data[CONTENT_MODS] = get_content_module_names(main_package_data[CONTENT_MODS],
                                                                   package_export_content_modules)
    write_to_file(f"{output}{DIR_CHARACTER}{file_name}", dumps(main_package_data))
    for values in package_export_content_modules:
        raw_slide_data = get_slide_data_listed(package_export_content_modules, values)
        info("Processing slides with render plugin now!")
        answer_data = package_export_content_modules[values][EXPORT_TASKS]
        for package in raw_slide_data:
            package_name_value = strip_unsafe_file_names(package)
            module_json = ModuleExportContentModule(package_export_content_modules[values][
                                                                     EXPORT_MOD_STRING]).to_dict()

            yml_out = f"description: '{module_json['description']}'\n" \
                      f"name: '{module_json['name']}'\n" \
                      f"owner: '{module_json['owner']}'\n" \
                      f"randomizable: {module_json['randomizable']}\n" \
                      f"status:  '{module_json['status']}'\n" \
                      f"survey:  {module_json['survey']}\n" \
                      f"duration:  {module_json['duration']}\n"

            write_to_file(f"{output}{DIR_CHARACTER}{package_name_value}.yml", yml_out)
            for slide_item in raw_slide_data[package]:
                slide_answer_key = json_format_str(answer_data, slide_item)
                try:
                    slide_name_string = strip_unsafe_file_names(slide_item)
                    write_to_file(f"{output}{DIR_CHARACTER}{package_name_value}{DIR_CHARACTER}{slide_name_string}"
                                  f" {MD_EXT}", (h_one_format(slide_item) + raw_slide_data[package][slide_item]))
                    if slide_answer_key:
                        write_to_file(f"{output}{DIR_CHARACTER}{package_name_value}{DIR_CHARACTER}"
                                      f"{slide_name_string}{JS_EXT}", slide_answer_key)
                except FileNotFoundError:
                    try:
                        mkdir(f"{output}{DIR_CHARACTER}{package_name_value}{DIR_CHARACTER}")
                        slide_name_string_value = strip_unsafe_file_names(slide_item)
                        write_to_file(
                            f"{output}{DIR_CHARACTER}{package_name_value}{DIR_CHARACTER}{slide_name_string_value}"
                            f"{MD_EXT}", (h_one_format(slide_item) + raw_slide_data[package][slide_item]))
                        if slide_answer_key:
                            write_to_file(f"{output}{DIR_CHARACTER}{package_name_value}{DIR_CHARACTER}"
                                          f"{slide_name_string_value}{JS_EXT}",
                                          slide_answer_key)
                    except FileExistsError:
                        try:
                            slide_name_string_value = strip_unsafe_file_names(slide_item)
                            write_to_file(
                                f"{output}{DIR_CHARACTER}{package_name_value}{DIR_CHARACTER}{slide_name_string_value}"
                                f"{MD_EXT}", (h_one_format(slide_item) + raw_slide_data[package][slide_item]))
                            if slide_answer_key:
                                write_to_file(f"{output}{DIR_CHARACTER}{package_name_value}{DIR_CHARACTER}"
                                              f"{slide_name_string_value}{JS_EXT}",
                                              (str(slide_answer_key)))
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
    package_export_content_modules = get_value(CONTENT_MOD_STRING, input_data)[CONTENT_MOD_STRING]
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
    package_export_content_modules = get_value(CONTENT_MOD_STRING, input_data)[CONTENT_MOD_STRING]
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


def markdown_in(package_export_name: str, input_dir: str, export_dir: str, owner_id: str):
    info("Compiling package export now with the markdown_in plugin now!")
    compile_package_data(package_export_name, input_dir, export_dir, owner_id)


def package_info(raw_data: dict):
    """Process content module for cep standards."""
    print(package_export_module_info(raw_data))
