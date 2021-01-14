"""The pycep model library."""
# coding=utf-8
import platform
import tarfile
from base64 import b64encode
from glob import glob
from shutil import rmtree, move, Error
from uuid import uuid4
from json import dumps
from os import mkdir, chdir, walk, getcwd, remove
from logging import error, info
from yaml_info.yamlinfo import YamlInfo
from pycep.content_strings import *

DIR_CHARACTER = "/"
SYSTEM_PLATFORM = platform.system()
if SYSTEM_PLATFORM == "Windows":
    info("Windows Detected")
    DIR_CHARACTER = "\\"
elif SYSTEM_PLATFORM not in ["Linux", "Darwin"]:
    error(f"Unsupported System type detected")
NEW_LINE = "\n"


def build_node_type(node_type):
    return {"data": {},
            "object": "mark",
            "type": node_type}


def build_text_line(line_data):
    data_nodes = {"text": line_data,
                  "object": "text",
                  "marks": []
                  }
    return data_nodes


def check_string(string_data, match_value):
    if string_data[:len(match_value)] == match_value and string_data[-len(match_value):] == match_value:
        return string_data[len(match_value):-len(match_value)]
    return None


def build_mark(line_data):
    build_line = ""
    mark_list = []
    new_test = line_data.split(" ")
    new_string = ""
    for item in new_test:
        test = check_string(item, "**")
        if test:
            new_data = build_text_line(new_string)
            mark_list.append(new_data)
            new_bold_item = build_text_line(test)
            new_bold_item["marks"] = [build_node_type("bold")]
            mark_list.append(new_bold_item)
            new_string = ""
        else:
            test_italic = check_string(item, "*")
            if test_italic:
                new_data = build_text_line(new_string)
                mark_list.append(new_data)
                new_italic_item = build_text_line(test_italic)
                new_italic_item["marks"] = [build_node_type("italic")]
                mark_list.append(new_italic_item)
                new_string = ""
            else:
                test_underscore = check_string(item, "__")
                if test_underscore:
                    new_data = build_text_line(new_string)
                    mark_list.append(new_data)
                    new_underscore_item = build_text_line(test_underscore)
                    new_underscore_item["marks"] = [build_node_type("underline")]
                    mark_list.append(new_underscore_item)
                    new_string = ""
                else:
                    test_code = check_string(item, "`")
                    if test_code:
                        new_data = build_text_line(new_string)
                        mark_list.append(new_data)
                        new_code_item = build_text_line(test_code)
                        new_code_item["marks"] = [build_node_type("code-mark")]
                        mark_list.append(new_code_item)
                        new_string = ""
                    else:
                        test_strikethrough = check_string(item, "~~")
                        if test_strikethrough:
                            new_data = build_text_line(new_string)
                            mark_list.append(new_data)
                            new_strikethrough_item = build_text_line(test_strikethrough)
                            new_strikethrough_item["marks"] = [build_node_type("strikethrough")]
                            mark_list.append(new_strikethrough_item)
                            new_string = ""
                        else:
                            new_string += f"{item} "
    mark_list.append(build_text_line(new_string))
    return mark_list


def build_node_package(nodes_data: list, data_type: str):
    data_node = {"data": {},
                 "object": "block",
                 "type": data_type,
                 "nodes": nodes_data,
                 }
    return data_node


def path_builder(build_path, delete):
    """Create directory with build_path variable."""
    try:
        mkdir(build_path)
    except FileExistsError:
        if delete:
            rmtree(build_path)
            mkdir(build_path)
    except FileNotFoundError:
        if delete:
            rmtree(f"{build_path}")
        mkdir(f"{build_path}")


def get_task_markdown_data(markdown_data: str,
                           task: str):
    """Return task data from markdown structure."""
    task_data = ""
    task_file = 0
    for line_data in markdown_data.splitlines():
        line_chunk = line_data[2:]
        line_search = line_data[:2]

        if line_chunk == task:
            task_file = 1
        elif line_search == "# ":
            task_file = 0
        else:
            if task_file == 1 and line_data != BREAK_LINE:
                task_data += line_data + "\n"
    return task_data


def search_string(string_value, value_1, value_2):
    """Return search list result."""
    start_string = ""
    end_string = ""
    middle_string = ""
    start_true = True
    end_true = False
    middle_true = False
    search_list = []
    for character in string_value:
        if value_1 == character:
            start_true = False
            middle_true = True
        elif value_2 == character:
            middle_true = False
            end_true = True
        elif start_true:
            start_string += character
        elif middle_true:
            middle_string += character
        elif end_true:
            end_string += character
    search_list.append(start_string)
    search_list.append(middle_string)
    search_list.append(end_string)
    return search_list


