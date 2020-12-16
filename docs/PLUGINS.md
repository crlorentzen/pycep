# pycep plugin guide!

## linter plugin

The linter plugin runs configured cep checks for any errors in a package export.

### Use pycep linter plugin against tar.gz export

When not using the default mode with the linter plugin only CEP checks that don't pass will be displayed to stdout

    cepcli.py -f examplepackage.tar.gz -p linter 
    
    ERROR:root:ELSA 0.0.0: Example pycep package content module name: CEP 2006 Test Failed! | More info: https://simspace.github.io/cep/ceps/2006/#requirements

### Use pycep linter plugin against tar.gz export in debug mode

When using the debug flag -d or --debug pycep will show debug level logging information and even display which ceps passed.

    cepcli.py -f Demo_Package_export.tar.gz -p linter -d
    
    Debug mode is on
    Process Time: 2020-02-11 12:40:21 | pycep linter plugin running now...
    Process Time: 2020-02-11 12:40:21 | ELSA 0.0.0: Example pycep package content module name: Rendering 10 sasks into raw data.
    Process Time: 2020-02-11 12:40:21 | ELSA 0.0.0: Example pycep package content module name: Processing sasks with linter now!
    Process Time: 2020-02-11 12:40:21 | ELSA 0.0.0: Example pycep package content module name: CEP 2000 - Passed
    Process Time: 2020-02-11 12:40:21 | ELSA 0.0.0: Example pycep package content module name: CEP 2006 Test Failed! | More info: https://simspace.github.io/cep/ceps/2006/#requirements
    Process Time: 2020-02-11 12:40:21 | ELSA 0.0.0: Example pycep package content module name: CEP 2007 - Passed


## spellcheck plugin
The spellcheck plugin searches for errors using a default spelling word list included in pycep/data/word_list.txt.

### How to use the spellcheck plugin against tar.gz export

    cepcli.py --plugin spellcheck --input_file Demo_Package_export.tar.gz 
    
    ERROR:root:Content Module Name: Training Demo: Introduction to Pycep
    Task Title: How to use spellcheck
    Line Number: 1
    Line Data:     volatilty is misspelled 
    Spelling Error: volatilty
    Suggested replacement: volatility

### How to use the spellcheck plugin against tar.gz export with custom word list

    cepcli.pp --plugin spellcheck --input_file Demo_Package_export.tar.gz --word_list /path/to/example_word_list.txt


## Parser plugin

The Parser plugin only supports exporting a package export json tar.gz file into a markdown output by default. It could be easy to implement a html output format as well and convert markdown back to export package portal format.

    cepcli.py -f Demo_Package_export.tar.gz -p parser -o /path/to/export/dir/


## Info plugin

The info plugin prints basic information about modules.

    cepcli.py -f Demo_Package_export.tar.gz -p package_info


## Compile Package plugin

The compile plugin compiles a package directory into an export package tar.gz format.

    cepcli.py -f package_module_directory -p compile -o package_module_export.tar.gz


## Task Question plugin

The info plugin prints basic information about modules.

    cepcli.py -f Demo_Package_export.tar.gz -p package_questions



## Mapping Tags plugin

Currently, the info plugin prints the mapping tags attached to a module in yaml output.

    cepcli.py -f Demo_Package_export.tar.gz -p mapping_tags


## Convert Plugin

The convert plugin currently supports ctfd formatted export of csv data as the input directory. It will take the csv files
and create a tasks.md and tasks.yml for the input data. Other SCP structure data will not be generated at this time

    cepcli.py -g /path/to/my/ctfd/dir/ 

