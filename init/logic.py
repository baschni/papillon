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

from init.logics_gui.core import display_conversations

GUI = None



#file_mapping = {}
from os import scandir, mkdir
from os.path import join, splitext, isdir
from shutil import copyfile

def init_logic(gui):
    print("== init logic ==")
    GUI = gui


    display_conversations(gui)


def get_gui():
    global GUI
    return GUI

