from gui.Popup import Popup
from gui.Textbox import Textbox
from gui.Listbox import Listbox
from gui.Button import Button

from init.logics.sql_queries import add_new_configuration

class Add_prompt_configuration(Popup):

    def __init__(self, id, gui):
        super().__init__(id, gui, "Konfiguration hinzufügen",draggable=True)

        self.add(Textbox,"tb_configuration_name")
        self.add(Listbox,"lb_available_models")
        self.add(Button,"btn_confirm_add_configuration")
        self.add(Button,"btn_cancel_add_configuration")


        self.load_available_configurations()



        self.btn_confirm_add_configuration.on_click(self.add_configuration)
        self.btn_cancel_add_configuration.on_click(self.hide)

    def load_available_configurations(self):
        models = [
            "meta/meta-llama-3-70b-instruct",
            "meta/meta-llama-3.1-405b-instruct"
        ]
        self.lb_available_models.load_dictionary({"model": models}, keys_to_display=["model"])

    def show(self):
        #id_conf = self.parent.lb_configurations.get_selected_data("id_conv")
        self.tb_configuration_name.value = ""

        super().show()

    def add_configuration(self):
        name = self.tb_configuration_name.value
        if name == "":
            self.gui.alert("Bitte geben Sie einen Namen für die neue Konfiguration ein.")
        else:
            id_conf = add_new_configuration(name, self.lb_available_models.get_selected_data("model"))

            self.parent.reload_and_select_configuration(id_conf)
            self.hide()
