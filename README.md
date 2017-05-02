# Every Woman's Ground

2D No Mans Sky :)

## Installation

This game uses **Python3**, **we highly recommend using a virtual environment with Python3 as the interpreter**. 
If you are having problems installing the game, check that you aren't trying to use Python 2.x; try replacing 
`python` and `pip` with `python3` and `pip3`.

### Linux

* Install system-wide dependencies:
    * `sudo apt-get install python3-dev`
    * `sudo apt-get install swig`
    * **NB: If swig version in your distro's repositories is < 3 (check with `swig -version`) then you'll need to 
install it from [source](http://www.swig.org/download.html).** 
* Install python dependencies:
    * `pip install -r requirements.txt`

#### Box2D issue
If you get the following error when running the game then there is a problem with the Box2D package:

*AttributeError: 'module' object has no attribute 'RAND_LIMIT_swigconstant'*

To fix this, you'll need to install Box2D from source as follows:

* `cd <somedir>`
* `git clone https://github.com/pybox2d/pybox2d`
* `cd pybox2d`
* `python setup.py build`
* `python setup.py install`

### Windows

* Install Visual C++ build tools from `http://landinghub.visualstudio.com/visual-cpp-build-tools`
* Install SWIG from `http://www.swig.org/`
* Follow the "Building from source: Windows" instructions found [here](https://github.com/pybox2d/pybox2d/blob/master/INSTALL.md):
    * `git clone https://github.com/pybox2d/pybox2d`
    * `python setup.py build`
    * `python setup.py install`
* `pip install -r requirements.txt`

## Running the game

Simply run the `game.py` module.

* `python game.py`
