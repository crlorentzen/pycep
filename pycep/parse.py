"""The pycep parsing function library."""
# coding=utf-8
import re
import random
import string

from pycep.ceps import CEPS
from pycep.render import extract_tar_file
from pycep.model import get_value, ModuleExportContentModule, PackageExport, strip_end_space
from pycep.content_strings import *


def open_input_file(input_file, file_type):
    """Return raw data from input file string."""
    if input_file:
        if file_type == "tar":
            input_data = extract_tar_file(input_file)
        if file_type == "json":
            with open(input_file, 'rb') as raw_json:
                input_data = raw_json.read()
        return input_data
    else:
        return None


def cep_check_message(cep_number: str):
    """Return cep help message."""
    return f"CEP {cep_number} Test Failed! | More info:  https://simspace.github.io/cep/ceps/{cep_number}/#requirements"


def get_slide_data(package_export_content_modules: dict, values: str):
    """Return raw data from package and package name."""
    package_data = package_export_content_modules[values]
    package_value = package_data[EXPORT_MOD_STRING]
    package_name = package_value[N_STR]
    raw_data = ""
    content_data_node = package_data[QUESTION_DESC]
    info(package_name + ": Rendering " + str(len(content_data_node)) + " slides into raw data.")
    for slide_item in content_data_node:
        slide_title = render_slide_name(package_export_content_modules, values, slide_item)
        if D_STR in content_data_node[slide_item]:
            check_dic = content_data_node[slide_item][D_STR][DOC_STR][NODES]
            render_slide_data = render_slide(check_dic)
            if render_slide_data:
                raw_data += f"# {slide_title}{render_slide_data}{NEW_LINE}"
    return raw_data, package_name


def render_slide_name(package_export_content_modules, values, slide_item):
    slide_title = None
    if EXPORT_TASKS in package_export_content_modules[values]:
        slide_title = package_export_content_modules[values][EXPORT_TASKS][slide_item]['title']
    elif QUESTION_DESC in package_export_content_modules[values]:
        slide_title = package_export_content_modules[values][QUESTION_DESC][slide_item]

    return slide_title


def get_slide_data_listed(package_export_content_modules: dict, values: str):
    """Return raw data from package and package name."""
    package_value = package_export_content_modules[values][EXPORT_MOD_STRING]
    package_name = package_value[N_STR]
    raw_data_dict = {package_name: {}}
    content_data_node = package_export_content_modules[values][QUESTION_DESC]
    for slide_item in content_data_node:
        slide_title = render_slide_name(package_export_content_modules, values, slide_item)
        info(package_name + ": Rendering " + str(len(content_data_node)) + " slides into raw data.")
        if content_data_node[slide_item]:
            if D_STR in content_data_node[slide_item]:
                check_dic = content_data_node[slide_item][D_STR][DOC_STR][NODES]
                render_slide_data = render_slide(check_dic)
                if render_slide_data:
                    raw_data_dict[package_name][slide_title] = render_slide_data
    task_data_node = package_export_content_modules[values][TASK_DESC]
    for slide_item in task_data_node:
        slide_title = render_slide_name(package_export_content_modules, values, slide_item)
        info(package_name + ": Rendering " + str(len(task_data_node)) + " slides into raw data.")
        if task_data_node[slide_item]:
            if D_STR in task_data_node[slide_item]:
                check_dic = task_data_node[slide_item][D_STR][DOC_STR][NODES]
                render_slide_data = render_slide(check_dic)
                if render_slide_data:
                    raw_data_dict[package_name][slide_title] = render_slide_data
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
        cep_check_result = cep_check_message(cep_item_dict[cep_items][CEP_NUM])
        if cep_item_dict[cep_items][CEP_TYPE_CHECK] is QUESTION_DESC:
            if STR_SEARCH in cep_item_dict[cep_items]:
                cep_check_result = f"{package_name}: CEP {cep_item_dict[cep_items][CEP_NUM]} - Passed"
            if RE_SEARCH in cep_item_dict[cep_items]:
                test_search = cep_item_dict[cep_items][RE_SEARCH]
                x = re.findall(test_search, raw_slide_data)
                if len(x) > 0:
                    cep_check_result = f"{package_name}: CEP {cep_item_dict[cep_items][CEP_NUM]} - Passed"
            if cep_check_result:
                if "Passed" not in cep_check_result:
                    error(f"{package_name}: {cep_check_result}")
                else:
                    info(cep_check_result)


def render_list_item(slide_line: dict, heading_level: str):
    """Return formatted list data."""
    raw_list_data = ""
    for node in slide_line:
        raw_list_data += f"{heading_level}{node[TXT]}"
    if len(heading_level) == len(raw_list_data):
        return None
    return raw_list_data


