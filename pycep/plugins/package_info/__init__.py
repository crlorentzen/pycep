"""Pycep package info cli library."""
# coding=utf-8
from pycep.plugins.parser import package_export_module_info


def chelp():
    """Print click CLI help information."""
    print(f"Plugin: \n  package_info: A simple package info export plugin.\n")
    pass


def package_info(raw_data: dict):
    """Process CLI input with package_info plugin function."""
    """Process module data return package information."""
    print(package_export_module_info(raw_data))
