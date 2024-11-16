from gui.Listbox import Listbox
from gui.Textarea import Textarea
from gui.Textbox import Textbox
from gui.Button import Button
from gui.Richtext import Richtext
from gui.Iframe import Iframe
from gui.Modal import Modal
from gui.Element import Element
from gui.Popup import Popup
from init.logics_gui.prompt_settings import Prompt_Settings

def init_classes(gui):
    print ("=== init classes ===")

    gui.add(Element, "left")
    gui.add(Listbox, "lb_conversations")
    gui.add(Button, "btn_add_conversation")
    gui.add(Button, "btn_remove_conversation")


    gui.add(Element, "right")
    gui.add(Element, "header")
    gui.add(Element, "conversation")
    gui.add(Element, "input")

    gui.add(Textbox, "tb_prompt")
    gui.add(Button, "btn_prompt_settings")
    gui.add(Button, "btn_prompt_history")
    gui.add(Button, "btn_toggle_prompt_height")
    gui.add(Button, "btn_send_prompt")
    gui.add(Button, "btn_clear_prompt")
    gui.add(Button, "btn_redo_change")
    gui.add(Button, "btn_undo_change")

    gui.add(Popup, "prompt_history")
    gui.add(Prompt_Settings, "prompt_settings")
    #gui.prompt_settings.add()



