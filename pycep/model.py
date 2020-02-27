"""The pycep model library."""
# coding=utf-8
import platform

from logging import info

dir_character = "/"
if platform.system() == "Windows":
    info("Windows Detected")
    dir_character = "\\"

content_module_string = 'packageExportContentModules'


def get_value(item: str, json_package: dict) -> dict:
    """Return dict item."""
    return_dict = {}
    if item in json_package:
        return_dict[item] = json_package[item]
    return return_dict


class PackageExport:
    def __init__(self, raw_data):
        self.enrollment_type = get_value('enrollmentType', raw_data)['enrollmentType']
        self.status = get_value('status', raw_data)['status']
        self.objective = get_value('objective', raw_data)['objective']
        self.image = get_value('image', raw_data)['image']
        self.tool = get_value('tool', raw_data)['tool']
        self.url_value = get_value('url', raw_data)['url']
        self.resources = get_value('resources', raw_data)['resources']
        self.owner = get_value('owner', raw_data)['owner']
        self.name_value = get_value('name', raw_data)['name']
        self.content_modules = get_value('contentModules', raw_data)['contentModules']
        self.difficulty = get_value('difficulty', raw_data)['difficulty']
        description = get_value('description', raw_data)['description']
        if description:
            self.description = get_value('description', raw_data)['description']

    def to_dict(self):
        """Return dictionary object type for to/from dict formatting."""
        data = {
            'enrollmentType': self.enrollment_type,
            'status': self.status,
            'objective': self.objective,
            'image': self.image,
            'tool': self.tool,
            'url': self.url_value,
            'resources': self.resources,
            'owner': self.owner,
            'name': self.name_value,
            'contentModules': self.content_modules,
            'difficulty': self.difficulty,
            'description': self.description
        }
        return data


class ModuleExportContentModule:
    def __init__(self, raw_data):
        self.status = get_value('status', raw_data)['status']
        self.randomizable = get_value('randomizable', raw_data)['randomizable']
        self.survey = get_value('survey', raw_data)['survey']
        clone_source = get_value('cloneSource', raw_data)
        if 'cloneSource' in clone_source:
            self.clone_source = clone_source['cloneSource']
        else:
            self.clone_source = None
        self.owner = get_value('owner', raw_data)['owner']
        self.name_value = get_value('name', raw_data)['name']
        self.questions = get_value('questions', raw_data)['questions']
        self.duration = get_value('duration', raw_data)['duration']
        self.description = get_value('description', raw_data)['description']

    def to_dict(self):
        """Return dictionary object type for to/from dict formatting."""
        data = {
            'status': self.status,
            'randomizable': self.randomizable,
            'survey': self.survey,
            'cloneSource': self.clone_source,
            'owner': self.owner,
            'name': self.name_value,
            'questions': self.questions,
            'duration': self.duration,
            'description': self.description
        }
        return data
