"""The pycep model library."""
# coding=utf-8
import platform
import tarfile
from shutil import rmtree
from uuid import uuid4
from json import dumps
from os import mkdir, chdir, walk, getcwd

from yaml_info.yamlinfo import YamlInfo
from pycep.content_strings import *

DIR_CHARACTER = "/"
SYSTEM_PLATFORM = platform.system()
if SYSTEM_PLATFORM == "Windows":
    info("Windows Detected")
    DIR_CHARACTER = "\\"
elif SYSTEM_PLATFORM != "Linux":
    error(f"Unsupported System type detected")
NEW_LINE = "\n"


def build_text_line(line_data):
    data_nodes = {"marks": [],
                  "object": "text",
                  "text": line_data
                  }
    return data_nodes


def build_node_package(nodes_data: list, data_type: str):
    data_node = {"data": {},
                 "object": "block",
                 "type": data_type,
                 "nodes": nodes_data,
                 }
    return data_node


def compile_package_data(package_export_name, input_dir, export_dir, owner_id):
    package_dir = input_dir
    dir_paths = package_dir.split("/")
    total_length = len(dir_paths)
    package_name = dir_paths[(total_length - 1)]
    input_package_export_name = package_export_name
    tar_data = tarfile.open(f"{input_package_export_name}", "w:gz")
    package_config_path = f"{input_dir}/{package_name}.yml"
    package_config_yaml = YamlInfo(package_config_path, "none", "none").get()
    build_json = {}
    build_json[PACKAGE_STR] = {}
    build_json[PACKAGE_STR] = package_config_yaml
    build_json['packageKey'] = str(uuid4())
    try:
        mkdir(f"{export_dir}/{package_name}")
    except FileExistsError:
        rmtree(f"{export_dir}/{package_name}")
        mkdir(f"{export_dir}/{package_name}")
    mkdir(f"{export_dir}/{package_name}/content-modules")
    tar_data.close()
    file_list = package_config_yaml["contentModules"]
    package_config_yaml[CONTENT_MODS] = []
    build_json[CONTENT_MOD_STRING] = {}
    for file_name in file_list:
        mod_config_path = f"{input_dir}/{file_name}{YAML_EXT}"
        module_config_yaml = YamlInfo(mod_config_path, "none", "none").get()
        slide_info_dict = {}
        slide_task_exports = {}
        question_data = {}
        questions_descriptions = {}
        if "tasks" in module_config_yaml:
            slide_task_list = []
            for tasks in module_config_yaml["tasks"]:
                sub_task_list = []
                if isinstance(tasks, list):
                    for task in tasks:
                        full_file_name = task
                        task_id = str(uuid4())
                        task_id_string = f"task-{task_id}"
                        task_dict = \
                            YamlInfo(f"{input_dir}/{file_name}/{full_file_name}{YAML_EXT}", "none", "none").get()
                        sub_task_list.append({"key": task_id_string, "val": task_dict})
                        slide_task_exports[task_id_string] = task_dict
                        with open(f"{input_dir}/{file_name}/{full_file_name}{MD_EXT}", 'r') as file_raw:
                            slide_info_dict[task_id_string] = file_raw.read()
                    slide_task_list.append(sub_task_list)
                else:
                    full_file_name = tasks
                    task_id = str(uuid4())
                    task_id_string = f"task-{task_id}"
                    task_dict = YamlInfo(f"{input_dir}/{file_name}/{full_file_name}{YAML_EXT}", "none", "none").get()
                    slide_task_list.append([{"key": task_id_string, "val": task_dict}])
                    slide_task_exports[task_id_string] = task_dict
                    with open(f"{input_dir}/{file_name}/{full_file_name}{MD_EXT}", 'r') as file_raw:
                        slide_info_dict[task_id_string] = file_raw.read()
        module_id = str(uuid4())
        module_id_string = f"{module_id}"
        module_dict_value = module_id_string
        package_config_yaml[CONTENT_MODS].append(module_id_string)
        build_json[CONTENT_MOD_STRING][module_dict_value] = {}
        build_json[CONTENT_MOD_STRING][module_dict_value][EXPORT_MOD_STRING] = module_config_yaml
        build_json[CONTENT_MOD_STRING][module_dict_value][CONTENT_MOD_EXPORT_MAPPING_TAGS] = {}
        build_json[CONTENT_MOD_STRING][module_dict_value][CONTENT_MOD_EXPORT_TASK_ATTACHMENTS] = {}
        # TODO Walk path for all markdown files and render a slide for each
        build_json[CONTENT_MOD_STRING][module_dict_value][EXPORT_MOD_STRING][TASKS] = slide_task_list
        build_json[CONTENT_MOD_STRING][module_dict_value][QUESTION_DESC] = {}
        build_json[CONTENT_MOD_STRING][module_dict_value][TASK_DESC] = {}
        # TODO Build proper markdown parser to dict
        for node_data in slide_info_dict:
            slide_list_items = []
            code_list = []
            star_list = []
            for line_data in slide_info_dict[node_data].splitlines():
                line_chunk = line_data[:4]
                if line_chunk == "### ":
                    slide_list_items.append(build_node_package([build_text_line(line_data[4:])], "heading-two"))
                elif line_chunk == "   -":
                    star_list.append(build_node_package([build_node_package([build_text_line(line_data[5:])],
                                                                            "list-item-child")], "list-item"))
                elif line_chunk == "   *":
                    star_list.append(build_node_package([build_node_package([build_text_line(line_data[5:])],
                                                                            "list-item-child")], "list-item"))
                elif line_chunk == "    ":
                    code_list.append(build_node_package([build_text_line(f"{line_data[4:]}\r")], "code-line"))
                elif line_chunk[:-1] == "## ":
                    slide_list_items.append(build_node_package([build_text_line(line_data[3:])], "heading-one"))
                elif line_chunk[:-1] == "***":
                    slide_list_items.append(build_node_package([build_text_line(line_data[3:-3])], "bold"))
                elif line_chunk[:-2] == "# ":
                    print("Title ")
                elif line_chunk[:-2] == "![":
                    image_data = build_node_package([build_text_line("")], "image-block")
                    image_data["data"] = {"imageData": line_data[10:-1]}
                    slide_list_items.append(image_data)
                elif len(code_list) > 0:
                    slide_list_items.append(build_node_package(code_list, "code-block"))
                    code_list = []
                elif len(star_list) > 0:
                    slide_list_items.append(build_node_package(star_list, "unordered-list"))
                    star_list = []
                elif len(line_data) > 0:
                    # TODO add regex parser for text data that contains bold/italic/code font formats
                    slide_list_items.append(build_node_package([build_text_line(line_data)], "paragraph"))
            if len(code_list) > 0:
                slide_list_items.append(build_node_package(code_list, "code-block"))
            elif len(star_list) > 0:
                slide_list_items.append(build_node_package(star_list, "unordered-list"))
            question_data[node_data] = {"data": {"document": {"data": {}, "object": "document", "nodes": slide_list_items},
                                                   "object": "value"}, "version": 2}
        build_json[CONTENT_MOD_STRING][module_dict_value][EXPORT_TASKS] = {}
        for slide in slide_info_dict:
            # TODO parse attachment data
            build_json[CONTENT_MOD_STRING][module_dict_value][CONTENT_MOD_EXPORT_TASK_ATTACHMENTS][slide] = {}

        build_json[CONTENT_MOD_STRING][module_dict_value][EXPORT_TASKS] = slide_task_exports
        build_json[CONTENT_MOD_STRING][module_dict_value][TASK_DESC] = question_data
        for slides in slide_task_exports:
            if "question" in slide_task_exports[slides]:
                questions_descriptions[slides] = question_data[slides]
        #build_json[CONTENT_MOD_STRING][module_dict_value][EXPORT_QUESTIONS_STR] = questions_descriptions
        build_json[CONTENT_MOD_STRING][module_dict_value][QUESTION_DESC] = questions_descriptions
        with open(f'data/module-.tar.gz', 'rb') as blank_module_file:
            module_data = blank_module_file.read()
        with open(f'{export_dir}/{package_name}/content-modules/{module_id_string}.tar.gz', 'wb') as module_file:
            module_file.write(module_data)
    with open(f'{export_dir}/{package_name}/export.version', 'w') as export_version_file:
        export_version_file.write("9")
    with open(f'{export_dir}/{package_name}/package_export{JS_EXT}', 'w') as package_json:
        package_json.write(dumps(build_json))
    compile_export_package(f"{export_dir}/{package_name}", input_package_export_name)


