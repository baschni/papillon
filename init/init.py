# from webview import FOLDER_DIALOG
# from config import VALID_CHARACTERS_IN_FILENAME
# from init.logics.file_mapping_csv import read_directory_mapping, write_directory_mapping
# from openpyxl.workbook import Workbook
#
# from datetime import datetime
# from os import getcwd, path
# import subprocess
# import shlex
#
#
# #from debug_timer import Timer
# import pytesseract
# import cv2
#
# import re
# import shutil
#from main import WINDOW
from init.Inmate import Inmate, Inmate2



#file_mapping = {}
from os import scandir, mkdir
from os.path import join, splitext, isdir
from shutil import copyfile

class Init():
    def __init__(self, window):
        self.window = window
        self.gui_class = Inmate

    def init(self):
        print("== init logic ==")
        self.gui = self.gui_class(self.window, self)
        self.gui.initialize()
    
    def change_page(self, html, gui_class_id):
        self.gui.unregister_events()
        self.gui_class = self.get_gui_class(gui_class_id)
        self.window.load_url(html)
        self.gui = self.gui_class(self.window, self)
        self.gui.initialize()

    def get_gui_class(self, id):
        if id == "Inmate":
            return Inmate
        elif id == "Inmate2":
            return Inmate2
        else:
            return None

    # window.expose(self.trigger_event)


    # display_conversations(gui)


# def get_gui():
#     global GUI
#     return GUI

