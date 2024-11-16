# this is a Demo file to demonstrate an easy GUI library using pywebview
# wrapping javascript inside python classes you will need no javascript to build interactive GUI
# the main.py creates a Javascript API (python functions in the python class API can be called with javascript commands)
# and will create a window based on an index.htm

# all local files (images for img tag, html for iframe) can only be loaded from the folder or subfolders of where the index htm is lying!

import sys
#alternative to modify $PYTHONPATH
#sys.path.append("C:\\Users\\basch\\Documents\\01 Python\\webview")
import webview
from os import getcwd
import os
from screeninfo import get_monitors
from shutil import copyfile
from api import Api
from gui.Gui import Gui
from os import path
from config import HTML_BASE_FOLDER

INDEX_HTML = path.join(HTML_BASE_FOLDER,"index.htm")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    #abstraction
    # gui holds all the html elements and python classes for thoses elements
    # api is a python class whose functions can be called from javascript
    # the api function initialise will be called when the webbrowser and the webpage has been loaded
    # then all initialisation code from the respective modules will be executed
    # 1: init_elements: adds gui objects (e.g. listboxes, buttons, ...) to the Gui object
    # 2: init_design: css code and html attributes will be set for the created gui objects
    # 3: the program logics will be linked to the gui element's events (e.g. click on a button shall trigger a certain python function)
    print(getcwd())
    #api = Api()
    for monitor in get_monitors():
        pass

    # copying index.htm to base folder so that iframe can access all pdf relative to this base folder
    #target_path = path.join(PDF_BASE_FOLDER,".index.htm")
    #copyfile("html/index.htm", target_path)
    #target_path="html/index.htm"
    window = webview.create_window("Prison system", INDEX_HTML, width=monitor.width, height=monitor.height, maximized=True)
    #js_api=api,
    gui = Gui(window)
    #api.set_gui(window)
    #window.js_api_endpoint = api
    print ("=== start webview ===")
    # after loading of webview the api initialise function will be called from html script tag (see index.htm)
    webview.start(gui.initialize, gui="edgechromium")

