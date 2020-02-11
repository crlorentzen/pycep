"""The pycep python plugin function library."""
# coding=utf-8

from logging import info
from pycep.parser import get_value, get_slide_data, cep_check


def linter(raw_data: dict):
    """Process content module for cep standards."""
    content_module_string = 'packageExportContentModules'
    package_export_content_modules = get_value(content_module_string, raw_data)[content_module_string]
    for values in package_export_content_modules:
        raw_slide_data, package_name = get_slide_data(package_export_content_modules, values)
        info(package_name + ": Processing slides with linter now!")
        cep_check(raw_slide_data, package_name)
