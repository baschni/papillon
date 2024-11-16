from gui.Element import Element
from json import dumps as j

class Textarea(Element):

    def __getattribute__(self, item):
        if item == "value":
            elements = self.get_elements()
            # return elements["value"] if "value" in elements else ""
            return elements.value
        else:
            return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if key=="value":
            self.js(f"document.getElementById({j(self.id)}).value = {j(value)}")
        else:
            super().__setattr__(key, value)