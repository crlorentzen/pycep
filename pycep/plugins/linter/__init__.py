"""Pycep package linter cli library."""
# coding=utf-8
import re
from logging import info
from pycep.model import *
from pycep.plugins.parser import get_task_data


def chelp():
    print(f"Plugin: \n  cep_check: The core pycep linter plugin.\n")
    pass


def get_ceps():
    """Return CEP test dict object."""
    cep_2000 = {"cep_number": "2000",
                "cep_check_type": "contentModuleExportQuestionDescriptions",
                "regex_search": "Learning Objectives:*\n*.\n.*\n.*\n",
                "log_message": "Learning Objectives: with following 3 listed items not found!"}
    cep_2006 = {"cep_number": "2006",
                "cep_check_type": "contentModuleExportQuestionDescriptions",
                "regex_search": "Toolkit:*\n*.\n"}
    cep_2007 = {"cep_number": "2007",
                "cep_check_type": "contentModuleExportQuestionDescriptions",
                "string_search": "data:image/png",
                "log_message": "A png image was not found in the introduction task!"}
    cep_dict = {"cep2000": cep_2000, "cep2006": cep_2006, "cep2007": cep_2007}
    # TODO Build and parse from json files
    return cep_dict


def cep_check_message(cep_number: str):
    """Return cep help message."""
    return f"CEP {cep_number} Test Failed! | More info:  https://simspace.github.io/cep/ceps/{cep_number}/#requirements"


def cep_check(raw_task_data: str, package_name: str) -> None:
    """Return string result of content enhancement proposal test.

    :ivar raw_task_data: raw data of content task
    :raw_task_data raw_task_data: str
    :ivar package_name: string value of package module name
    :package_name package_name: string
    """
    cep_item_dict = get_ceps()
    for cep_items in cep_item_dict:
        cep_check_result = cep_check_message(cep_item_dict[cep_items][CEP_NUM])
        if cep_item_dict[cep_items][CEP_TYPE_CHECK] is QUESTION_DESC:
            if STR_SEARCH in cep_item_dict[cep_items]:
                cep_check_result = f"{package_name}: CEP {cep_item_dict[cep_items][CEP_NUM]} - Passed"
            if RE_SEARCH in cep_item_dict[cep_items]:
                test_search = cep_item_dict[cep_items][RE_SEARCH]
                x = re.findall(test_search, raw_task_data)
                if len(x) > 0:
                    cep_check_result = f"{package_name}: CEP {cep_item_dict[cep_items][CEP_NUM]} - Passed"
            if cep_check_result:
                if "Passed" not in cep_check_result:
                    error(f"{package_name}: {cep_check_result}")
                else:
                    info(cep_check_result)


def linter(raw_data: dict):
    """Process content module for cep standards."""
    package_export_content_modules = get_value(CONTENT_MOD_STRING, raw_data)[CONTENT_MOD_STRING]
    for values in package_export_content_modules:
        raw_task_data, package_name = get_task_data(package_export_content_modules, values)
        info(f"{package_name}: Processing tasks with linter now!")
        cep_check(raw_task_data, package_name)
