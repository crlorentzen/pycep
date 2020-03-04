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