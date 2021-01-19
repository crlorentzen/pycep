# Pre-req

## Ubuntu 16.04 + package install

    sudo apt-get install python3-dev python3-setuptools


    sudo apt-get install libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
        libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
        libharfbuzz-dev libfribidi-dev libxcb1-dev


## Mac OSX package install

* Pycep requires some libraries which your system may not have. Below is the command to install these libraries using [Homebrew](https://brew.sh/)  
`brew install libtiff libjpeg webp little-cms2 freetype harfbuzz fribidi`

* Install mkvirtualenvwrapper  
`sudo pip3 install mkvirtualenvwrapper`

* Add the virtualenvwrapper setup scripts to your Terminal's rc file  
```
if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
  export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
  export WORKON_HOME=$HOME/.virtualenvs
  export PROJECT_HOME=$HOME/Devel
  source /usr/local/bin/virtualenvwrapper.sh
fi
```

* Create or open the pycep virtual environment  
`mkvirtualenv pycep` or `workon pycep`

* Return to the [Pip Install](/README.md#pip-install) section of the README