def render_link_chunk(task_list_items, line_data, star_list, code_list):
    """Return formatted line chunk for a task."""
    line_chunks = search_string(line_data, "<", ">")
    count = 0
    for line_chunk_value in line_chunks:
        count += 1
        line_chunk = line_chunk_value[:4]
        if count == 2:
            if len(line_chunk_value) > 0:
                url_dict = {D_STR: {"url": line_chunk_value},
                            "object": "inline",
                            "type": "link",
                            "nodes": build_mark(line_chunk_value)}
                task_list_items[0]["nodes"].append(url_dict)
        elif line_chunk == "### ":
            task_list_items.append(build_node_package([build_text_line(line_chunk_value[4:])], "heading-two"))
        elif line_chunk == "   -":
            star_list.append(build_node_package([build_node_package([build_text_line(line_chunk_value[5:])],
                                                                "list-item-child")], "list-item"))
        elif line_chunk == "   *":
            star_list.append(build_node_package([build_node_package([build_text_line(line_chunk_value[5:])],
                                                                "list-item-child")], "list-item"))
        elif line_chunk == "    ":
            code_list.append(build_node_package([build_text_line(f"{line_chunk_value[4:]}\r")], "code-line"))
        elif line_chunk[:-1] == "## ":
            task_list_items.append(build_node_package([build_text_line(line_chunk_value[3:])], "heading-one"))
        elif line_chunk[:-2] == "**":
            task_list_items.append(build_node_package([build_text_line(line_chunk_value[2:-2])], "bold"))
        elif line_chunk[:-2] == "![":
            image_data = build_node_package([build_text_line("")], "image-block")
            image_data["data"] = {"imageData": line_chunk_value[10:-1]}
            task_list_items.append(image_data)
        elif len(code_list) > 0:
            task_list_items.append(build_node_package(code_list, "code-block"))
            code_list = []
        elif len(star_list) > 0:
            task_list_items.append(build_node_package(star_list, "unordered-list"))
            star_list = []
        elif len(line_data) > 0:
            task_list_items.append(build_node_package(build_mark(line_chunk_value), "paragraph"))
    return task_list_items, line_data, star_list, code_list


