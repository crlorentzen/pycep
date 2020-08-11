"""Pycep plugin function library."""
# coding=utf-8
import re
import random
import string
from os import mkdir
from shutil import rmtree
from logging import info, error
from yaml_info.yamlinfo import YamlInfo
from pycep.render import write_to_file
from pycep.model import get_value, strip_unsafe_file_names, strip_end_space, h_one_format, DIR_CHARACTER, \
    ModuleExportContentModule, AnswerKey, PackageExport, extract_tar_data, get_task_markdown_data
from pycep.content_strings import *


def get_task_data(package_export_content_modules: dict,
                  values: str):
    """Return raw data from package and package name."""
    package_data = package_export_content_modules[values]
    package_value = package_data[EXPORT_MOD_STRING]
    package_name = package_value[N_STR]
    raw_data = ""
    content_data_node = package_data[QUESTION_DESC]
    info(package_name + ": Rendering " + str(len(content_data_node)) + " tasks into raw data.")
    for task_item in content_data_node:
        task_title = render_task_name(package_export_content_modules, values, task_item)
        if D_STR in content_data_node[task_item]:
            check_dic = content_data_node[task_item][D_STR][DOC_STR][NODES]
            render_task_data = render_task(check_dic)
            if render_task_data:
                raw_data += f"# {task_title}{render_task_data}{NEW_LINE}"
    return raw_data, package_name


def return_non_data_task(input_data: dict) -> dict:
    """Return structured data dict."""
    package_export_content_modules = get_value(CONTENT_MOD_STRING, input_data)[CONTENT_MOD_STRING]
    task_dict = {}
    for values in package_export_content_modules:
        raw_task_data = get_task_data_listed(package_export_content_modules, values)
        for package in raw_task_data:
            task_dict[package] = {}
            for titles, task_item in raw_task_data[package].items():
                task_dict[package][titles] = {}
                line_count = 0
                line_item = task_item.split("\n")
                for task_line_item in line_item:
                    line_count += 1
                    test_search = "data:image\/\S{1,4};base64"
                    x = re.findall(test_search, task_line_item)
                    if len(x) < 1 < len(task_line_item):
                        task_dict[package][titles][line_count] = task_line_item

    return task_dict


def render_task_name(package_export_content_modules: dict,
                     values: str,
                     task_item: str):
    task_title = None
    if EXPORT_TASKS in package_export_content_modules[values]:
        task_title = package_export_content_modules[values][EXPORT_TASKS][task_item]['title']
    elif QUESTION_DESC in package_export_content_modules[values]:
        task_title = package_export_content_modules[values][QUESTION_DESC][task_item]

    return task_title


def get_task_data_listed(package_export_content_modules: dict,
                         values: str):
    """Return raw data from package and package name."""
    package_value = package_export_content_modules[values][EXPORT_MOD_STRING]
    package_name = package_value[N_STR]
    raw_data_dict = {package_name: {}}
    content_data_node = package_export_content_modules[values][QUESTION_DESC]
    for task_item in content_data_node:
        task_title = render_task_name(package_export_content_modules, values, task_item)
        info(package_name + ": Rendering " + str(len(content_data_node)) + " tasks into raw data.")
        if content_data_node[task_item]:
            if D_STR in content_data_node[task_item]:
                check_dic = content_data_node[task_item][D_STR][DOC_STR][NODES]
                render_task_data = render_task(check_dic)
                if render_task_data:
                    raw_data_dict[package_name][task_title] = render_task_data
    task_data_node = package_export_content_modules[values][TASK_DESC]
    for task_item in task_data_node:
        task_title = render_task_name(package_export_content_modules, values, task_item)
        info(package_name + ": Rendering " + str(len(task_data_node)) + " tasks into raw data.")
        if task_data_node[task_item]:
            if D_STR in task_data_node[task_item]:
                check_dic = task_data_node[task_item][D_STR][DOC_STR][NODES]
                render_task_data = render_task(check_dic)
                if render_task_data:
                    raw_data_dict[package_name][task_title] = render_task_data
    return raw_data_dict


def id_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def render_list_item(task_line: dict,
                     heading_level: str):
    """Return formatted list data."""
    raw_list_data = ""
    for node in task_line:
        raw_list_data += f"{heading_level}{node[TXT]}"
        if "## " in raw_list_data[2:]:
            test_data = raw_list_data[2:].replace("## ", "__")
            test_data = test_data.replace("##", "__")
            raw_list_data = f"{heading_level}{test_data}"
    if len(heading_level) == len(raw_list_data):
        return None
    return raw_list_data


def render_nested_list_nodes(task_line: dict,
                             format_string: str,
                             list_type: str):
    """Return raw list data from nested node data."""
    raw_list_data = ""
    order_count = 0
    for node in task_line:
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


