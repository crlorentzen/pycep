import csv
from pycep.model import DIR_CHARACTER
# csv fileused id Geeks.csv

# opening the file using "with"
# statemen


def parse_hints(csvFilePath):
    # create a dictionary
    hint_data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary key
            key = rows['Number']
            hint_number = rows['HintNumber']
            if key not in hint_data:
                hint_data[key] = {}
            hint_data[key][hint_number] = rows
    return hint_data


def get_answer_data(csvFilePath):
    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary key
            try:
                key = rows['\ufeffNumber']
            except KeyError:
                key = rows['Number']
            data[key] = rows
    return data


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_dict(csvFilePath):
    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary key
            key = rows['Number']
            data[key] = rows
            try:
                del data[key]['_key']
                del data[key]['_user']
            except KeyError:
                pass
    return data


def convert_ctfd_module(input_directory):
    question_file = f"{input_directory}{DIR_CHARACTER}ctf_hints.csv"
    ctf_answers = make_dict(question_file)
    hint_file = f"{input_directory}{DIR_CHARACTER}ctf_hints.csv"
    hints = parse_hints(hint_file)
    answer_file = f"{input_directory}{DIR_CHARACTER}ctf_answers.csv"
    answer_data = get_answer_data(answer_file)
    yaml_questions = ""
    md_data = ""
    for question in ctf_answers:
        print("  - " + "\"Question " + ctf_answers[question]["Number"] + "\"")
    for question in ctf_answers:
        yaml_questions += '"Question ' + str(ctf_answers[question]["Number"]) + '":\n'
        yaml_questions += """  vmKeys: [] 
      attachments: []
      type: text
      mappingtags: []
      extradata: {}
      retrycount: 50
      pointtotal: """
        yaml_questions += ctf_answers[question]["BasePoints"]
        yaml_questions += """\n  hints: \n"""
        for hint in hints.items():
            if hint[0] == ctf_answers[question]["Number"]:
                for values in hint[1]:
                    yaml_questions += "    " + hint[1][values]["HintNumber"] + ":\n"
                    yaml_questions += "      cost: " + hint[1][values]["HintCost"] + "\n"
                    yaml_questions += "      message: \"" + hint[1][values]["Hint"] + "\"\n"
        for answer in answer_data:
            if question == answer:
                yaml_questions += """  answers:\n    correct:\n      - \"""" + answer_data[answer]["Answer"].replace('"', "'") + "\"\n"
        md_data += f"# Question {ctf_answers[question]['Number']}\n{ctf_answers[question]['Question']}\n" \
                   f"_________________________________________________________________________________________________\n"

    with open("tasks.yml", 'w') as task_yml:
        task_yml.write(yaml_questions)
    with open("tasks.md", 'w') as task_yml:
        task_yml.write(md_data)