def compile_package_data(package_export_name: str,
                         input_dir: str,
                         export_dir: str):
    """Compile export package with input package/module directory."""
    package_dir = input_dir
    dir_paths = package_dir.split(f"{DIR_CHARACTER}")
    total_length = len(dir_paths)
    package_name = dir_paths[(total_length - 1)]
    input_package_export_name = package_export_name
    package_config_path = f"{input_dir}{DIR_CHARACTER}{package_name}.yml"
    package_config_yaml = YamlInfo(package_config_path, "none", "none").get()
    build_json = {}
    build_json[PACKAGE_STR] = {}
    build_json[PACKAGE_STR] = package_config_yaml
    build_json['packageKey'] = str(uuid4())
    package_path = f"{export_dir}{DIR_CHARACTER}{package_name}"
    try:
        mkdir(f"{package_path}")
    except FileNotFoundError:
        mkdir(f"{export_dir}")
        mkdir(f"{package_path}")
    except FileExistsError:
        rmtree(f"{package_path}")
        mkdir(f"{package_path}")
    mkdir(f"{package_path}{DIR_CHARACTER}content-modules")
    file_list = package_config_yaml["contentModules"]
    package_config_yaml[CONTENT_MODS] = []
    build_json[CONTENT_MOD_STRING] = {}
    for file_name in file_list:
        task_task_exports = {}
        attachment_data_dict = {}
        mod_config_path = f"{input_dir}{DIR_CHARACTER}{file_name}{DIR_CHARACTER}module.yml"
        module_config_yaml = YamlInfo(mod_config_path, "none", "none").get()
        task_info_dict = {}
        question_data = {}
        questions_descriptions = {}
        task_task_list = []
        module_id = str(uuid4())
        module_id_string = f"{module_id}"
        content_module_path = f"{package_path}{DIR_CHARACTER}content-modules"
        module_path = f"{content_module_path}{DIR_CHARACTER}module-{module_id_string}"
        attachment_build_path = f"{module_path}{DIR_CHARACTER}attachments{DIR_CHARACTER}"
        test_build = YamlInfo(f"{input_dir}{DIR_CHARACTER}{file_name}{DIR_CHARACTER}tasks.yml", "none", "none").get()
        with open(f"{input_dir}{DIR_CHARACTER}{file_name}{DIR_CHARACTER}tasks.md", 'r') as markdown_data_file:
            module_markdown_data = markdown_data_file.read()
        if "tasks" in module_config_yaml:
            for tasks in module_config_yaml["tasks"]:
                sub_task_list = []
                if isinstance(tasks, list):
                    for task in tasks:
                        task_id = str(uuid4())
                        task_id_string = f"task-{task_id}"
                        task_dict = test_build[task]
                        if "vmKeys" not in task_dict:
                            task_dict["vmKeys"] = []
                        else:
                            vm_list = []
                            for vm in task_dict["vmKeys"]:
                                vm_list.append({'key': {'repetitionGroup': task_dict["vmKeys"][vm]['ID'],
                                                        'index': task_dict["vmKeys"][vm]['index']}, 'val': vm})
                            task_dict["vmKeys"] = vm_list
                        if "attachments" in task_dict:
                            del task_dict["attachments"]
                        if "answers" in task_dict:
                            question_list = task_dict["answers"]
                            tasks_dict = {}
                            tasks_dict["questions"] = {}
                            choices = []
                            true_str = "true"
                            false_str = "false"
                            for correct in question_list["correct"]:
                                choices.append({'value': correct, 'correct': True})
                            if "incorrect" in question_list:
                                for wrong in question_list["incorrect"]:
                                    choices.append({'value': wrong, 'correct': False})
                            hints = []
                            if "hints" in task_dict:
                                if task_dict["hints"]:
                                    for hint in task_dict["hints"]:
                                        hints.append({'text': task_dict["hints"][hint]["message"],
                                                      'pointsDeduction': task_dict["hints"][hint]["cost"]})
                                    del task_dict["hints"]
                            tasks_dict["questions"]["choices"] = choices
                            tasks_dict["questions"]["hints"] = hints
                            tasks_dict["questions"]["retryCount"] = task_dict["retrycount"]
                            tasks_dict["questions"]["type"] = task_dict["type"]
                            tasks_dict["questions"]["points"] = task_dict["pointtotal"]
                            tasks_dict["questions"]["extraData"] = {}
                            tasks_dict["questions"]["mappingTags"] = []
                            if "mappingtags" in task_dict:
                                tasks_dict["questions"]["mappingTags"] = task_dict['mappingtags']
                            else:
                                tasks_dict["questions"]["mappingTags"] = []
                            if "extradata" in task_dict:
                                tasks_dict["questions"]["extraData"] = {}
                                del task_dict["extradata"]
                            else:
                                tasks_dict["questions"]["extraData"] = {}
                            task_dict["question"] = tasks_dict["questions"]
                            del task_dict["answers"]
                            del task_dict["type"]
                            del task_dict["pointtotal"]
                            del task_dict["retrycount"]
                        if "question" in task_dict:
                            custom_task_dict = {"vmKeys": task_dict["vmKeys"],
                                                "title": task,
                                                "question": task_dict["question"]}
                        else:
                            if "vmKeys" in task_dict:
                                custom_task_dict = {"vmKeys": task_dict["vmKeys"], "title": task}
                            else:
                                custom_task_dict = {"vmKeys": [], "title": task}
                        sub_task_list.append({"key": task_id_string, "val": custom_task_dict})
                        task_task_exports[task_id_string] = custom_task_dict
                        task_info_dict[task_id_string] = get_task_markdown_data(module_markdown_data, task)
                        attachment_data_dict[task_id_string] = {}
                    task_task_list.append(sub_task_list)
                else:
                    task_id = str(uuid4())
                    task_id_string = f"task-{task_id}"
                    task_dict = test_build[tasks]
                    if "vmKeys" not in task_dict:
                        task_dict["vmKeys"] = []
                    else:
                        vm_list = []
                        for vm in task_dict["vmKeys"]:
                            vm_list.append({'key': {'repetitionGroup': task_dict["vmKeys"][vm]['ID'],
                                                    'index': task_dict["vmKeys"][vm]['index']}, 'val': vm})
                        task_dict["vmKeys"] = vm_list
                    if "answers" in task_dict:
                        question_list = task_dict["answers"]
                        tasks_dict = {}
                        tasks_dict["questions"] = {}
                        choices = []
                        true_str = "true"
                        false_str = "false"
                        for correct in question_list["correct"]:
                            choices.append({'value': correct, 'correct': True})
                        if "incorrect" in question_list:
                            for wrong in question_list["incorrect"]:
                                choices.append({'value': wrong, 'correct': False})
                        hints = []
                        if "hints" in task_dict:
                            if task_dict["hints"]:
                                for hint in task_dict["hints"]:
                                    hints.append({'text': task_dict["hints"][hint]["message"],
                                                  'pointsDeduction': task_dict["hints"][hint]["cost"]})
                                del task_dict["hints"]
                        tasks_dict["questions"]["choices"] = choices
                        tasks_dict["questions"]["hints"] = hints
                        tasks_dict["questions"]["retryCount"] = task_dict["retrycount"]
                        tasks_dict["questions"]["type"] = task_dict["type"]
                        tasks_dict["questions"]["points"] = task_dict["pointtotal"]
                        tasks_dict["questions"]["extraData"] = {}
                        tasks_dict["questions"]["mappingTags"] = []
                        if "mappingtags" in task_dict:
                            tasks_dict["questions"]["mappingTags"] = task_dict['mappingtags']
                        else:
                            tasks_dict["questions"]["mappingTags"] = []
                        if "extradata" in task_dict:
                            tasks_dict["questions"]["extraData"] = {}
                            del task_dict["extradata"]
                        else:
                            tasks_dict["questions"]["extraData"] = {}
                        task_dict["question"] = tasks_dict["questions"]
                        del task_dict["answers"]
                        del task_dict["type"]
                        del task_dict["pointtotal"]
                        del task_dict["retrycount"]
                    if "mappingtags" in task_dict:
                        del task_dict["mappingtags"]
                    if "extradata" in task_dict:
                        del task_dict["extradata"]
                    attachment_list = 0
                    if "question" in task_dict:
                        custom_task_dict_sub = {"vmKeys": task_dict["vmKeys"], "title": tasks,
                                                "question": task_dict["question"]}
                    else:
                        custom_task_dict_sub = {"vmKeys": task_dict["vmKeys"], "title": tasks}
                    task_task_exports[task_id_string] = custom_task_dict_sub
                    if "attachments" in task_dict:
                        attachment_list = len(task_dict["attachments"])
                    attachment_data_dict[task_id_string] = {}
                    path_builder(content_module_path, False)
                    path_builder(module_path, False)
                    path_builder(attachment_build_path, False)
                    attachment_data_dict[task_id_string] = {}
                    if attachment_list > 0:
                        for attachment in task_dict["attachments"]:
                            attachment_uuid = str(uuid4())
                            # TODO update this to support more than just pdf files
                            attachment_data_dict[task_id_string][attachment_uuid] = \
                                {"attachmentMetaContentType": "application/pdf",
                                 "attachmentMetaKey": attachment_uuid,
                                 "attachmentMetaName": attachment
                                 }
                            file_safe_attachment = attachment.replace(" ", "%20")
                            try:
                                read_file = \
                                    f"{input_dir}{DIR_CHARACTER}attachments{DIR_CHARACTER}{file_safe_attachment}"
                                with open(read_file, 'rb') \
                                        as module_file:
                                    module_data = module_file.read()
                                    attachment_path = f"{attachment_build_path}{attachment_uuid}"
                                    path_builder(attachment_path, False)
                                    with open(f'{attachment_path}{DIR_CHARACTER}{file_safe_attachment}', 'wb') \
                                            as module_file_data:
                                        module_file_data.write(module_data)
                            except FileNotFoundError:
                                error("Attachment data misconfig, attachment not found")
                    else:
                        attachment_data_dict[task_id_string] = {}
                    if "question" in task_dict:
                        custom_task_dict_main = {"vmKeys": task_dict["vmKeys"], "title": tasks,
                                                 "question": task_dict["question"]}
                    else:
                        custom_task_dict_main = {"vmKeys": task_dict["vmKeys"], "title": tasks}
                    task_task_list.append([{"key": task_id_string, "val": custom_task_dict_main}])
                    task_info_dict[task_id_string] = get_task_markdown_data(module_markdown_data, tasks)
        module_dict_value = f"module-{module_id_string}"
        package_config_yaml[CONTENT_MODS].append(module_id_string)
        module_list = []
        for module in package_config_yaml[CONTENT_MODS]:
            module_list.append(f"module-{module}")
        package_config_yaml[CONTENT_MODS] = module_list
        build_json[CONTENT_MOD_STRING][module_dict_value] = {}
        build_json[CONTENT_MOD_STRING][module_dict_value][EXPORT_MOD_STRING] = module_config_yaml
        build_json[CONTENT_MOD_STRING][module_dict_value][CONTENT_MOD_EXPORT_MAPPING_TAGS] = {}
        build_json[CONTENT_MOD_STRING][module_dict_value][EXPORT_MOD_STRING][TASKS] = task_task_list
        build_json[CONTENT_MOD_STRING][module_dict_value][QUESTION_DESC] = {}
        build_json[CONTENT_MOD_STRING][module_dict_value][TASK_DESC] = {}
        for node_data in task_info_dict:
            task_list_items = []
            code_list = []
            star_list = []
            for line_data in task_info_dict[node_data].splitlines():
                line_chunk = line_data[:4]
                if line_chunk[:-2] == "# ":
                    info("Processing task Title ")
                elif line_chunk == "### ":
                    task_list_items.append(build_node_package([build_text_line(line_data[4:])], "heading-two"))
                elif line_chunk == "   -":
                    star_list.append(build_node_package([build_node_package([build_text_line(line_data[5:])],
                                                                            "list-item-child")], "list-item"))
                elif line_chunk == "   *":
                    star_list.append(build_node_package([build_node_package([build_text_line(line_data[5:])],
                                                                            "list-item-child")], "list-item"))
                elif line_chunk == "    ":
                    code_list.append(build_node_package([build_text_line(f"{line_data[4:]}\r")], "code-line"))
                elif line_chunk[:-1] == "## ":
                    task_list_items.append(build_node_package([build_text_line(line_data[3:])], "heading-one"))
                elif line_chunk[:-2] == "**":
                    task_list_items.append(build_node_package([build_text_line(line_data[2:-2])], "bold"))
                elif line_chunk[:-2] == "![":
                    image_data = build_node_package([build_text_line("")], "image-block")
                    picture_path = f"{input_dir}{DIR_CHARACTER}media{line_data[12:-1]}"
                    with open(picture_path, 'rb') as picture_file:
                        raw_picture = b64encode(picture_file.read()).decode('utf-8')
                    image_data["data"] = {"imageData": f"data:image/png;base64,{raw_picture}"}
                    task_list_items.append(image_data)
                elif len(code_list) > 0:
                    task_list_items.append(build_node_package(code_list, "code-block"))
                    code_list = []
                elif len(star_list) > 0:
                    task_list_items.append(build_node_package(star_list, "unordered-list"))
                    star_list = []
                elif len(line_data) > 0:
                    task_list_items, line_data, star_list, code_list = render_link_chunk(task_list_items,
                                                                                         line_data,
                                                                                         star_list,
                                                                                         code_list)
            if len(code_list) > 0:
                task_list_items.append(build_node_package(code_list, "code-block"))
            elif len(star_list) > 0:
                task_list_items.append(build_node_package(star_list, "unordered-list"))
            question_data[node_data] = {"data": {"document": {
                "data": {}, "object": "document", "nodes": task_list_items}, "object": "value"}, "version": 2}
        build_json[CONTENT_MOD_STRING][module_dict_value][EXPORT_TASKS] = {}
        build_json[CONTENT_MOD_STRING][module_dict_value][EXPORT_TASKS] = task_task_exports
        build_json[CONTENT_MOD_STRING][module_dict_value][TASK_DESC] = question_data
        for tasks in task_task_exports:
            if "question" in task_task_exports[tasks]:
                questions_descriptions[tasks] = question_data[tasks]
        build_json[CONTENT_MOD_STRING][module_dict_value][QUESTION_DESC] = questions_descriptions
        build_json[CONTENT_MOD_STRING][module_dict_value][CONTENT_MOD_EXPORT_TASK_ATTACHMENTS] = attachment_data_dict
    with open(f'{package_path}{DIR_CHARACTER}export.version', 'w') as export_version_file:
        export_version_file.write("9")
    with open(f'{package_path}{DIR_CHARACTER}package_export{JS_EXT}', 'w') as package_json:
        package_json.write(dumps(build_json))
    compile_export_package(f"{package_path}", input_package_export_name)