def render_paragraph_data(paragraph_item: dict,
                          count: int,
                          task_line: dict):
    raw_task_data = ""
    if "marks" in paragraph_item and len(paragraph_item[M_STR]) > 0:
        item_type = paragraph_item[M_STR][0][TYPE_STRING]
        item_text = paragraph_item[TXT]
        if "bold" == paragraph_item[M_STR][0][TYPE_STRING]:
            if len(paragraph_item[TXT]) > 0:
                raw_task_data += f"**{strip_end_space(item_text)}** "
        elif 'code-mark' == item_type:
            raw_task_data += f"`{strip_end_space(item_text)}` "
        elif 'strikethrough' == item_type:
            raw_task_data += f"~~{strip_end_space(item_text)}~~ "
        elif 'underline' == item_type:
            raw_task_data += f"__{strip_end_space(item_text)}__ "
        elif 'italic' == item_type:
            raw_task_data += f"*{strip_end_space(item_text)}* "
        else:
            error(f"Missing type parsing for value: {str(item_text)}")
    else:
        if TXT in task_line[NODES][count]:
            raw_task_data += task_line[NODES][count][TXT]
        elif "data" in task_line[NODES][count]:
            if task_line[NODES][count][TYPE_STRING] == "link":
                raw_task_data += f"<{task_line[NODES][count][NODES][0][TXT]}>"
            else:
                error(f"Unknown Data Format not being processed properly {task_line[NODES][count][TYPE_STRING]}")
    return raw_task_data


def render_task(task_dict: dict):
    """Return string data from content module task data."""
    raw_task_data = ""
    if task_dict:
        for task_line in task_dict:
            raw_task_data += NEW_LINE
            if TYPE_STRING in task_line:
                if 'paragraph' in task_line[TYPE_STRING]:
                    if "marks" in task_line[NODES][0] and len(task_line[NODES][0][M_STR]) > 0:
                        if "bold" == task_line[NODES][0][M_STR][0][TYPE_STRING]:
                            if len(task_line[NODES][0][TXT]) > 0:
                                raw_task_data += f"**{strip_end_space(task_line[NODES][0][TXT])}**"
                        elif 'code-mark' == task_line[NODES][0][M_STR][0][TYPE_STRING]:
                            raw_task_data += f"`{strip_end_space(task_line[NODES][0][TXT])}`"
                        elif 'strikethrough' == task_line[NODES][0][M_STR][0][TYPE_STRING]:
                            raw_task_data += f"~~{strip_end_space(task_line[NODES][0][TXT])}~~"
                        elif 'underline' == task_line[NODES][0][M_STR][0][TYPE_STRING]:
                            raw_task_data += f"__{strip_end_space(task_line[NODES][0][TXT])}__"
                        elif 'italic' == task_line[NODES][0][M_STR][0][TYPE_STRING]:
                            raw_task_data += f"*{strip_end_space(task_line[NODES][0][TXT])}*"
                        else:
                            error(f"Missing type parsing for value: {str(task_line[NODES][0][M_STR][0][TYPE_STRING])}")
                    else:
                        count = 0
                        for paragraph_item in task_line[NODES]:
                            raw_task_data += render_paragraph_data(paragraph_item, count, task_line)
                            count += 1
                elif 'unordered-list' in task_line[TYPE_STRING]:
                    raw_list_data = render_nested_list_nodes(task_line[NODES], "   * ", UNORDERED_STR)
                    if len(raw_list_data) > 0:
                        raw_task_data += raw_list_data
                elif 'ordered-list' in task_line[TYPE_STRING]:
                    raw_list_data = render_nested_list_nodes(task_line[NODES], "  ", ORDERED_STR)
                    if len(raw_list_data) > 0:
                        raw_task_data += raw_list_data
                elif 'list-item-child' in task_line[TYPE_STRING]:
                    raw_list_data = render_nested_list_nodes(task_line[NODES], "   * ", UNORDERED_STR)
                    if len(raw_list_data) > 0:
                        raw_task_data += raw_list_data
                elif 'heading-two' in task_line[TYPE_STRING]:
                    raw_heading_data = render_list_item(task_line[NODES], '### ')
                    if raw_heading_data:
                        raw_task_data += raw_heading_data
                elif 'heading-one' in task_line[TYPE_STRING]:
                    raw_heading_data = render_list_item(task_line[NODES], '## ')
                    if raw_heading_data:
                        raw_task_data += raw_heading_data
                elif 'underline' in task_line[TYPE_STRING]:
                    raw_heading_data = render_list_item(task_line[NODES], '__')
                    raw_heading_data += "__"
                    if raw_heading_data:
                        raw_task_data += raw_heading_data
                elif 'bold' in task_line[TYPE_STRING]:
                    raw_heading_data = render_list_item(task_line[NODES], '**')
                    raw_heading_data += "**"
                    if raw_heading_data:
                        raw_task_data += raw_heading_data
                elif 'italic' in task_line[TYPE_STRING]:
                    raw_heading_data = render_list_item(task_line[NODES], '*')
                    raw_heading_data += "*"
                    if raw_heading_data:
                        raw_task_data += raw_heading_data
                elif 'image-block' in task_line[TYPE_STRING]:
                    picture_id = id_generator()
                    raw_heading_data = f"![{picture_id}]({task_line[D_STR]['imageData']})"
                    if raw_heading_data:
                        raw_task_data += raw_heading_data
                elif 'code-block' in task_line[TYPE_STRING]:
                    raw_heading_data = render_nested_list_nodes(task_line[NODES], "    ", UNORDERED_STR)
                    if raw_heading_data:
                        raw_task_data += raw_heading_data
                elif 'code-line' in task_line[TYPE_STRING]:
                    raw_heading_data = render_nested_list_nodes(task_line[NODES], "\n     ", UNORDERED_STR)
                    if raw_heading_data and len(raw_heading_data) > 5:
                        raw_task_data += raw_heading_data
                else:
                    error(f"Data type {task_line[TYPE_STRING]} unknown")
                    raw_task_data += " Data Type Unknown\n"
            raw_task_data += NEW_LINE
    return raw_task_data


