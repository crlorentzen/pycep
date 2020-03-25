"""The pycep model library."""
# coding=utf-8
import platform

from pycep.content_strings import *

DIR_CHARACTER = "/"
SYSTEM_PLATFORM = platform.system()
if SYSTEM_PLATFORM == "Windows":
    info("Windows Detected")
    DIR_CHARACTER = "\\"
elif SYSTEM_PLATFORM != "Linux":
    error(f"Unsupported System type detected")


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
        self.objective = get_value('objective', raw_data)['objective']
        self.image = get_value('image', raw_data)['image']
        self.tool = get_value('tool', raw_data)['tool']
        self.url_value = get_value('url', raw_data)['url']
        self.resources = get_value('resources', raw_data)['resources']
        self.owner = get_value('owner', raw_data)['owner']
        self.name_value = get_value(N_STR, raw_data)[N_STR]
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
            'description': self.description
        }
        return data


class ModuleExportContentModule:
    def __init__(self, raw_data):
        self.status = get_value(STAT_S, raw_data)[STAT_S]
        self.randomizable = get_value('randomizable', raw_data)['randomizable']
        self.survey = get_value('survey', raw_data)['survey']
        clone_source = get_value('cloneSource', raw_data)
        if 'cloneSource' in clone_source:
            self.clone_source = clone_source['cloneSource']
        else:
            self.clone_source = None
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