def compile_export_package(compile_dict: str,
                           package_export_name: str):
    current_path = getcwd()
    chdir(current_path)
    chdir(compile_dict)
    content_path = f"{compile_dict}{DIR_CHARACTER}content-modules{DIR_CHARACTER}"
    for (dir_path, dirs, files) in walk(content_path):
        for path_value in dirs:
            if "module-" in path_value:
                chdir(content_path)
                tar_file = tarfile.open(f"{path_value}.tar.gz", mode='w:gz')
                chdir(f"{path_value}")
                attachments_true = None
                count = 0
                for items in glob("attachments/"):
                    count += 1
                if count > 1:
                    if attachments_true:
                        tar_file.add("attachments")
                tar_file.close()
                chdir(content_path)
                rmtree(path_value)
    chdir(compile_dict)
    tar_data = tarfile.open(f"{package_export_name}", "w:gz")
    tar_data.add("package_export.json")
    tar_data.add("export.version")
    tar_data.add(f"content-modules")
    tar_data.close()


def strip_end_space(string_value: str):
    """Remove escape character from end of input string value and return."""
    while string_value[-1:] == " ":
        string_value = string_value[:-1]
    return string_value


def add_whitespace(input_string):
    url_safe_string = ""
    for char in input_string:
        if char != " ":
            url_safe_string += char
        else:
            url_safe_string += "%20"
    return url_safe_string


