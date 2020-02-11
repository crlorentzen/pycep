"""pycep cep loading."""
# coding=utf-8


def get_ceps():
    """Return CEP test dict object."""
    cep_2000 = {"cep_number": "2000",
                "cep_check_type": "contentModuleExportQuestionDescriptions",
                "regex_search": "Learning Objectives:*\n*.\n.*\n.*\n"}
    cep_2006 = {"cep_number": "2006",
                "cep_check_type": "contentModuleExportQuestionDescriptions",
                "regex_search": "Toolkit:*\n*.\n"}
    cep_2007 = {"cep_number": "2007",
                "cep_check_type": "contentModuleExportQuestionDescriptions",
                "string_search": "data:image/png"}
    cep_dict = {"cep2000": cep_2000, "cep2006": cep_2006, "cep2007": cep_2007}
    return cep_dict


CEPS = get_ceps()
