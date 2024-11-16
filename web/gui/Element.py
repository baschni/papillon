from multipledispatch import dispatch
from inspect import signature
from json import dumps as j
from threading import Thread

class InnerHTML():

    def __init__(self):
        pass

    def __iadd__(self, instance, html):
        instance.append_html(html)

    def __get__(self, instance, owner):
        elements = instance.get_elements()
        if "innerHTML" in elements.node:
            return elements.node["innerHTML"]
        else:
            return ""

    def __set__(self, instance, new_value):
        # print("new innerhtml for #" + instance.id)
        # print(new_value)
        instance.html_attr("innerHTML",new_value)


class Element:
    innerHTML = InnerHTML()
    def __init__(self, id, gui):
        self.window = gui.window
        self.parent = None
        self.display_mode = None
        elements = len(self.window.dom.get_elements("#" + id))
        if elements == 0:
            raise Exception("HTML Element with id #" + id + " does not exist.")
        elif elements > 1:
            raise Exception("HTML Element with id #" + id + " is declared multiple times.")
        self.id = id
        self.gui = gui
        self.event_functions = dict()

        self._function_on_show = lambda gui: None

    def __getattr__(self, name):
        elements = self.get_elements()

        if not hasattr(elements,"node"):
            return None

        if name in elements.node:
            return elements.node[name]
        else:
            return None

    def js(self, script):
        return self.window.evaluate_js(script)

    def on_show(self, func):
        self._function_on_show = func

    def get_width_in_em(self):
        js = f"document.getElementById({j(self.id)}).clientWidth/parseFloat(getComputedStyle(document.getElementById({j(self.id)}))['font-size'])"
        return self.js(js)

    def get_height_in_em(self):
        js = f"document.getElementById({j(self.id)}).clientHeight/parseFloat(getComputedStyle(document.getElementById({j(self.id)}))['font-size'])"
        return self.js(js)
    def hide(self):
        # previous_mode = self.js(f"document.getElementById({j(self.id)}).style.display")
        # if previous_mode != "none":
        #     self.display_mode = previous_mode

        js = f"document.getElementById({j(self.id)}).style.visibility = 'hidden'"
        self.js(js)
    def show(self):
        self._function_on_show(self.gui)
        js = f"document.getElementById({j(self.id)}).style.visibility = 'visible'"
        self.js(js)
        # display_mode = mode
        # if display_mode is None:
        #     if self.display_mode is not None:
        #         display_mode = self.display_mode
        #     else:
        #         display_mode = "block"
        #
        # print("show element", display_mode)
        # if display_mode is not None:
        #     js = f"document.getElementById({j(self.id)}).style.display = {j(display_mode)}"
        #     self.js(js)
    def size(self):
        js = f"[document.getElementById({j(self.id)}).width,document.getElementById({j(self.id)}).height]"
        return tuple(self.js(js))
    def width(self):
        js = f"document.getElementById({j(self.id)}).width"
        return self.js(js)
    def height(self):
        js = f"document.getElementById({j(self.id)}).height"
        return self.js(js)
    def offsetSize(self):
        js = f"[document.getElementById({j(self.id)}).naturalWidth,document.getElementById({j(self.id)}).naturalHeight]"
        return tuple(self.js(js))
    def offsetWidth(self):
        js = f"document.getElementById({j(self.id)}).naturalWidth"
        return self.js(js)
    def offsetHeight(self):
        js = f"document.getElementById({j(self.id)}).naturalHeight"
        return self.js(js)
    def get_elements(self):
        return self.window.dom.get_elements("#"+self.id)[0]

    def register_event(self, event, function, block_main_thread=True):
        if event not in self.event_functions:
            self.event_functions[event] = []
        self.event_functions[event].append(function)
        self.gui.register_event(self.id, self, event, block_main_thread)
    def trigger_event(self, event, event_information, block_main_thread):
        if event in self.event_functions:
            event_information["event_type"] = event
            for function in self.event_functions[event]:
                if function is None:
                    raise Exception("Event-function not available")

                sig = signature(function)
                no_params = len(sig.parameters)

                if block_main_thread:
                    if no_params >= 3:
                        function(self, self.gui, event_information)
                    elif no_params == 2:
                        function(self, self.gui)
                    elif no_params == 1:
                        function(self.gui)
                    elif no_params == 0:
                        function()
                else:
                    print("started non blocking thread")
                    if no_params >= 3:
                        Thread(target=function, args=(self, self.gui, event_information)).start()
                    elif no_params == 2:
                        Thread(target=function, args=(self, self.gui)).start()
                    elif no_params == 1:
                        Thread(target=function, args=(self.gui,)).start()
                    elif no_params == 0:
                        Thread(target=function, args=()).start()
                    print("ENDED non blocking thread")


    def create_child(self, gui_class, html_id, html_tag = None, innerHTML = None, alias=None):

        subid = html_id if alias is None else alias
        if subid in self.__dict__.keys():
            raise Exception("Unterobjekt mit Namen " + subid + " (HTML id #" + html_id + ") existiert bereits!")

        if html_tag is None or html_tag == "":
            self.__dict__[subid] = self.gui.add(gui_class, html_id)

        else:
            script = f"""
            element = document.createElement({j(html_tag)})
            element.id = {j(html_id)}
            """
            if innerHTML is not None and innerHTML != "":
                script += f"element.innerHTML = {j(innerHTML)};\n"
            script += f"document.getElementById({j(self.id)}).appendChild(element);"
            self.js(script)
            self.__dict__[subid] = self.gui.add(gui_class, html_id)

        return self.__dict__[subid]

    #register event functions without element and gui arguments
    def event(self, func):
        def arg_func(element, gui, event_information):
            func()

        return arg_func

    @dispatch(str, str)
    def load_css(self, css_attribute, css_value):
        css = f"""
                    #{self.id}
                    {{
                    {css_attribute} : {css_value};
                    }}
                    """
        self.window.load_css(css)

    @dispatch(str)
    def load_css(self, css_code):

        if "{" in css_code:
            css = css_code
        else:
            css = f"""
                        #{self.id}
                        {{
                        {css_code}
                        }}
                        """

        self.window.load_css(css)

    @dispatch(dict)
    def load_css(self, css_dict):
        css = f"""
                #{self.id}
                {{
                { "".join(attribute+": "+value+";" for attribute, value in css_dict.items()) }
                }}
                """
        self.window.load_css(css)

    @dispatch(str, str)
    def html_attr(self, attribute, value):
        js = f"document.getElementById({j(self.id)}).{attribute} = {j(value)}"
        self.js(js)

    @dispatch(str, bool)
    def html_attr(self, attribute, value):
        js = f"document.getElementById({j(self.id)}).{attribute} = {j(value)}"
        self.js(js)
    @dispatch(dict)
    def html_attr(self, attributes):
        for attribute, value in attributes.items():
            self.html_attr(attribute, value)

    def append_html(self, html):
        js = f"document.getElementById('{self.id}').insertAdjacentHTML('beforeend', {j(html)})"
        self.js(js)

    def prepend_html(self, html):
        js = f"document.getElementById('{self.id}').insertAdjacentHTML('afterbegin', {j(html)})"
        #print(js)
        self.js(js)

    # @property
    # def innerHTML(self):
    #     elements = self.get_elements()
    #     if "innerHTML" in elements.node:
    #         return self.get_elements().node["innerHTML"]
    #     else:
    #         return ""
    #
    # @innerHTML.setter
    # def innerHTML(self, new_value):
    #     self.html_attr("innerHTML",new_value)

