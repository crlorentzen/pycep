from logging import info
import re
from pycep.model import *
from pycep.plugins.parser import get_task_data


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


def package_info(raw_data: dict):
    """Process CLI input with package_info plugin function."""
    """Process module data return package information."""
    print(package_export_module_info(raw_data))


def package_export_module_info(raw_data):
    package_data = {}
    package_export_content_modules = get_value(CONTENT_MOD_STRING, raw_data)[CONTENT_MOD_STRING]
    for values in package_export_content_modules:
        module_data = ModuleExportContentModule(package_export_content_modules[values][EXPORT_MOD_STRING])
        package_data[values] = {}
        for data_value, value in module_data.to_dict().items():
            if value and data_value != ('questions' or 'tasks'):
                package_data[values][data_value] = value
    return package_data


def package_export_question_info(raw_data):
    package_data = {}
    package_export_content_modules = get_value(CONTENT_MOD_STRING, raw_data)[CONTENT_MOD_STRING]
    question_data = {}
    for values in package_export_content_modules:
        module_data = ModuleExportContentModule(package_export_content_modules[values][EXPORT_MOD_STRING])
        package_data[values] = {}
        for data_value, value in module_data.to_dict().items():
            if value or data_value == 'questions':
                package_data[values][data_value] = value
    for module in package_data:
        module_name = package_data[module][N_STR]
        question_data[module_name] = package_data[module]["questions"]
    return question_data


def package_questions(raw_data: dict):
    """Return package question data."""
    data = package_export_question_info(raw_data)
    for item in data:
        print(f"Content Module: {item} ")
        for value in data[item]:
            for tasks in value:
                if "question" in tasks['val']:
                    print(f"\n  TaskTitle: {tasks['val']['title']}")
                    print(f"  PointTotal: {tasks['val']['question']['points']}")
                    print(f"  RetryCount: {tasks['val']['question']['retryCount']}")
                    answer_number = 0
                    answer_data = ""
                    for answers in tasks['val']['question']["choices"]:
                        if answers["correct"] is True:
                            answer_number += 1
                            answer_data += f"    Answer {answer_number}: {answers['value']}\n"
                    print(answer_data[:-1])
                    hint_number = 0
                    hints_data = ""
                    for hints in tasks['val']['question']["hints"]:
                        hint_number += 1
                        hints_data += f"    Hint{hint_number}:\n"
                        hints_data += f"      Cost: {hints['pointsDeduction']}\n"
                        hint_text = hints['text'].replace('\n', "\n               ")
                        hints_data += f"      Message: \"{hint_text}\" \n"
                    print(hints_data[:-1])
        print(f"\n")


def linter(raw_data: dict):
    """Process content module for cep standards."""
    package_export_content_modules = get_value(CONTENT_MOD_STRING, raw_data)[CONTENT_MOD_STRING]
    for values in package_export_content_modules:
        raw_task_data, package_name = get_task_data(package_export_content_modules, values)
        info(f"{package_name}: Processing tasks with linter now!")
        cep_check(raw_task_data, package_name)
