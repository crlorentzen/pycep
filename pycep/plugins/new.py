"""Pycep plugin to create a new package and module from the cli"""
from os import mkdir, rmdir

from click import prompt
from pycep.model import DIR_CHARACTER, strip_unsafe_file_names, NEW_LINE, STAT_S


def selection_list(question, question_list, yaml_key):

    count = 0
    question_list_str = ""
    question_dict = {}
    for items in question_list:
        count += 1
        question_list_str += f"\n{str(count)}: {items}"
        question_dict[count] = items
    return_type = prompt(f"{question}{question_list_str}\n", type=int)
    return f"{yaml_key}: '{question_dict[return_type]}'{NEW_LINE}"


def selection_boolean(question, yaml_key):
    return_type = prompt(f"{question}\n 0: False \n 1: True", type=int)
    if return_type == 0:
        result_answer = "True"
    else:
        result_answer = "False"
    return f"{yaml_key}: {result_answer}{NEW_LINE}"


def selection_int(question, yaml_key):
    return_type = prompt(f"{question} - Note:Enter an int only", type=int)
    return f"{yaml_key}: {return_type}{NEW_LINE}"


def new_module(output_dir: str):
    package_name = prompt('Please enter a new package name?\n', type=str)
    package_dir = f"{output_dir}{package_name}"
    package_dir_yaml = f"{package_dir}{DIR_CHARACTER}{package_name}.yml"
    package_path = f"{package_dir}{DIR_CHARACTER}"
    package_yml = ""
    attachment_dir = f"{package_dir}{DIR_CHARACTER}attachments"
    try:
        mkdir(package_dir)
        mkdir(attachment_dir)
    except FileExistsError:
        rmdir(package_dir)
        mkdir(package_dir)
        mkdir(attachment_dir)
    package_yml += f"name: \"{package_name}\"{NEW_LINE}"
    package_yml += f"{STAT_S}: \"published\"{NEW_LINE}"
    package_yml += f"objective: []{NEW_LINE}"
    package_yml += f"resources: []{NEW_LINE}"
    package_yml += f"url: ''{NEW_LINE}"
    package_yml += f"image: ''{NEW_LINE}"
    package_yml += selection_list('Choose the enrollment type from the following list?\n',
                                  ['individual', 'team'],
                                  'enrollmentType')
    package_yml += selection_list('Choose the difficulty for this package?',
                                  ['beginner', 'intermediate', 'advanced', 'expert'],
                                  'difficulty')
    package_yml += selection_boolean('Self Enroll Enabled?',
                                     'selfEnrollEnabled')
    package_yml += selection_boolean('Randomize Questions Enabled?',
                                     'randomizeQuestions')
    package_yml += selection_boolean('Leaderboard Enabled?',
                                     'leaderboardEnabled')
    package_yml += selection_boolean('Reveal Answers Enabled?',
                                     'revealAnswers')
    package_yml += selection_int('How long should the event time limit be?\n',
                                 'eventTimeLimitMinutes')
    package_yml += f"contentModules:{NEW_LINE}"
    number_of_modules = prompt('Please enter the number of new content modules you want to create?', type=int)
    module_dict = {}
    while number_of_modules > 0:
        new_module_name = prompt('Please enter a new module name', type=str)
        module_dict[new_module_name] = {}
        number_of_modules += -1
        safe_path_name = strip_unsafe_file_names(new_module_name)
        module_path = f"{package_dir}{DIR_CHARACTER}{safe_path_name}"
        module_tasks_path = f"{module_path}{DIR_CHARACTER}tasks"
        module_task_dir = f"{module_tasks_path}{DIR_CHARACTER}"
        mkdir(module_path)
        mkdir(module_tasks_path)
        package_yml += f"  - \"{safe_path_name}\"{NEW_LINE}"
        task_count = prompt('How many tasks will there be for this module?', type=int)
        while task_count > 0:
            new_task_name = prompt('Please enter a new task name', type=str)
            new_task_path = f"{strip_unsafe_file_names(new_task_name)}"
            with open(f"{module_task_dir}{new_task_path}.md", 'w') as new_task_data:
                new_task_data.write(f"# {new_task_name} \n...")
            new_task_yml = "extradata: {}\nattachments: []\nmappingtags: []\n"
            question_task = prompt('Will this task have a question? Y/N', type=str)
            if question_task == "Y" or "y":
                new_task_yml += f"pointtotal: {prompt('How many points will this task be worth?', type=int)}{NEW_LINE}"
                new_task_yml += f"retrycount: {prompt('How many retries will this task have?', type=int)}{NEW_LINE}"
                correct_answers = prompt("How many correct answers will there be?", type=int)
                correct_answer_out = ""
                while correct_answers > 0:
                    correct_answer_out += f"  - \"{prompt('What is the answer?', type=str)}\"{NEW_LINE}"
                    correct_answers += -1
                new_task_yml += f"answers: \n  correct: \n{correct_answer_out}"
                incorrect_answer_out = ""
                incorrect_answers = prompt("How many incorrect answers will there be?", type=int)
                while incorrect_answers > 0:
                    incorrect_answer_out += f"  - \"{prompt('What is the wrong answer?', type=str)}\"{NEW_LINE}"
                    incorrect_answers += -1
                if "-" in incorrect_answer_out:
                    new_task_yml += incorrect_answer_out
                    new_task_yml += f"type: multi\n"
                else:
                    new_task_yml += f"type: text\n"
                new_task_yml += f"title: {new_task_name}"
            with open(f"{module_task_dir}{new_task_path}.yml", 'w') as new_task_config:
                new_task_config.write(new_task_yml)
            task_count += -1
    with open(f"{package_dir_yaml}", "w") as package_out:
        package_out.write(package_yml)
