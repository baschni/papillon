from gui.Listbox import Listbox
from gui.Textarea import Textarea
from gui.Textbox import Textbox
from gui.Button import Button
from gui.Richtext import Richtext
from gui.Iframe import Iframe
from gui.Modal import Modal
from gui.Element import Element
from gui.Popup import Popup
from gui.Gui import Gui
from init.logics_gui.prompt_settings import Prompt_Settings

def init_classes(window):
	print ("=== init inmate index ===")
	gui = Gui(window)
	gui.add(Button, "accounts_button")



