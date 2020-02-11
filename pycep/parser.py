"""The pycep python parsing function library."""
# coding=utf-8
import re
import tarfile

from sys import exit
from logging import error, info
from pycep.ceps import CEPS


def extract_tar_file(file_name: str):
    try:
        tar_file = tarfile.open(file_name, mode="r:gz")
        json_file = tar_file.extractfile("package_export.json")
        return json_file.read()
    except tarfile.ReadError:
        error("Input file " + file_name + " is not a proper tar.gz exiting now\n"
                                          "please correct the file_type input.")
        exit(1)


def get_value(item: str, json_package: dict) -> dict:
    """Return dict item."""
    return_dict = {}
    if item in json_package:
        return_dict[item] = json_package[item]
    return return_dict


def cep_check_message(cep_number: str):
    """Return cep help message."""
    return "CEP " + cep_number + " Test Failed!" + " | " + \
        "More info: https://simspace.github.io/cep/ceps/" + cep_number + "/#requirements"


def get_slide_data(package_export_content_modules, values):
    package_value = package_export_content_modules[values]['contentModuleExportContentModule']
    package_name = package_value['name']
    raw_data = ""
    content_data_node = package_export_content_modules[values]['contentModuleExportQuestionDescriptions']
    info(package_name + ": Rendering " + str(len(content_data_node)) + " slides into raw data.")
    for slide_item in content_data_node:
        if 'data' in content_data_node[slide_item]:
            check_dic = content_data_node[slide_item]['data']['document']['nodes']
            render_slide_data = render_slide(check_dic)
            if render_slide_data:
                raw_data += "# " + package_export_content_modules[values]['contentModuleExportQuestions'][
                    slide_item]['title'] + "\n"
                raw_data += render_slide_data
    return raw_data, package_name


def linter(raw_data: dict):
    content_module_string = 'packageExportContentModules'
    package_export_content_modules = get_value(content_module_string, raw_data)[content_module_string]
    for values in package_export_content_modules:
        raw_slide_data, package_name = get_slide_data(package_export_content_modules, values)
        info(package_name + ": Processing slides with linter now!")
        cep_check(raw_slide_data, package_name)


def cep_check(raw_slide_data: str, package_name: str) -> None:
    """Return string result of content enhancement proposal test.
    :ivar raw_slide_data: raw data of content slide
    :raw_slide_data raw_slide_data: str
    :ivar package_name: string value of package module name
    :package_name package_name: string
    """
    cep_item_dict = CEPS
    for cep_items in cep_item_dict:
        cep_check_result = cep_check_message(cep_item_dict[cep_items]["cep_number"])
        if cep_item_dict[cep_items]["cep_check_type"] is "contentModuleExportQuestionDescriptions":
            if "string_search" in cep_item_dict[cep_items]:
                cep_check_result = package_name + ": CEP " + cep_item_dict[cep_items]["cep_number"] + " - Passed"
            if "regex_search" in cep_item_dict[cep_items]:
                test_search = cep_item_dict[cep_items]["regex_search"]
                x = re.findall(test_search, raw_slide_data)
                if len(x) > 0:
                    cep_check_result = package_name + ": CEP " + cep_item_dict[cep_items]["cep_number"] + " - Passed"
            if cep_check_result:
                if "Passed" not in cep_check_result:
                    error(package_name + ": " + cep_check_result)
                else:
                    info(cep_check_result)


def render_list_item(slide_line: dict, heading_level: str):
    """Return formatted list data.

    """
    raw_list_data = ""
    for node in slide_line:
        raw_list_data += heading_level + node['text']
    return raw_list_data


def render_nested_list_nodes(slide_line: dict, format_string: str):
    raw_list_data = ""
    for node in slide_line:
        if 'text' in node:
            raw_list_data += "   * " + node['text'] + "\n"
        else:
            for nested_node in node["nodes"]:
                if 'text' in nested_node:
                    raw_list_data += format_string + nested_node['text'] + "\n"
                else:
                    if 'text' in nested_node["nodes"][0]:
                        raw_list_data += "   * " + nested_node["nodes"][0]['text'] + "\n"
    return raw_list_data


def strip_end_space(string_value: str):
    while string_value[-1:] == " ":
        string_value = string_value[:-1]
    return string_value


def render_slide(slide_dict: dict):
    """Return string data from content module slide data."""
    raw_slide_data = ""
    if slide_dict:
        for slide_line in slide_dict:
            if 'type' in slide_line:
                if 'paragraph' in slide_line['type']:
                    if "marks" in slide_line['nodes'][0] and len(slide_line['nodes'][0]['marks']) > 0:
                        if "bold" == slide_line['nodes'][0]['marks'][0]['type']:
                            if len(slide_line['nodes'][0]['text']) > 0:
                                raw_slide_data += "***" + strip_end_space(slide_line['nodes'][0]['text']) + "***" + "\n"
                    else:
                        raw_slide_data += slide_line['nodes'][0]['text'] + "\n"
                elif 'unordered-list' in slide_line['type']:
                    raw_list_data = render_nested_list_nodes(slide_line['nodes'], "   * ")
                    if len(raw_list_data) > 0:
                        raw_slide_data += raw_list_data
                elif 'heading-two' in slide_line['type']:
                    raw_heading_data = render_list_item(slide_line['nodes'], '## ')
                    if len(raw_heading_data) > 3:
                        raw_slide_data += raw_heading_data + "\n"
                elif 'heading-one' in slide_line['type']:
                    raw_heading_data = render_list_item(slide_line['nodes'], '# ')
                    if len(raw_heading_data) > 2:
                        raw_slide_data += raw_heading_data + "\n"
                elif 'image-block' in slide_line['type']:
                    raw_slide_data += "-   []() \n"
                elif 'code-block' in slide_line['type']:
                    raw_heading_data = render_nested_list_nodes(slide_line['nodes'], "    ")
                    if len(raw_heading_data) > 3:
                        raw_slide_data += raw_heading_data
                else:
                    error("Data type " + slide_line['type'] + "unknown")
                    raw_slide_data += "Data Type Unknown \n"
    return raw_slide_data
