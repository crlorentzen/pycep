"""The pycep python output function library."""
# coding=utf-8
import tarfile

from sys import exit
from logging import error


def write_to_file(input_file_name: str, string_data: str) -> None:
    """Write string data with input file path."""
    with open(input_file_name, 'w') as output_file:
        output_file.write(string_data)


def extract_tar_file(file_name: str) -> str:
    """Extract tar gz file from input file_name string."""
    try:
        tar_file = tarfile.open(file_name, mode="r:gz")
        json_file = tar_file.extractfile("package_export.json")
        return json_file.read()
    except tarfile.ReadError:
        error(f"Input file {file_name} is not a proper tar.gz exiting now.\n Please correct the file_type input.")
        exit(1)