def compile_export_package(compile_dict: str, package_export_name: str):
    current_path = getcwd()
    chdir(current_path)
    tar_data = tarfile.open(f"{package_export_name}", "w:gz")
    chdir(compile_dict)
    for (dir_path, dirs, files) in walk(compile_dict):
        for filename in files:
            if dir_path == f"{compile_dict}/content-modules":
                chdir(compile_dict)
                try:
                    tar_data.add(f"content-modules/")
                except FileExistsError:
                    pass
            else:
                chdir(dir_path)
                tar_data.add(f"{filename}")
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
        else:
            new_string += character

    return new_string


def format_table(dict_value):
    package_data = ""
    package_spacer = ""
    package_headers = ""
    for data_value, value in dict_value.items():
        if value and data_value != 'questions':
            package_data += f"{data_value} |"
            package_spacer += ":---------- |"
            package_headers += f"{value} |"

    package_data += f"\n{package_spacer}\n{package_headers}"
    return package_data


def h_one_format(heading_data):
    return f"# {heading_data}{NEW_LINE}"


def get_value(item: str, json_package: dict) -> dict:
    """Return dict item."""
    return_dict = {}
    if item in json_package:
        return_dict[item] = json_package[item]
    return return_dict


class PackageExport:
    def __init__(self, raw_data):
        self.enrollment_type = get_value(ENROLLMENT_TYPE, raw_data)[ENROLLMENT_TYPE]
        self.status = get_value(STAT_S, raw_data)[STAT_S]
        objective = get_value('objective', raw_data)
        if 'objective' in objective:
            self.objective = get_value('objective', raw_data)['objective']
        else:
            self.objective = []
        self.reveal_answers = get_value(REVEAL_ANSWERS, raw_data)[REVEAL_ANSWERS]
        self.randomized_questions = get_value(RANDOM_QUESTIONS, raw_data)[RANDOM_QUESTIONS]
        self.self_enroll_enabled = get_value(SELF_ENROLLMENT, raw_data)[SELF_ENROLLMENT]
        self.leaderboard_enabled = get_value(LEADERBOARD, raw_data)[LEADERBOARD]
        self.image = get_value('image', raw_data)['image']
        self.tool = get_value('tool', raw_data)['tool']
        self.url_value = get_value('url', raw_data)['url']
        resources = get_value('resources', raw_data)['resources']
        if resources:
            self.resources = get_value('resources', raw_data)['resources']
        else:
            self.resources = []
        self.owner = get_value('owner', raw_data)['owner']
        self.name_value = get_value(N_STR, raw_data)[N_STR]
        self.event_time_limit = get_value(EVENT_TIME, raw_data)[EVENT_TIME]
        self.content_modules = get_value(CONTENT_MODS, raw_data)[CONTENT_MODS]
        self.difficulty = get_value('difficulty', raw_data)['difficulty']
        description = get_value('description', raw_data)['description']
        if description:
            self.description = get_value('description', raw_data)['description']

    def to_dict(self):
        """Return dictionary object type for to/from dict formatting."""
        data = {
            ENROLLMENT_TYPE: self.enrollment_type,
            STAT_S: self.status,
            'objective': self.objective,
            'image': self.image,
            'tool': self.tool,
            'url': self.url_value,
            'resources': self.resources,
            'owner': self.owner,
            N_STR: self.name_value,
            CONTENT_MODS: self.content_modules,
            'difficulty': self.difficulty,
            'description': self.description,
            SELF_ENROLLMENT: self.self_enroll_enabled,
            REVEAL_ANSWERS: self.reveal_answers,
            EVENT_TIME: self.event_time_limit,
            RANDOM_QUESTIONS: self.randomized_questions,
            LEADERBOARD: self.leaderboard_enabled

        }
        return data

    def to_yml(self):
        """Return dictionary object type for to/from
         dict formatting."""
        description = ""
        if self.description:
            description = self.description
        yml_out = f"{ENROLLMENT_TYPE}: '{self.enrollment_type}'\n" \
                  f"{STAT_S}: '{self.status}'\n" \
                  f"owner: '{self.owner}'\n" \
                  f"{N_STR}:  '{self.name_value}'\n" \
                  f"objective: {self.objective}\n" \
                  f"url:  '{self.url_value}'\n" \
                  f"image: '{self.image}'\n" \
                  f"{SELF_ENROLLMENT}: {self.self_enroll_enabled}\n" \
                  f"tool:  '{self.tool}'\n" \
                  f"{RANDOM_QUESTIONS}: {self.randomized_questions}\n" \
                  f"resources:  {self.resources}\n" \
                  f"{LEADERBOARD}: {str(self.leaderboard_enabled)}\n" \
                  f"{CONTENT_MODS}:  {self.content_modules}\n" \
                  f"difficulty:  '{self.difficulty}'\n" \
                  f"description:  '{description}'\n" \
                  f"{REVEAL_ANSWERS}: {self.reveal_answers}\n" \
                  f"{EVENT_TIME}: {str(self.event_time_limit)}\n"
        return yml_out


