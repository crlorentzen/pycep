# PYCEP

The main goal of this project is to bring basic content checking features in a python 3.7+ library that enabled content developers to automate as much of their QA process as possible.

## Install pycep

### pip coming soon!

### Install from source

    git clone https://github.com/SimSpace/pycep/
    cd pycep 
    python setup.py install

## Basic pycep CLI usage

### Example cli help output

    cepcli.py --help
    Usage: cepcli.py [OPTIONS]
    
    Options:
      -f, --input_file TEXT  The Package export tar.gz file.  [required]
      -t, --file_type TEXT   Input File type format json/tar.gz .
      -p, --plugin TEXT      pycep function to run.  [required]
      -d, --debug            pycep function to run.
      --version
      --help                 Show this message and exit.

### Use pycep linter plugin against tar.gz export
When not using the default mode with the linter plugin only CEP checks that don't pass will be displayed to stdout

    cepcli.py -f examplepackage.tar.gz -p linter 
    
    ERROR:root:ELSA 0.0.0: Example pycep package content module name: CEP 2006 Test Failed! | More info: https://simspace.github.io/cep/ceps/2006/#requirements

### Use pycep linter plugin against tar.gz export in debug mode
When using the debug flag -d or --debug pycep will show debug level logging information and even display which ceps passed.

    cepcli.py -f examplepackage.tar.gz -p linter -d
    
    Debug mode is on
    Process Time: 2020-02-11 12:40:21 | pycep linter plugin running now...
    Process Time: 2020-02-11 12:40:21 | ELSA 0.0.0: Example pycep package content module name: Rendering 10 slides into raw data.
    Process Time: 2020-02-11 12:40:21 | ELSA 0.0.0: Example pycep package content module name: Processing slides with linter now!
    Process Time: 2020-02-11 12:40:21 | ELSA 0.0.0: Example pycep package content module name: CEP 2000 - Passed
    Process Time: 2020-02-11 12:40:21 | ELSA 0.0.0: Example pycep package content module name: CEP 2006 Test Failed! | More info: https://simspace.github.io/cep/ceps/2006/#requirements
    Process Time: 2020-02-11 12:40:21 | ELSA 0.0.0: Example pycep package content module name: CEP 2007 - Passed
    
## Current Features

-   File type support for json/tar.gz 
-   Modular python linter functionality 
-   Verbose logging output with debug mode
-   Basic cep linter support for CEP 2000, 2006, and 2007
-   Automatic requirement document support linking for failed tests

### Coming Soon!

-   Markdown formatting to/from
-   Spellcheck
-   Plagiarism Check
-   Reading level score
-   ML based NIST(an other framework) tagging
-   More CEP checks
-   Unit tests code coverage