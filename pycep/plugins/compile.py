from logging import info
from pycep.model import compile_package_data


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
