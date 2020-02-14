"""The pycep python parsing function library."""
# coding=utf-8
import re
import random
import string

from logging import error, info

from pycep.ceps import CEPS
from pycep.render import extract_tar_file


def open_input_file(input_file, file_type):
    """Return raw data from input file string."""
    if file_type is "tar":
        input_data = extract_tar_file(input_file)
    if file_type == "json":
        with open(input_file, 'rb') as raw_json:
            input_data = raw_json.read()
    return input_data


def get_value(item: str, json_package: dict) -> dict:
    """Return dict item."""
    return_dict = {}
    if item in json_package:
        return_dict[item] = json_package[item]
    return return_dict


def cep_check_message(cep_number: str):
    """Return cep help message."""
    return f"CEP {cep_number} Test Failed! | More info:  https://simspace.github.io/cep/ceps/{cep_number}/#requirements"


def get_slide_data(package_export_content_modules: dict, values: str):
    """Return raw data from package and package name."""
    package_data = package_export_content_modules[values]
    package_value = package_data['contentModuleExportContentModule']
    package_name = package_value['name']
    raw_data = ""
    content_data_node = package_data['contentModuleExportQuestionDescriptions']
    info(package_name + ": Rendering " + str(len(content_data_node)) + " slides into raw data.")
    for slide_item in content_data_node:
        if 'data' in content_data_node[slide_item]:
            check_dic = content_data_node[slide_item]['data']['document']['nodes']
            render_slide_data = render_slide(check_dic)
            if render_slide_data:
                raw_data += add_newline("# " + package_data['contentModuleExportQuestions'][slide_item]['title']) + \
                            render_slide_data
    return raw_data, package_name


def h_one_format(heading_data):
    return f"# {add_newline(heading_data)}"


def get_slide_data_listed(package_export_content_modules: dict, values: str):
    """Return raw data from package and package name."""
    package_value = package_export_content_modules[values]['contentModuleExportContentModule']
    package_name = package_value['name']
    raw_data_dict = {package_name: {}}
    content_data_node = package_export_content_modules[values]['contentModuleExportQuestionDescriptions']
    info(package_name + ": Rendering " + str(len(content_data_node)) + " slides into raw data.")
    for slide_item in content_data_node:
        if 'data' in content_data_node[slide_item]:
            check_dic = content_data_node[slide_item]['data']['document']['nodes']
            render_slide_data = render_slide(check_dic)
            if render_slide_data:
                raw_data_dict[package_name][package_export_content_modules[values]['contentModuleExportQuestions'][
                    slide_item]['title']] = render_slide_data
    return raw_data_dict


def id_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


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
                cep_check_result = f"{package_name}: CEP {cep_item_dict[cep_items]['cep_number']} - Passed"
            if "regex_search" in cep_item_dict[cep_items]:
                test_search = cep_item_dict[cep_items]["regex_search"]
                x = re.findall(test_search, raw_slide_data)
                if len(x) > 0:
                    cep_check_result = f"{package_name}: CEP {cep_item_dict[cep_items]['cep_number']} - Passed"
            if cep_check_result:
                if "Passed" not in cep_check_result:
                    error(f"{package_name}: {cep_check_result}")
                else:
                    info(cep_check_result)


def render_list_item(slide_line: dict, heading_level: str):
    """Return formatted list data."""
    raw_list_data = ""
    for node in slide_line:
        raw_list_data += f"{heading_level}{node['text']}"
    if len(heading_level) == len(raw_list_data):
        return None
    return raw_list_data


def render_nested_list_nodes(slide_line: dict, format_string: str):
    """Return raw list data from nested node data."""
    raw_list_data = ""
    for node in slide_line:
        if 'text' in node:
            raw_list_data += add_newline(f"   * {node['text']}")
        else:
            for nested_node in node["nodes"]:
                if 'text' in nested_node:
                    raw_list_data += add_newline(format_string + nested_node['text'])
                else:
                    if 'text' in nested_node["nodes"][0]:
                        raw_list_data += add_newline(f"   * {nested_node['nodes'][0]['text']}")
    return raw_list_data


def strip_end_space(string_value: str):
    """Remove escape character from end of input string value and return."""
    while string_value[-1:] == " ":
        string_value = string_value[:-1]
    return string_value


def add_newline(input_item: str) -> str:
    return f"{input_item}\n"


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
                                raw_slide_data += add_newline(strip_end_space(slide_line['nodes'][0]['text']))
                    else:
                        raw_slide_data += add_newline(slide_line['nodes'][0]['text'])
                elif 'unordered-list' in slide_line['type']:
                    raw_list_data = render_nested_list_nodes(slide_line['nodes'], "   * ")
                    if len(raw_list_data) > 0:
                        raw_slide_data += raw_list_data
                elif 'ordered-list' in slide_line['type']:
                    raw_list_data = render_nested_list_nodes(slide_line['nodes'], "   * ")
                    if len(raw_list_data) > 0:
                        raw_slide_data += add_newline(raw_list_data)
                elif 'list-item-child' in slide_line['type']:
                    raw_list_data = render_nested_list_nodes(slide_line['nodes'], "   * ")
                    if len(raw_list_data) > 0:
                        raw_slide_data += raw_list_data
                elif 'heading-two' in slide_line['type']:
                    raw_heading_data = render_list_item(slide_line['nodes'], '### ')
                    if raw_heading_data:
                        raw_slide_data += add_newline(raw_heading_data)
                elif 'heading-one' in slide_line['type']:
                    raw_heading_data = render_list_item(slide_line['nodes'], '## ')
                    if raw_heading_data:
                        raw_slide_data += add_newline(raw_heading_data)
                elif 'image-block' in slide_line['type']:
                    picture_id = id_generator()
                    raw_heading_data = f"![{picture_id}]({slide_line['data']['imageData']})"
                    if raw_heading_data:
                        raw_slide_data += add_newline(raw_heading_data)
                elif 'code-block' in slide_line['type']:
                    raw_heading_data = render_nested_list_nodes(slide_line['nodes'], "    ")
                    if raw_heading_data:
                        raw_slide_data += raw_heading_data
                elif 'code-line' in slide_line['type']:
                    raw_heading_data = render_nested_list_nodes(slide_line['nodes'], "    ")
                    if raw_heading_data and len(raw_heading_data) > 5:
                        raw_slide_data += add_newline(raw_heading_data)
                else:
                    error("Data type " + slide_line['type'] + "unknown")
                    raw_slide_data += " Data Type Unknown\n"
    return raw_slide_data