def strip_unsafe_file_names(string_data: str) -> str:
    new_string = ""
    string_data.replace("\x5C", "%92")

    for character in string_data:
        if character == ":":
            new_string += "%58"
        elif character == "/":
            new_string += "%47"
        elif character == "?":
            new_string += "%63"
        elif character == "&":
            new_string += "%38"
        elif character == '"':
            new_string += "'"
        else:
            new_string += character

    return new_string


def h_one_format(heading_data):
    return f"# {heading_data}{NEW_LINE}"


def get_value(item: str, json_package: dict) -> dict:
    """Return dict item."""
    return_dict = {}
    if item in json_package:
        return_dict[item] = json_package[item]
    return return_dict


class PackageExport:
    """Package object class to manage package data."""
    def __init__(self, raw_data):
        self.enrollment_type = get_value(ENROLLMENT_TYPE, raw_data)[ENROLLMENT_TYPE]
        self.status = get_value(STAT_P, raw_data)[STAT_P]
        objective = get_value('objective', raw_data)
        if 'objective' in objective:
            self.objective = get_value('objective', raw_data)['objective']
        else:
            self.objective = []
        self.randomized_questions = get_value(RANDOM_QUESTIONS, raw_data)[RANDOM_QUESTIONS]
        self.self_enroll_enabled = get_value(SELF_ENROLLMENT, raw_data)[SELF_ENROLLMENT]
        self.leaderboard_enabled = get_value(LEADERBOARD, raw_data)[LEADERBOARD]
        self.tool = get_value('tool', raw_data)['tool']
        self.url_value = get_value('url', raw_data)['url']
        resources = get_value('resources', raw_data)['resources']
        if resources:
            self.resources = get_value('resources', raw_data)['resources']
        else:
            self.resources = []
        self.owner = get_value('owner', raw_data)['owner']
        self.name_value = get_value(N_STR, raw_data)[N_STR]
        event_time = get_value(EVENT_TIME, raw_data)[EVENT_TIME]
        if event_time:
            self.event_time_limit = get_value(EVENT_TIME, raw_data)[EVENT_TIME]
        else:
            self.event_time_limit = 0
        self.content_modules = get_value(CONTENT_MODS, raw_data)[CONTENT_MODS]
        self.difficulty = get_value('difficulty', raw_data)['difficulty']
        description = get_value('description', raw_data)['description']
        if description:
            self.description = get_value('description', raw_data)['description']
        work_roles = get_value('workRoles', raw_data)['workRoles']
        if work_roles:
            self.work_roles = work_roles
        else:
            self.work_roles = []
        event_roles = get_value('eventRoles', raw_data)['eventRoles']
        if event_roles:
            self.event_roles = event_roles
        else:
            self.event_roles = []
        content_class = get_value(C_CLASS, raw_data)[C_CLASS]
        if content_class:
            self.content_class = content_class
        else:
            self.content_class = []
        platform_roles = get_value(P_ROLES, raw_data)[P_ROLES]
        if platform_roles:
            self.platform_roles = platform_roles
        else:
            self.platform_roles = []
        publisher = get_value(P_STR, raw_data)[P_STR]
        if publisher:
            self.publisher = publisher
        else:
            self.publisher = ""
        topics = get_value(TOPICS_STR, raw_data)[TOPICS_STR]
        if topics:
            self.topics = topics
        else:
            self.topics = []
        answer_feedback = get_value(ANSWER_FEEDBACK, raw_data)[ANSWER_FEEDBACK]
        if answer_feedback:
            self.answer_feedback = answer_feedback
        else:
            self.answer_feedback = {}
        industry_sector = get_value(INDUSTRY_SECTOR, raw_data)[INDUSTRY_SECTOR]
        if industry_sector:
            self.industry_sector = industry_sector
        else:
            self.industry_sector = ''

    def to_dict(self):
        """Return dictionary object type for to/from dict formatting."""
        data = {
            ENROLLMENT_TYPE: self.enrollment_type,
            P_STR: self.publisher,
            STAT_P: self.status,
            'objective': self.objective,
            'tool': self.tool,
            'url': self.url_value,
            'resources': self.resources,
            'owner': self.owner,
            N_STR: self.name_value,
            CONTENT_MODS: self.content_modules,
            'difficulty': self.difficulty,
            'description': self.description,
            SELF_ENROLLMENT: self.self_enroll_enabled,
            EVENT_TIME: self.event_time_limit,
            RANDOM_QUESTIONS: self.randomized_questions,
            LEADERBOARD: self.leaderboard_enabled,
            'workRoles': self.work_roles,
            'eventRoles': self.event_roles,
            C_CLASS: self.content_class,
            P_ROLES: self.platform_roles,
            TOPICS_STR: self.topics,
            ANSWER_FEEDBACK: self.answer_feedback,
            INDUSTRY_SECTOR: self.industry_sector

        }
        return data

    def to_yml(self):
        """Return dictionary object type for to/from
         dict formatting."""
        description = ""
        if self.description:
            description = self.description
        content_mods = "contentModules:\n"
        for item in self.content_modules:
            content_mods += f"  - \"{item}\"\n"
        yml_out = f"{ENROLLMENT_TYPE}: '{self.enrollment_type}'\n" \
                  f"{STAT_P}: '{self.status}'\n" \
                  f"{P_STR}: '{self.publisher}'\n" \
                  f"owner: '{self.owner}'\n" \
                  f"{N_STR}:  '{self.name_value}'\n" \
                  f"objective: {self.objective}\n" \
                  f"url:  '{self.url_value}'\n" \
                  f"{SELF_ENROLLMENT}: {self.self_enroll_enabled}\n" \
                  f"tool:  '{self.tool}'\n" \
                  f"{RANDOM_QUESTIONS}: {self.randomized_questions}\n" \
                  f"resources:  {self.resources}\n" \
                  f"{LEADERBOARD}: {str(self.leaderboard_enabled)}\n" \
                  f"{content_mods}" \
                  f"difficulty:  '{self.difficulty}'\n" \
                  f"description:  \"{description}\"\n" \
                  f"{EVENT_TIME}: {str(self.event_time_limit)}\n" \
                  f"{'workRoles'}: {self.work_roles}\n" \
                  f"{'eventRoles'}: {self.event_roles}\n" \
                  f"{C_CLASS}: {self.content_class}\n" \
                  f"{P_ROLES}: {self.platform_roles}\n" \
                  f"{TOPICS_STR}: {self.topics}\n" \
                  f"{ANSWER_FEEDBACK}: {self.answer_feedback}\n" \
                  f"{INDUSTRY_SECTOR}: {self.industry_sector}\n"

        return yml_out


