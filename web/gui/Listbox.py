from gui.Element import Element
from json import dumps as j
import time
from debug_timer import Timer

class Listbox(Element):

    def __init__(self, id, gui):
        super().__init__(id, gui)
        self.selected_index = None
        #self.allow_multiple_selected = bool(self.get_elements()["multiple"])
        self.allow_multiple_selected = bool(self.gui.window.dom.get_elements("#"+id)[0].node["multiple"])

        def set_selected_index_from_html(element, gui, info):
            #print("set lb index event")
            self.selected_index = int(self.js(f"document.getElementById({j(self.id)}).selectedIndex"))



        self.register_event("change", set_selected_index_from_html)

    # def update_selected(self):
    #     self.selected = self.init_selected()
    def load_dictionary(self, data, keys_to_display, id_to_select=None):

        self.key_to_display = None
        if not isinstance(keys_to_display, list):
            raise Exception("keys_to_display must be of type list!")

        self.keys_to_display = keys_to_display

        self.data = []
        for index, __ in enumerate(list(data.values())[0]):
            idict = {key: data[key][index] for key in data.keys()}
            #print(idict)
            self.data.append(idict)


        selected_before = self.get_selected()
        self.display_data()

        if (id_to_select is None and selected_before is not None) or len(list(data.values())[0]) == 0:
            # no item selected but new data has been loaded so dispatch change Event
            self.js(f"document.getElementById({j(self.id)}).dispatchEvent(new Event('change'));")
        else:
            self.set_selected(0 if id_to_select is None else id_to_select)

    def load_list(self, data, id_to_select=None):

        self.key_to_display = "default"
        self.data = [{self.key_to_display: value} for value in data]
        selected_before = self.get_selected()

        self.display_data()

        if (id_to_select is None and selected_before is not None) or len(data) == 0:
            self.js(f"document.getElementById({j(self.id)}).dispatchEvent(new Event('change'));")
        else:
            self.set_selected(0 if id_to_select is None else id_to_select)

    def empty(self, suppress_change_event=False):
        self.selected_index = None
        script = f"document.getElementById({j(self.id)}).innerHTML = '';"
        if not suppress_change_event:
            script += f"document.getElementById({j(self.id)}).dispatchEvent(new Event('change'));"
        self.js(script)
        self.data = []

    def allow_multiple_select(self):
        self.html_attr("multiple", True)
        self.allow_multiple_selected = True
    def disable_multiple_select(self):
        self.html_attr("multiple", False)
        self.allow_multiple_selected = False
    def multiple_select_allowed(self):
        return self.allow_multiple_selected

    def select_previous(self):

        if not self.multiple_select_allowed():
            selected = self.get_selected()
            if selected is not None and selected != 0:
                self.set_selected(selected - 1)

    def select_next(self):
        t = self.t = Timer("select_next", True)

        if not self.multiple_select_allowed():
            selected = self.get_selected()
            t.print("got selected")

            max_id = len(self.data) - 1

            if selected is not None and selected < max_id:
                self.set_selected(selected + 1)
                t.print("set selected")

    def set_data(self, value, key=None, id=None):
        if key is None:
            if self.key_to_display is not None:
                key = self.key_to_display

        if id==None:
            selected = self.get_selected()
        else:
            selected = id

        if key is not None and selected is not None:
            self.data[selected][key]= value
    def get_data(self, index, key=None):
        t = Timer("=== get data", True)
        if key is None:
            if self.key_to_display is not None:
                key = self.key_to_display
            else:
                return None

        t.print("=== checked if key is none")
        if len(self.data)==0:
            return None

        if key=="#selected":
            return index
        else:
            if self.multiple_select_allowed():
                if type(key) is list:
                    rdata = []
                    for i in index:
                        idata = self.data[index]
                    return [idata[subkey] if subkey != "#selected" else i for subkey in key]
                else:
                    return [self.data[selected][key] for selected in index]
            else:

                if type(key) is list:
                    t.print("=== key is list")
                    idata = self.data[index]
                    t.print("=== got idict for data")
                    result = [idata[subkey] if subkey != "#selected" else index for subkey in key]

                    t.print("=== result calculated")
                    return result
                else:
                    t.print("=== key is single")
                    data = self.data[index][key]
                    t.print("=== single key data got")
                    return data

    # def get_select(self):
    #     return self.selected
    def get_selected(self):

        t = Timer("==== get_selected", True)


        if self.multiple_select_allowed():
            info = self.get_elements()


            selected = [i for i, child in enumerate(info["childNodes"]) if child["selected"] == True]
            return None if selected == [] else selected
        else:
            t.print("self index is " + str(self.selected_index))
            return self.selected_index
            #index = self.js(f"document.getElementById({j(self.id)}).selectedIndex")
            #return index



    def get_selected_data(self, key=None):

        t = Timer("=== start get selected data ===", True)
        selected = self.get_selected()
        t.print("== got selected index")

        if selected == None:
            return None
        else:

            return self.get_data(selected, key)
            t.print("== got selected data")

    def unselect_all(self):
        self.selected_index = None
        pass

    def reload_data(self, suppress_change_event=False, select_index_afterwards = -1, suppress_select_event=False):

        if select_index_afterwards == -1:
            selected_previously = self.get_selected()
        else:
            selected_previously = select_index_afterwards

        self.display_data()
        if not suppress_select_event:
            self.set_selected(selected_previously, suppress_change_event)



    def set_selected(self, id_to_select, suppress_change_event=False):
        if hasattr(self, "t") and self.t is not None:
            t = self.t
        else:
            t = Timer("no change next", True)

        if id_to_select is not None:

            if self.multiple_select_allowed():

                self.unselect_all()
                if type(id_to_select) == "List":
                    for index in id_to_select:
                        self.set_selected(index, suppress_change_event=True)

                    self.js(f"document.getElementById({j(self.id)}).dispatchEvent(new Event('change'));")
            else:
                if isinstance(id_to_select, dict):
                    new_id_to_select = 0

                    #user passed dictionary of conditions to search for
                    for new_id_to_select, data_dict in enumerate(self.data):
                        conditions = [data_dict[needle] == value for needle, value in id_to_select.items()]
                        if False not in conditions:
                            break

                    id_to_select = new_id_to_select


                if id_to_select >= 0 and id_to_select < len(self.data):

                    self.selected_index = id_to_select
                    js = f"document.getElementById({j(self.id)}).value = {j(id_to_select)};"

                    if not suppress_change_event:
                        js += f"document.getElementById({j(self.id)}).dispatchEvent(new Event('change'));"
                        t.print("js has change event")
                    self.js(js)
                    t.print("javascript to change selected value and trigger change event executed")


    def display_data(self):
        # for every element in data create option and add it to current select
        # self.view.evaluate_js("alert('hello world')")
        if self.key_to_display is not None:
            script = f"document.getElementById({j(self.id)}).innerHTML = '';"
            for i, vals in enumerate(self.data):
                val = str(vals[self.key_to_display])
                script += f"""
                element = document.createElement("option");
                element.innerHTML = {j(val)};
                element.value = {j(i)};
                document.getElementById({j(self.id)}).appendChild(element);
                """
        else:
            script = f"document.getElementById({j(self.id)}).innerHTML = '';"
            for i, val in enumerate(self.data):

                script += f"""
                            element = document.createElement("option");
                            element.innerHTML = {j("&nbsp;|&nbsp;".join([str(val[key]) for key in self.keys_to_display]))};
                            element.value = {j(i)};
                            document.getElementById({j(self.id)}).appendChild(element);
                            """

        self.js(script)


