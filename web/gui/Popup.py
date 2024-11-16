from gui.Element import Element
from gui.Button import Button
from json import dumps as j

SUFFIX_TITLE_BAR = "_title_bar"
SUFFIX_TITLE = "_title_label"
SUFFIX_CLOSE_BUTTON = "_btn_close"
SUFFIX_CLOSE_BUTTON_IN_TITLE_BAR = "_btn_close_in_title_bar"
class Popup(Element):


    def __init__(self, id, gui, title=None, draggable=False):
        #todo add body element when having titlebar
        super().__init__(id, gui)
        self.ids_not_to_erase = [self.id + SUFFIX_TITLE_BAR, self.id + SUFFIX_CLOSE_BUTTON, self.id + SUFFIX_CLOSE_BUTTON_IN_TITLE_BAR]

        self.hide()


        self.has_title_bar=False
        self.is_draggable = False

        self.title = title


        self.create_close_button()

        if title is not None:
            self.set_title_and_dragging(title, draggable)

        #self.btn_close.on_click(gui.getElementById(self.id).hide)
        self.initiate_css()

    def set_title_and_dragging(self, title, draggable=False):
        self.has_title_bar = True

        self.title = title
        self.create_title_bar(title)

        if draggable:
            self.is_draggable = True
            self.enable_dragging()

    def clear_contents(self):
        js = f"""
            for (elem of document.getElementById('{self.id}').children)
            {{
                if(! {self.ids_not_to_erase}.includes(elem.id))
                {{
                    elem.remove();
                }}
            }}
            """
        self.js(js)

    def initiate_css(self):

        css_popup = f"""
        #{self.id} {{
            border: 1px solid black;
            overflow: hidden;
            background-color: white;
        }}"""

        css_close_button = f"""
        #{self.id+SUFFIX_CLOSE_BUTTON} {{
          color: #aaa;
          float: right;
          font-size: 3em;
          font-weight: bold;
        }}
        
        #{self.id+SUFFIX_CLOSE_BUTTON}:hover,
        #{self.id+SUFFIX_CLOSE_BUTTON}:focus {{
          color: black;
          text-decoration: none;
          cursor: pointer;
        }}
        
        #{self.id+SUFFIX_CLOSE_BUTTON_IN_TITLE_BAR} {{
          color: #aaa;
          float: right;
          font-size: 3em;
          font-weight: bold;
        }}
        
        #{self.id+SUFFIX_CLOSE_BUTTON_IN_TITLE_BAR}:hover,
        #{self.id+SUFFIX_CLOSE_BUTTON_IN_TITLE_BAR}:focus {{
          color: black;
          text-decoration: none;
          cursor: pointer;
        }}
        """

        css_title_bar = f"""
        #{self.id + SUFFIX_TITLE_BAR} {{
          background-color: #e7e9eb;
          position: absolute,
          left: 0;
          right: 0;
          width: 100%;
          height: 3em;
          font-weight: bold;
        }}
        """
        #e7e9eb

        self.load_css(css_popup)
        self.load_css(css_close_button)
        self.load_css(css_title_bar)

    def create_close_button(self):
        #self.innerHTML = f"<span id='{self.id+SUFFIX_CLOSE_BUTTON}'>&times;</span>" + self.innerHTML
        self.prepend_html(f"<span id='{self.id+SUFFIX_CLOSE_BUTTON}'>&times;</span>")
        self.add(Button, self.id+SUFFIX_CLOSE_BUTTON)
        self.__dict__[SUFFIX_CLOSE_BUTTON[1:]].on_click(lambda gui: gui.getElementById(self.id).hide())


    def create_title_bar(self, title):
        js = f"document.getElementById('{self.id+SUFFIX_CLOSE_BUTTON}').remove()"
        self.js(js)

        self.prepend_html(f"<div id='{self.id+SUFFIX_TITLE_BAR}'><label id='{self.id+SUFFIX_TITLE}'>{title}</label>"\
                         + f"<span id='{self.id+SUFFIX_CLOSE_BUTTON_IN_TITLE_BAR}'>&times;</span>"\
                         + "</div")

        self.add(Button, self.id + SUFFIX_CLOSE_BUTTON_IN_TITLE_BAR)
        # def event_close(gui):
        #     self.hide()

        self.btn_close_in_title_bar.on_click(self.hide)
        #self.btn_close_in_title_bar.register_event()




    def enable_dragging(self):
        js = f"""
            dragElement(document.getElementById('{self.id}'));

            function dragElement(elmnt) {{
              var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
              if (document.getElementById('{self.id + SUFFIX_TITLE_BAR}')) {{
                // if present, the header is where you move the DIV from:
                document.getElementById('{self.id + SUFFIX_TITLE_BAR}').onmousedown = dragMouseDown;
              }}
               else {{
                // otherwise, move the DIV from anywhere inside the DIV:
                elmnt.onmousedown = dragMouseDown;
              }}
            
              function dragMouseDown(e) {{
                e = e || window.event;
                e.preventDefault();
                // get the mouse cursor position at startup:
                pos3 = e.clientX;
                pos4 = e.clientY;
                document.onmouseup = closeDragElement;
                // call a function whenever the cursor moves:
                document.onmousemove = elementDrag;
              }}
            
              function elementDrag(e) {{
                e = e || window.event;
                e.preventDefault();
                // calculate the new cursor position:
                pos1 = pos3 - e.clientX;
                pos2 = pos4 - e.clientY;
                pos3 = e.clientX;
                pos4 = e.clientY;
                // set the element's new position:
                elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
                elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
              }}
            
              function closeDragElement() {{
                // stop moving when mouse button is released:
                document.onmouseup = null;
                document.onmousemove = null;
              }}
            }}
        """
        self.js(js)
    def show(self):
        #always on top
        js = f"var elem = document.getElementById('{self.id}'); elem = elem.parentNode.appendChild(elem)"
        self.js(js)
        super().show()
    def add(self, gui_class, html_id):
        #short inner
        if len(html_id) > len(self.id) and html_id[:len(self.id)+1] == self.id + "_":
            sub_id = html_id[len(self.id)+1:]
        else:
            sub_id = html_id


        # add variable to class object namespace by constructing a new object of type gui_class
        if sub_id in self.__dict__.keys():
            raise Exception("HTML-Element mit ID " + sub_id + " (#" + html_id + ") bereits hinzugefügt!")

        element = self.__dict__[sub_id] = gui_class(html_id, self.gui)
        element.parent = self
        return element