class AnswerKey:
    """Question object class to manage answers, hints and points."""
    def __init__(self, raw_data, attachment_data, task):
        question_query = get_value("question", raw_data)
        if question_query:
            self.question = question_query["question"]
        else:
            self.question = None
        self.title = get_value("title", raw_data)["title"]
        vm_key = get_value("vmKeys", raw_data)
        if len(vm_key) > 0:
            self.vm_keys = get_value("vmKeys", raw_data)['vmKeys']
        else:
            self.vm_keys = []
        self.attachment_data = []
        for values in attachment_data:
            if values == task and len(attachment_data[values]) > 0:
                self.attachment_data = attachment_data[values]
            elif values == task:
                self.attachment_data = []
        self.task_id = task

    def to_yml(self):
        """Return dictionary object type for to/from
         dict formatting."""
        yml_out = ""
        title_string = self.title.replace('"', "\\\"")
        yml_out += f"\"{title_string}\": \n"
        if self.question:
            yml_out += f"  type: {self.question['type']}\n"
            yml_out += f"  mappingtags: {self.question['mappingTags']}\n"
            yml_out += f"  extradata: {self.question['extraData']}\n"
            yml_out += f"  pointtotal: {self.question['points']}\n"
            yml_out += f"  retrycount: {self.question['retryCount']}\n"
            answer_data = "  answers: \n"
            correct_list = []
            incorrect_list = []
            for answers in self.question["choices"]:
                if answers["correct"] is True:
                    correct_list.append(answers['value'])
                elif answers["correct"] is False:
                    incorrect_list.append(answers['value'])
            if correct_list:
                answer_data += f"    correct:\n"
                for item in correct_list:
                    safe_item = item.replace('"', "'")
                    safe_item = safe_item.replace("\\", "\\\\")
                    answer_data += f"    - \"{safe_item}\" \n"

            if incorrect_list:
                answer_data += f"    incorrect:\n"
                for item in incorrect_list:
                    safe_item = item.replace('"', "'")
                    safe_item = safe_item.replace("\\", "\\\\")
                    answer_data += f"    - \"{safe_item}\" \n"
            yml_out += answer_data
            hint_number = 0
            if "hints" in self.question:
                if len(self.question["hints"]) > 0:
                    hints_data = ""
                    hints_data += f"  hints:\n"
                    for hints in self.question["hints"]:
                        hint_number += 1
                        hints_data += f"    {str(hint_number)}: \n      cost: {hints['pointsDeduction']}\n"
                        hint_text = hints['text'].replace('\n', "\n       ")
                        hint_text = hint_text.replace('"', "\\\"")
                        hints_data += f"      message: \"{hint_text}\" \n"
                    yml_out += hints_data
        if len(self.vm_keys) > 0:
            keys_vm = "  vmKeys:\n"
            for items in self.vm_keys:
                keys_vm += f"    \"{items['val']}\": \n      ID: \"{items['key']['repetitionGroup']}\"" \
                           f"\n      index: {items['key']['index']}\n"
            yml_out += f"{keys_vm}"
        else:
            yml_out += "  vmKeys: [] \n"

        attachment_list = []
        if len(self.attachment_data) > 0:
            for attachment in self.attachment_data:
                attachment_value = self.attachment_data[attachment]
                if isinstance(attachment_value, dict):
                    attachment_list.append(attachment_value['attachmentMetaName'])
        yml_out += f"  attachments: {attachment_list}\n"
        yml_out += "\n"
        return yml_out


