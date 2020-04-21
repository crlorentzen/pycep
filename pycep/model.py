"""The pycep model library."""
# coding=utf-8
import platform
from formatter import strip_unsafe_file_names

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
