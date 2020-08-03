"""Pycep package compile cli library."""
# coding=utf-8
from logging import info
from pycep.model import compile_package_data


def load(raw_data: dict,
         plugin,
         file_type,
         output: str,
         word_list,
         input_directory,
         export_dir,
         owner_id,
         input_file):
    """Process CLI input with compile plugin function."""
    render = markdown_in
    return render(raw_data,
                  plugin,
                  file_type,
                  output,
                  word_list,
                  input_directory,
                  export_dir,
                  owner_id,
                  input_file)


def chelp():
    print(f"Plugin: \n  compile: A package render from markdown to package export plugin.\n")
    pass


def markdown_in(raw_data: dict,
                plugin: str,
                file_type: str,
                output: str,
                word_list: str,
                input_directory: str,
                export_dir: str,
                owner_id: str,
                input_file: str):
    """Create archive file in package_export format, from markdown + yaml input."""
    info("Compiling package export now with the markdown_in plugin now!")
    compile_package_data(output, input_directory, export_dir, owner_id, input_file)


