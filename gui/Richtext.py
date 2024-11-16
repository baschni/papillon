from gui.Element import Element
from json import dumps as j
class Richtext(Element):

    def __getattribute__(self, item):
        if item =="innerHTML":
            return self.get_elements()[item]
        else:
            return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if key=="innerHTML":
            self.js(f"document.getElementById({j(self.id)}).value = {j(value)}")
        else:
            super().__setattr__(key, value)