def get_package_data(package_export_content_modules: dict):
    package_list = []
    for module in package_export_content_modules:
        pck_name = strip_unsafe_file_names(package_export_content_modules[module][EXPORT_MOD_STRING]['name'])
        package_list.append(pck_name)
    return package_list


def yml_format_str(answer_data, task_item, attachment_data):
    task_answer_key = None
    for title in answer_data.items():
        search_title = title[1]['title']
        if search_title is task_item:
            task_answer_key = AnswerKey(raw_data=title[1], attachment_data=attachment_data, task=title[0]).to_yml()
            task_answer_key = task_answer_key.replace("True", "true")
            task_answer_key = task_answer_key.replace("False", "false")
    return task_answer_key


def package_export_package_info(raw_data: dict):
    package_dict = PackageExport(raw_data[PACKAGE_STR])
    package_data = {}
    for data_value, value in package_dict.to_dict().items():
        if value:
            package_data[data_value] = value
    return package_data


def parser(raw_data: dict,
           output: str,
           input_file: str):
    """Output package to md format."""
    package_export_content_modules = get_value(CONTENT_MOD_STRING, raw_data)[CONTENT_MOD_STRING]
    package_data = get_package_data(package_export_content_modules)
    main_package_data = package_export_package_info(raw_data)
    file_name = f"{strip_unsafe_file_names(main_package_data[N_STR].strip(' '))}{YAML_EXT}"
    raw_data[PACKAGE_STR][CONTENT_MODS] = package_data
    package_yml = PackageExport(raw_data[PACKAGE_STR]).to_yml()
    write_to_file(f"{output}{DIR_CHARACTER}{file_name}", package_yml)
    extract_tar_data(input_file, output)
    for values in package_export_content_modules:
        raw_task_data = get_task_data_listed(package_export_content_modules, values)
        info("Processing tasks with compile plugin now!")
        attachment_data = package_export_content_modules[values][CONTENT_MOD_EXPORT_TASK_ATTACHMENTS]
        answer_data = package_export_content_modules[values][EXPORT_TASKS]
        for package in raw_task_data:
            package_name_value = strip_unsafe_file_names(package)
            package_path = f"{output}{DIR_CHARACTER}{package_name_value}{DIR_CHARACTER}"
            try:
                mkdir(package_path)
            except FileExistsError:
                rmtree(package_path)
                mkdir(package_path)
            write_to_file(f"{package_path}module.yml",
                          ModuleExportContentModule(package_export_content_modules[values]).to_yml())
            module_task_yml = ""
            module_task_md = ""
            for task_item in raw_task_data[package]:
                task_answer_key = yml_format_str(answer_data, task_item, attachment_data)
                module_task_md += (h_one_format(task_item) + raw_task_data[package][task_item]) + "\n"
                if task_answer_key:
                    module_task_yml += task_answer_key
            tasks_path = f"{package_path}tasks.md"
            write_to_file(tasks_path, module_task_md)
            tasks_answer_key_path = f"{package_path}tasks.yml"
            write_to_file(tasks_answer_key_path, module_task_yml)
            with open(tasks_path, 'r') as task_markdown_data:
                ordered_markdown_data = task_markdown_data.read()
            module_config_yaml = YamlInfo(f"{package_path}module.yml", "none", "none").get()
            fixed_order = ""
            if "tasks" in module_config_yaml:
                for tasks in module_config_yaml["tasks"]:
                    if isinstance(tasks, list):
                        for task in tasks:
                            fixed_order += f"# {task}{NEW_LINE}"
                            fixed_order += f"{get_task_markdown_data(ordered_markdown_data, task)}{BREAK_LINE}{NEW_LINE}"
                    else:
                        fixed_order += f"# {tasks}{NEW_LINE}"
                        fixed_order += f"{get_task_markdown_data(ordered_markdown_data, tasks)}{BREAK_LINE}{NEW_LINE}"
            with open(tasks_path, 'w') as fixed_markdown:
                fixed_markdown.write(fixed_order)