class AnswerKey:
    def __init__(self, raw_data):
        question_query = get_value("question", raw_data)
        if question_query:
            self.question = question_query["question"]
        else:
            self.question = None
        self.title = get_value("title", raw_data)["title"]
        self.vm_keys = get_value("vmKeys", raw_data)["vmKeys"]

    def to_yml(self):
        """Return dictionary object type for to/from
         dict formatting."""
        yml_out = ""
        if self.question:
            yml_out += f"question: {str(self.question)}\n"
        yml_out += f"title: '{self.title}'\n"
        if len(self.vm_keys) > 0:
            yml_out += f"vmKeys: {self.vm_keys}\n"
        else:
            yml_out += f"vmKeys: []\n"
        return yml_out


class ModuleExportContentModule:
    def __init__(self, raw_data):
        self.status = get_value(STAT_S, raw_data)[STAT_S]
        self.randomizable = get_value('randomizable', raw_data)['randomizable']
        self.survey = get_value('survey', raw_data)['survey']
        clone_source = get_value('cloneSource', raw_data)
        if 'cloneSource' in clone_source:
            self.clone_source = clone_source['cloneSource']
        else:
            self.clone_source = []
        self.owner = get_value('owner', raw_data)['owner']
        self.name_value = get_value(N_STR, raw_data)[N_STR]
        question_data = get_value('questions', raw_data)
        if 'questions' in question_data:
            self.questions = question_data['questions']
        tasks_data = get_value(TASKS, raw_data)
        if tasks_data:
            self.questions = tasks_data[TASKS]
        self.duration = get_value('duration', raw_data)['duration']
        self.description = get_value('description', raw_data)['description']

    def to_dict(self):
        """Return dictionary object type for to/from
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
            'description': self.description
        }
        return data

    def to_yml(self):
        """Return dictionary object type for to/from
         dict formatting."""
        yml_out = ""
        yml_out += f"description: '{str(self.description)}'\n"
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
                value_string = strip_unsafe_file_names(value['val']['title'])
                if count > 1:
                    value_list.append(value_string)
                else:
                    task_list.append(value_string)
                    count = 0
            if len(value_list) > 1:
                task_list.append(value_list)
                value_list = []
        yml_out += f"tasks:  {task_list}"

        return yml_out
