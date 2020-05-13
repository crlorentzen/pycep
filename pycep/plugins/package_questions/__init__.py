"""Pycep package question cli library."""
# coding=utf-8
from pycep.plugins.parser import package_export_question_info


def chelp():
    """Print click CLI help information."""
    print(f"Plugin: \n  package_questions: A package task question simple export plugin.\n")
    pass


def load(input_data, plugin, file_type, output, word_list, input_directory, export_dir, owner_id):
    """Process CLI input with package_questions plugin function."""
    return package_questions(input_data, plugin, file_type, output, word_list, input_directory, export_dir, owner_id)


def package_questions(raw_data: dict, plugin, file_type, output, word_list, input_directory, export_dir, owner_id):
    """Return package question data."""
    data = package_export_question_info(raw_data)
    for item in data:
        print(f"Content Module: {item} ")
        for value in data[item]:
            for tasks in value:
                if "question" in tasks['val']:
                    print(f"\n  TaskTitle: {tasks['val']['title']}")
                    print(f"  PointTotal: {tasks['val']['question']['points']}")
                    print(f"  RetryCount: {tasks['val']['question']['retryCount']}")
                    answer_number = 0
                    answer_data = ""
                    for answers in tasks['val']['question']["choices"]:
                        if answers["correct"] is True:
                            answer_number += 1
                            answer_data += f"    Answer {answer_number}: {answers['value']}\n"
                    print(answer_data[:-1])
                    hint_number = 0
                    hints_data = ""
                    for hints in tasks['val']['question']["hints"]:
                        hint_number += 1
                        hints_data += f"    Hint{hint_number}:\n"
                        hints_data += f"      Cost: {hints['pointsDeduction']}\n"
                        hint_text = hints['text'].replace('\n', "\n               ")
                        hints_data += f"      Message: \"{hint_text}\" \n"
                    print(hints_data[:-1])
        print(f"\n")
