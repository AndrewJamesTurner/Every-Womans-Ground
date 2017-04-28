# Every-Womans-Ground
2D No Mans Sky :)

## Idea ##

Three phases to the game:

1. 2D space travel like asteroids
Can land on planets

2. 2D landing
Triggered when landing on, or leaving planet

3. 2D world to walk around
Can walk around
Can leave planet

This can be separated into effectively three mini games which will be great for parallelizing our time. The details of each mini game can be decided by who ever is working on it.

Overall game could be to leave earth with some fuel, have to get collected things back home. Things / more fuel can be gathered some how.

## Tech ##

### lang ###
Python (we all know it and its quick for throwing things together)

### libs ###
pygame / EzPyGame (handles drawing to screen, consolers etc, very simple to use, uses SDL2 underneath)

if we need physics pybox2d (very simple good 2D physics engine, uses box2d underneath)

### install linux ###
* `sudo apt-get install swig`
* `sudo apt-get install python-box2d`
* `sudo apt-get install python3-dev`
* `pip install box2d`
* `sudo pip3 install -r requirements.txt`

### install windows ###
* Install Visual C++ build tools from `http://landinghub.visualstudio.com/visual-cpp-build-tools`
* Install SWIG from `http://www.swig.org/`
* Follow the "Building from source: Windows" instructions from `https://github.com/pybox2d/pybox2d/blob/master/INSTALL.md`
    * `git clone https://github.com/pybox2d/pybox2d`
    * `python setup.py build`
    * `python setup.py install`
* `sudo pip3 install -r requirements.txt`

### run the game ###

* `python3 game.py`