def extract_all(archives: str, extract_path: str):
    """Extract archive file to input path."""
    tar = tarfile.open(archives, "r:gz")
    tar.extractall(path=extract_path)
    remove(f"{extract_path}{DIR_CHARACTER}package_export.json")
    remove(f"{extract_path}{DIR_CHARACTER}export.version")
    attachment_path = f"{extract_path}{DIR_CHARACTER}attachment{DIR_CHARACTER}"
    for items in glob(f"{extract_path}{DIR_CHARACTER}content-modules{DIR_CHARACTER}*.tar.gz"):
        tar_module = tarfile.open(items, "r:gz")
        tar_module.extractall(path=attachment_path)
        tar_module.close()
    tar.close()
    rmtree(f"{extract_path}{DIR_CHARACTER}content-modules")
    attachment_dir = f"{extract_path}{DIR_CHARACTER}attachments"
    try:
        mkdir(attachment_dir)
    except FileExistsError:
        rmtree(attachment_dir)
        mkdir(attachment_dir)
    for file_name in \
            glob(f"{extract_path}{DIR_CHARACTER}attachment{DIR_CHARACTER}attachments{DIR_CHARACTER}*{DIR_CHARACTER}*"):
        try:
            move(file_name, f"{extract_path}{DIR_CHARACTER}attachments{DIR_CHARACTER}")
        except Error:
            info("File move failed")
    try:
        rmtree(f"{extract_path}{DIR_CHARACTER}attachment")
    except FileNotFoundError:
        pass


