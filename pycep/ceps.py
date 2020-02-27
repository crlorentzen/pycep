"""The pycep cep loading."""
# coding=utf-8


def get_ceps():
    """Return CEP test dict object."""
    cep_2000 = {"cep_number": "2000",
                "cep_check_type": "contentModuleExportQuestionDescriptions",
                "regex_search": "Learning Objectives:*\n*.\n.*\n.*\n",
                "log_message": "Learning Objectives: with following 3 listed items not found!"}
    cep_2006 = {"cep_number": "2006",
                "cep_check_type": "contentModuleExportQuestionDescriptions",
                "regex_search": "Toolkit:*\n*.\n"}
    cep_2007 = {"cep_number": "2007",
                "cep_check_type": "contentModuleExportQuestionDescriptions",
                "string_search": "data:image/png",
                "log_message": "A png image was not found in the introduction slide!"}
    cep_dict = {"cep2000": cep_2000, "cep2006": cep_2006, "cep2007": cep_2007}
    # TODO Build and parse from json files
    return cep_dict


CEPS = get_ceps()