def render_nested_list_nodes(slide_line: dict, format_string: str, list_type: str):
    """Return raw list data from nested node data."""
    raw_list_data = ""
    order_count = 0
    for node in slide_line:
        order_count += 1
        if TXT in node:
            if list_type is UNORDERED_STR:
                raw_list_data += f"   * {node[TXT]}{NEW_LINE}"
            elif list_type is ORDERED_STR:
                raw_list_data += f"{str(order_count)}. {node[TXT]}{NEW_LINE}"
        else:
            for nested_node in node[NODES]:
                if TXT in nested_node:
                    raw_list_data += f"{format_string}{nested_node[TXT]}{NEW_LINE}"
                else:
                    if TXT in nested_node[NODES][0]:
                        if list_type is UNORDERED_STR:
                            raw_list_data += f"   * {nested_node[NODES][0][TXT]}{NEW_LINE}"
                        elif list_type is ORDERED_STR:
                            raw_list_data += f"{str(order_count)}. {nested_node[NODES][0][TXT]}{NEW_LINE}"
    return raw_list_data


def render_slide(slide_dict: dict):
    """Return string data from content module slide data."""
    raw_slide_data = ""
    if slide_dict:
        for slide_line in slide_dict:
            raw_slide_data += NEW_LINE
            if TYPE_STRING in slide_line:
                if 'paragraph' in slide_line[TYPE_STRING]:
                    if "marks" in slide_line[NODES][0] and len(slide_line[NODES][0][M_STR]) > 0:
                        if "bold" == slide_line[NODES][0][M_STR][0][TYPE_STRING]:
                            if len(slide_line[NODES][0][TXT]) > 0:
                                raw_slide_data += f"***{strip_end_space(slide_line[NODES][0][TXT])[:-1]}***"
                        elif 'code-mark' == slide_line[NODES][0][M_STR][0][TYPE_STRING]:
                            raw_slide_data += f"`{strip_end_space(slide_line[NODES][0][TXT])}`"
                        elif 'strikethrough' == slide_line[NODES][0][M_STR][0][TYPE_STRING]:
                            raw_slide_data += f"~~{strip_end_space(slide_line[NODES][0][TXT])}~~"
                        elif 'underline' == slide_line[NODES][0][M_STR][0][TYPE_STRING]:
                            raw_slide_data += f"__{strip_end_space(slide_line[NODES][0][TXT])}__"
                        else:
                            error(f"Missing type parsing for value: {str(slide_line[NODES][0][M_STR][0][TYPE_STRING])}")
                    else:
                        raw_slide_data += slide_line[NODES][0][TXT]
                elif 'unordered-list' in slide_line[TYPE_STRING]:
                    raw_list_data = render_nested_list_nodes(slide_line[NODES], "   * ",  UNORDERED_STR)
                    if len(raw_list_data) > 0:
                        raw_slide_data += raw_list_data
                elif 'ordered-list' in slide_line[TYPE_STRING]:
                    raw_list_data = render_nested_list_nodes(slide_line[NODES], "  ", ORDERED_STR)
                    if len(raw_list_data) > 0:
                        raw_slide_data += raw_list_data
                elif 'list-item-child' in slide_line[TYPE_STRING]:
                    raw_list_data = render_nested_list_nodes(slide_line[NODES], "   * ",  UNORDERED_STR)
                    if len(raw_list_data) > 0:
                        raw_slide_data += raw_list_data
                elif 'heading-two' in slide_line[TYPE_STRING]:
                    raw_heading_data = render_list_item(slide_line[NODES], '### ')
                    if raw_heading_data:
                        raw_slide_data += raw_heading_data
                elif 'heading-one' in slide_line[TYPE_STRING]:
                    raw_heading_data = render_list_item(slide_line[NODES], '## ')
                    if raw_heading_data:
                        raw_slide_data += raw_heading_data
                elif 'bold' in slide_line[TYPE_STRING]:
                    raw_heading_data = render_list_item(slide_line[NODES], '***')
                    raw_heading_data += "***"
                    if raw_heading_data:
                        raw_slide_data += raw_heading_data
                elif 'italic' in slide_line[TYPE_STRING]:
                    raw_heading_data = render_list_item(slide_line[NODES], '*')
                    raw_heading_data += "*"
                    if raw_heading_data:
                        raw_slide_data += raw_heading_data
                elif 'image-block' in slide_line[TYPE_STRING]:
                    picture_id = id_generator()
                    raw_heading_data = f"![{picture_id}]({slide_line[D_STR]['imageData']})"
                    if raw_heading_data:
                        raw_slide_data += raw_heading_data
                elif 'code-block' in slide_line[TYPE_STRING]:
                    raw_heading_data = render_nested_list_nodes(slide_line[NODES], "    ", UNORDERED_STR)
                    if raw_heading_data:
                        raw_slide_data += raw_heading_data
                elif 'code-line' in slide_line[TYPE_STRING]:
                    raw_heading_data = render_nested_list_nodes(slide_line[NODES], "\n     ", UNORDERED_STR)
                    if raw_heading_data and len(raw_heading_data) > 5:
                        raw_slide_data += raw_heading_data
                else:
                    error(f"Data type {slide_line[TYPE_STRING]} unknown")
                    raw_slide_data += " Data Type Unknown\n"
            raw_slide_data += NEW_LINE
            
    return raw_slide_data


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


def package_export_package_info(raw_data):
    package_dict = PackageExport(raw_data[PACKAGE_STR])
    package_data = {}
    for data_value, value in package_dict.to_dict().items():
        if value:
            package_data[data_value] = value
    return package_data
