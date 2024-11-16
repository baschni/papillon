from gui.Listbox import Listbox
from gui.Textarea import Textarea
from gui.Textbox import Textbox
from gui.Button import Button
from gui.Richtext import Richtext
from gui.Iframe import Iframe
from gui.Modal import Modal
def init_classes(gui):
    gui.add(Listbox, "lb_level1")
    gui.add(Textarea, "ta_level1")
    gui.add(Textbox, "tb_level1")

    gui.add(Listbox, "lb_level2")
    gui.add(Textbox, "tb_level2")

    gui.add(Button, "btn_level1_add")
    gui.add(Button, "btn_level1_remove")
    gui.add(Button, "btn_level2_add")
    gui.add(Button, "btn_level2_remove")

    gui.add(Richtext, "rt_text")
    gui.add(Button, "btn_print_rt")

    gui.add(Iframe, "if_pdf")

    gui.add(Modal, "md_popup")
    gui.add(Button, "btn_modal")