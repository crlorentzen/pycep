# pycep Change Log

## pycep Release 0.0.1

-   Initial Release with CEP 2000, 2006 and 2007 basic linting support

## pycep Release 0.0.2

-   Dockerfile support added
-   Python documentation style fixes
-   Moved plugin to dedicated pycep library 
-   Docker documentation added

## pycep Release 0.0.3

-   Spellcheck plugin added
-   Markdown output rendering support added
-   Add user word list feature
-   Create render python library to handle data output
-   Create MANIFEST.in to include data in library install
-   Add pyspellcheck to requirements.txt
-   Move code of conduct to docs folder
-   Update arg help functions
-   Add Contributing.md to docs

## pycep Release 0.0.4

-   Updated word_list.txt with 242 new words
-   Use ujson now instead of built-in json
-   Fix spell checking bug against image data(image data shouldn't be scanned).
-   Update docs with spellcheck/render plugin example
-   Created modular spellchecking functions
-   Add line data field to spellcheck output
-   Change spellcheck output to logging output instead of using print()

## pycep Release 0.0.5

-   New info plugin to display content module information
-   Markdown out now supports table output for module information
-   New formatting python library for handling data structures
-   Added ujson for faster json processing

## pycep Release 0.0.6

-   New sentiment analysis plugin
-   Fix bug in markdown output
-   Remove cep directory for now and fix bug to allow window installs to work properly

## pycep Release 0.0.7

-   Change windows path output format to html ascii code values.

## pycep Release 0.0.8

-   Fix multiple slide imports

## pycep Release 0.0.9

-   Fix package export bug that didn't export all the tasks.

## pycep Release 0.0.10
-   Change answerkey output data to yml out replacing json out.
    - Note: This is not backwards compatible with the json format you must export from a package json or manually create
      the file.
- Add slide order and module order variables to package export data

## pycep Release 0.0.11
-   Fix latin bug parsing.
-   Implement plugin style package design for modular pycep plugin functionality.
-   Add package_questions output plugin.
-   Add 4 new words to default word_list.txt.
-   Change render plugin name to parser.
-   All plugins moved to dedicated python packages.
-   Improve the Yaml out of answerkey data