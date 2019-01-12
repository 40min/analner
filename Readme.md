
##Installation

* from src
    * clone this repo
    * run
``` pip install -r ./requirements.txt ```
    * setup environment variables
        * DATA_PATH -- dir where will be stored text headers and models in json
        * DROPBOX_TOKEN -- token of dropbox account to backup headers-files

* as pip pkg from git:
    * pip install -e git+https://github.com/40min/analner.git@master#egg=analner

## ToDo

* see https://github.com/GuyAglionby/chatsimulatorbot
* try combine:
    Combining models https://github.com/jsvine/markovify#combining-models
* split model json files by months
* create new files with ok phrases
* try to del bad phrases

* bugfix: add ability to setup custom dropbox folder