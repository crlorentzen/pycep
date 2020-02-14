# pycep plugin guide!

## linter plugin

The linter plugin runs configured cep checks for any errors in a package export.

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
    