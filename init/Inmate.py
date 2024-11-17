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

class Inmate(Gui): 
    def initialize(self):
        print ("=== init inmate index ===")

        self.add(Button, "profile_button")
        self.profile_button.on_click(self.print_hello)
        return self

    def print_hello(self):
        self.init.change_page("html/index.html", "Inmate")


class Inmate2(Gui): 
    def initialize(self):
        print ("=== init inmate index ===")

        self.add(Button, "profile_button")
        self.profile_button.on_click(self.print_hello)
        return self

    def print_hello(self):
        self.init.change_page("html/menu.html", "Inmate")

