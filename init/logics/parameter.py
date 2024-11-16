from init.logics.sqlite_helper import update_bitemporal_configuration_value
from gui.Textbox import Textbox
from gui.Input import Input

class Parameter():
    def __init__(self, name, default=None, description=None, value=None, can_be_none=False):
        self.name = name
        self.default = default
        self.description = description

        self.gui_class = None
        self.id = None
        self.element = None
        self.id_conf = None


        self._value = value

        if not can_be_none and (self.default is None and self.value is None):
            raise Exception

    def get_value(self):
        if self.value is None:
            return self.default
        else:
            return self.value
    def update_value(self, Element, gui, event):
        #gui.alert("hello")
        if isinstance(self, Boolean):
            print("update", Element.value)
            self.value = 1 if Element.value else 0
        else:
            self.value = Element.value

        update_bitemporal_configuration_value(self.id_conf, self.name, self.value, self.sql_type)

    def connect_events(self):

        if self.gui_class == Textbox:
            self.element.register_event("input", self.update_value)
        else:
            self.element.register_event("change", self.update_value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.element is not None:
            self.element.value = new_value
        self._value = new_value



class Integer(Parameter):

    def __init__(self, name, default=None, range=(None, None), description=None, value=None, can_be_none=False):
        super().__init__(name, default, description, value, can_be_none)
        self.range = range
        self.sql_type = "int"


class Float(Parameter):

    def __init__(self, name, default=None, range=(None, None), description=None, value=None, can_be_none=False):
        super().__init__(name, default, description, value, can_be_none)
        self.range = range
        self.sql_type = "float"

class Text(Parameter):
    def __init__(self, name, default=None, range=(None, None), description=None, value=None, can_be_none=False):
        super().__init__(name, default, description, value, can_be_none)
        self.sql_type = "text"


class Boolean(Parameter):
    def __init__(self, name, default=None, range=(None, None), description=None, value=None, can_be_none=False):
        super().__init__(name, default, description, value, can_be_none)
        self.sql_type = "int"