def extract_tar_data(file_name: str, output: str) -> None:
    """Extract tar gz file from input file_name string."""
    extract_all(file_name, output)


class ModuleExportContentModule:
    def __init__(self, raw_data):
        export_tasks = raw_data[EXPORT_MOD_STRING]
        self.attachment_data = raw_data[CONTENT_MOD_EXPORT_TASK_ATTACHMENTS]
        self.status = get_value(STAT_S, export_tasks)[STAT_S]
        self.randomizable = get_value('randomizable', export_tasks)['randomizable']
        self.survey = get_value('survey', export_tasks)['survey']
        clone_source = get_value('cloneSource', export_tasks)
        if 'cloneSource' in clone_source:
            self.clone_source = clone_source['cloneSource']
        else:
            self.clone_source = []
        self.owner = get_value('owner', export_tasks)['owner']
        self.name_value = get_value(N_STR, export_tasks)[N_STR]
        question_data = get_value('questions', export_tasks)
        if 'questions' in question_data:
            self.questions = question_data['questions']
        tasks_data = get_value(TASKS, export_tasks)
        if tasks_data:
            self.questions = tasks_data[TASKS]
        self.duration = get_value('duration', export_tasks)['duration']
        self.description = get_value('description', export_tasks)['description'].replace('"', "'")

    def to_dict(self):
        """Return dictionary object type for to{DIR_CHARACTER}from
         dict formatting."""
        data = {
            STAT_S: self.status,
            'randomizable': self.randomizable,
            'survey': self.survey,
            'cloneSource': self.clone_source,
            'owner': self.owner,
            N_STR: self.name_value,
            'questions': self.questions,
            'duration': self.duration,
            'description': self.description,
            'attachments': self.attachment_data
        }
        return data

    def to_yml(self):
        """Return dictionary object type for to/from
         dict formatting."""
        yml_out = ""
        yml_out += f"description: \"{str(self.description)}\"\n"
        yml_out += f"name: '{self.name_value}'\n"
        if len(self.clone_source) > 0:
            yml_out += f"cloneSource: {self.clone_source}\n"
        yml_out += f"owner: '{self.owner}'\n"
        yml_out += f"randomizable: {self.randomizable}\n"
        yml_out += f"status:  '{self.status}'\n"
        yml_out += f"survey:  {self.survey}\n"
        yml_out += f"duration:  {str(self.duration)}\n"
        task_list = []
        value_list = []
        for items in self.questions:
            count = len(items)
            for value in items:
                value_string = value['val']['title']
                if count > 1:
                    value_list.append(value_string)
                else:
                    task_list.append(value_string)
                    count = 0
            if len(value_list) > 1:
                task_list.append(value_list)
                value_list = []
        yml_out += f"tasks:\n"
        for item in task_list:
            if isinstance(item, list):
                yml_out += f"  - {item} \n"
            else:
                safe_item = item.replace('"', "'")
                safe_item = safe_item.replace("\\", "\\\\")
                yml_out += f"  - \"{safe_item}\" \n"
        return yml_out
