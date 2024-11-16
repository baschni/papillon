from gui.Element import Element
from json import dumps as j
import time
class Input(Element):

    def __init__(self, id, gui):
        super().__init__(id, gui)
        #self.html_attr("input", "text")
        #self.__setattr__("value", )


    def __getattribute__(self, item):
        if item == "value":
            elements = self.get_elements()
            # return elements["value"] if "value" in elements else ""
            if elements.node["type"] == "checkbox":

                return elements.node["checked"]
            else:
                return elements.value
        else:
            return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if key=="value":
            self.js(f"document.getElementById({j(self.id)}).value = {j(value)}")
        else:
            super().__setattr__(key, value)

    def focus(self, trigger_event=True):
        start = time.time()
        self.js(f"document.getElementById({j(self.id)}).focus()")
        print("--- Element looked up and focused", (time2 := time.time())-start)
        if trigger_event:
            print("----- trigger event true")
            if "focus" in self.event_functions:
                print("------- focus event set")
                self.event_functions["focus"](self, self.gui, {})
        print("--- Checked event functions", (time3 := time.time())-time2)

    def focus_on_beginning(self, trigger_event=True):

        self.js(f"document.getElementById({j(self.id)}).setSelectionRange(0,0)")
        self.focus(trigger_event)
        # if trigger_event:
        #
        #     if "focus" in self.event_functions:
        #
        #         self.event_functions["focus"](self, self.gui, {})
