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

    Usage: cepcli.py [OPTIONS]
    
      Pycep Command line interface.
    
    Options:
      -f, --input_file TEXT  The Package export tar.gz or the json file .
                             [required]
      -t, --file_type TEXT   Input File type format json/tar.gz.
      -o, --output TEXT      Output file directory.
      -w, --word_list TEXT   Input spelling word list.
      -p, --plugin TEXT      Plugin for pycep to run.  [required]
      -d, --debug            Turn debug mode on.
      --version              Print Application Version
      --help                 Show this message and exit.


For more information on plugins please see [Plugin Guide](docs/PLUGINS.md)

## Current Features

-   File type support for json/tar.gz 
-   Modular python linter functionality 
-   Verbose logging output with debug mode
-   Basic cep linter support for CEP 2000, 2006, and 2007
-   Automatic requirement document support linking for failed tests
-   Process timestamp output in debug mode
-   Package Export level processing 
-   Version 8+ Package module exports
-   Docker support
-   From package export format to Markdown
-   Spellcheck

### Coming Soon!

-   From Markdown format to package export
-   Plagiarism Check
-   Reading level score
-   ML based NIST(an other framework) tagging
-   More CEP checks
-   Unit tests code coverage

## Contributing  

See the official guidelines [here](docs/CONTRIBUTING.md)!

## Code of Conduct 
In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

Please read the full [Code of Conduct](docs/CODE-OF-CONDUCT.md)!