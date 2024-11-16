from gui.Listbox import Listbox
from gui.Button import Button

data = {
    "entry1": ["testvalue1", "testtext1", {"entry1-1": "testvalue1-1", "entry1-2": "testvalue1-2", "entry1-3": "testvalue1-3"}],
    "entry2": ["testvalue2", "testtext2", {"entry2-1": "testvalue2-1", "entry2-2": "testvalue2-2", "entry2-3": "testvalue2-3"}],
    "entry3": ["testvalue3", "testtext3", {"entry3-1": "testvalue3-1", "entry3-2": "testvalue3-2", "entry3-3": "testvalue3-3"}]
}

def init_logic(gui):
    gui.lb_level1.register_event("change", select_level1)
    gui.lb_level2.register_event("change", select_level2)

    gui.lb_level1.load_list(list(data.keys()), 0)

    gui.btn_level1_add.register_event("click", add_level1)
    gui.btn_level1_remove.register_event("click", remove_level1)
    gui.btn_level2_add.register_event("click", add_level2)
    gui.btn_level2_remove.register_event("click", remove_level2)

    gui.btn_print_rt.register_event("click", print_rt)

    gui.btn_modal.on_click(event(gui.md_popup.show))
    gui.md_popup.title = "Test Popup"

    #gui.if_pdf.html_attr("src","file:///C:\\Users\\basch\\Documents\\webview\\resources\\amende.pdf")
    #gui.if_pdf.html_attr("src","file:///C:/Users/basch/Documents/webview/resources/amende.pdf")

def event(func):
    def arg_func(element, gui):
        func()

    return arg_func

def print_rt(element, gui):
    print(gui.rt_text.innerHTML)
def empty_level1_and_level2(gui):
    gui.tb_level1.value = ""
    gui.ta_level1.value = ""
    empty_level2(gui)

def empty_level2(gui):
    gui.lb_level2.empty(suppress_change_event=True)
    gui.tb_level2.value = ""

def select_level1(element: Listbox, gui):

    selected = element.get_selected_data()
    if selected in data and selected is not None:
        subdata = data[selected]

        gui.tb_level1.value = subdata[0]
        gui.ta_level1.value = subdata[1]

        gui.lb_level2.load_list(list(subdata[2].keys()),0)
    else:
        empty_level1_and_level2(gui)


def select_level2(element: Listbox, gui):
    level1_selected = gui.lb_level1.get_selected_data()

    level2_selected = gui.lb_level2.get_selected_data()

    if level2_selected is not None and level2_selected in data[level1_selected][2]:
        subdata = data[level1_selected][2][level2_selected]
        gui.tb_level2.value = subdata
    else:
        empty_level2(gui)

def add_level1(btn: Button, gui):
    input = gui.prompt("Neuer Eintrag:")

    if input is not None and input != "":

        if input in data:
            gui.alert("Eintrag existiert bereits!")
        else:
            data[input] = ["", "", dict()]
            gui.lb_level1.load_list(list(data.keys()), len(data) - 1)

def remove_level1(btn: Button, gui):
    index = gui.lb_level1.get_selected()
    selected = gui.lb_level1.get_selected_data()
    del data[selected]
    gui.lb_level1.load_list(list(data.keys()), max(0,index-1))

def add_level2(btn: Button, gui):
    input = gui.prompt("Neuer Eintrag:")

    if input is not None and input != "":
        subdata = data[gui.lb_level1.get_selected_data()][2]
        if input in subdata:
            gui.alert("Eintrag existiert bereits!")
        else:
            subdata[input] = ""
            gui.lb_level2.load_list(list(subdata.keys()), len(subdata) - 1)

def remove_level2(btn: Button, gui):
    index = gui.lb_level2.get_selected()
    selected = gui.lb_level2.get_selected_data()
    subdata = data[gui.lb_level1.get_selected_data()][2]
    del subdata[selected]
    gui.lb_level2.load_list(list(subdata.keys()), max(index-1, 0))



