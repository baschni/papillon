from gui.Popup import Popup
from gui.Listbox import Listbox
from gui.Button import Button
from gui.Element import Element
from init.logics.sql_queries import get_configurations, set_configuration_id_for_conversation,get_configuration_id_for_conversation, get_configuration_object, remove_configuration
from init.logics_gui.add_prompt_configuration import Add_prompt_configuration
class Prompt_Settings(Popup):

    def __init__(self, id, gui):
        super().__init__(id, gui, "Modell-Konfigurationen",draggable=True)

        self.conv_id = None
        self.id_conf = None

        self.add(Listbox,"prompt_settings_lb_configurations")
        self.add(Button,"prompt_settings_btn_add_configuration")
        self.add(Button,"prompt_settings_btn_remove_configuration")
        self.add(Element,"prompt_settings_div_left")
        self.add(Element,"prompt_settings_div_right")

        self.ids_not_to_erase.append("prompt_setting_div_left")
        self.ids_not_to_erase.append("prompt_settings_div_right")
        self.div_right.load_css("""
            overflow-y: scroll;
        """)
        self.ids_not_to_erase.append("prompt_settings_btn_add_configuration")

        self.init_add_prompt_popup()

        self.btn_add_configuration.on_click(self.pop_add_prompt_configuration.show)
        self.btn_remove_configuration.on_click(self.remove_configuration)
        self.lb_configurations.register_event("change",self.show_configuration)

        self.parameter_elements = {}



    def init_add_prompt_popup(self):
        self.add(Add_prompt_configuration, "pop_add_prompt_configuration")
        css = """
            width: 30%;
            height: 20%;
            position: absolute;
            left: 50%;
            top: 50%;
            translate: (-50%,-50%)
        """
        self.pop_add_prompt_configuration.load_css(css)
    def remove_configuration(self, gui):
        gui.alert("remove")
        if self.id_conf is not None:
            remove_configuration(self.id_conf)

    def show(self, id_conv=None):
        #reload listbox
        self.id_conv = id_conv
        configurations = get_configurations()
        self.lb_configurations.load_dictionary(configurations, keys_to_display=["name"])

        #select configuration for current prompt
        if id_conv is not None:
            id_conf = get_configuration_id_for_conversation(id_conv)
            #print("select configuration in listbox", id_conf)
            self.lb_configurations.set_selected({"id_conf": id_conf})

        #super show
        #print("parent show function of event")
        super().show()

    def reload_and_select_configuration(self, id_conf):
        configurations = get_configurations()
        self.lb_configurations.load_dictionary(configurations, keys_to_display=["name"])
        self.lb_configurations.set_selected({"id_conf": id_conf})

    def show_configuration(self, gui):
        id_conf = self.id_conf = self.lb_configurations.get_selected_data("id_conf")

        if id_conf is not None and self.id_conv is not None:
            set_configuration_id_for_conversation(id_conf, self.id_conv)

        if id_conf is not None:
            config = get_configuration_object(id_conf)
            #self.div_right.innerHTML = ""
            self.div_right.innerHTML = config.layout_parameters(self.id)
            #print("connect parameter events ", id_conf)
            config.connect_parameter_events(gui)



