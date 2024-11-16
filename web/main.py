# this is a Demo file to demonstrate an easy GUI library using pywebview
# wrapping javascript inside python classes you will need no javascript to build interactive GUI
# the main.py creates a Javascript API (python functions in the python class API can be called with javascript commands)
# and will create a window based on an index.htm

import webview
from api import Api
from gui.Gui import Gui
from os import getcwd



if __name__ == '__main__':
    #abstraction
    # gui holds all the html elements and python classes for thoses elements
    # api is a python class whose functions can be called from javascript
    # the api function initialise will be called when the webbrowser and the webpage has been loaded
    # then all initialisation code from the respective modules will be executed
    # 1: init_elements: adds gui objects (e.g. listboxes, buttons, ...) to the Gui object
    # 2: init_design: css code and html attributes will be set for the created gui objects
    # 3: the program logic will be linked to the gui element's events (e.g. click on a button shall trigger a certain python function)
    print(getcwd())
    api = Api()
    window = webview.create_window("GUI demonstration", "html/index.htm", js_api=api)

    gui = Gui(window)
    api.set_gui(gui)

    # after loading of webview the api initialise function will be called from html script tag (see index.htm)
    webview.start(gui="edgechromium")

