"""Pycep spellcheck plugin library."""
# coding=utf-8
import re
import click
import nltk

from os import curdir
from logging import info, error
from nltk.sentiment import SentimentIntensityAnalyzer
# noinspection PyPackageRequirements
from spellchecker import SpellChecker
from pycep.content_strings import CONTENT_MOD_STRING
from pycep.model import get_value
from pycep.plugins.parser import get_task_data_listed, return_non_data_task


@click.group()
@click.option("--custom_list", "-w", help="Input spelling word list.", default="pycep/data/word_list.txt")
def custom_lis(custom_list):
    """--custom_list help=Custom Word List Path Directory"""


def sentiment_analyzer(input_data) -> None:
    """Check package for spelling errors."""
    nltk.download('vader_lexicon')
    info("Processing tasks with sentimentanalyzer plugin now!")
    sid = SentimentIntensityAnalyzer()
    package_export_content_modules = get_value(CONTENT_MOD_STRING, input_data)[CONTENT_MOD_STRING]
    for values in package_export_content_modules:
        raw_task_data = get_task_data_listed(package_export_content_modules, values)
        for package in raw_task_data:
            for titles, task_item in raw_task_data[package].items():
                line_count = 0
                line_item = task_item.split("\n")
                for task_line_item in line_item:
                    line_count += 1
                    test_search = "data:image\/\S{1,4};base64"
                    x = re.findall(test_search, task_line_item)
                    if len(x) < 1 < len(task_line_item):
                        print(f"Package: {package}\nTask Title: {titles}\nLine Count: {line_count}\nSentence Analyzed:"
                              f" {task_line_item}")
                        kvp = sid.polarity_scores(task_line_item)
                        for k in kvp:
                            print(f"{k}: {kvp[k]}")
                        print()


def spellcheck(input_data: dict,
               plugin,
               file_type,
               output,
               word_list,
               input_directory,
               export_dir,
               owner_id,
               input_file) -> None:
    """Check package for spelling errors."""
    spell = SpellChecker()
    try:
        spell.word_frequency.load_text_file(word_list)
        with open(word_list, 'r') as data_file:
            word_list_data = data_file.read()
    except FileNotFoundError:
        info("Word list not found searching up a directory...")
        # Search for word list if not found.
        search_path = f"/opt/pycep/word_list.txt"
        spell.word_frequency.load_text_file(search_path)
        with open(search_path, 'r') as data_file:
            word_list_data = data_file.read()
    known_data_list = word_list_data.split("\n")
    spell.known(known_data_list)
    task_data = return_non_data_task(input_data)
    for package in task_data:
        for values, lines in task_data[package].items():
            spell_check_task(spell, lines, values, package)


def spell_check_task(spell, line: dict, titles: str, package: str) -> None:
    for line_number in line:
        item = line[line_number]
        words = spell.split_words(item)
        test_spelling = spell.unknown(words)
        for task_line_item in test_spelling:
            correct_spelling = spell.correction(task_line_item)
            if task_line_item == correct_spelling:
                correct_spelling = "N\A"
            error(f"Content Module Name: {package}\n"
                  f"Task Title: {titles}\n"
                  f"Line Number: {str(line_number)}\n"
                  f"Line Data: {item}\n"
                  f"Spelling Error: {task_line_item}\n"
                  f"Suggested replacement: {correct_spelling}\n")
