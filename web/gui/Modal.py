from gui.Element import Element
from gui.Button import Button

from json import dumps as j
class Modal(Element):
    def __init__(self, id, gui):
        super().__init__(id, gui)
        self.close()
        self.add_child(Element, self.id + "_content","div", alias="content")
        self.content.add_child(Element, self.id + "_header", "div", alias="header")
        self.content.add_child(Element, self.id + "_body", "div", alias="body")
        self.content.add_child(Element, self.id + "_footer", "div", alias="footer")
        self.header = self.content.header
        self.body = self.content.body
        self.footer = self.content.footer

        self.header.add_child(Button, self.id+"_btn_close", "span", "&times;", alias="btn_close")
        self.btn_close = self.header.btn_close
        self.header.add_child(Element, self.id+"_title", "h2", alias="title_element")
        self.btn_close.on_click(self.event(self.close))

    def set_default_css(self):

        css_background = {
            "position": "fixed",
            "z-index": "1",
            "left": "0",
            "top": "0",
            "width": "100%",
            "height": "100%",
            "overflow": "auto",
            "background-color": "rgba(0,0,0,0.4)"
        }
        self.load_css(css_background)
        css_content = {
            "background-color": "#fefefe",
            "margin": "15% auto",
            "width": "80%",
            "border": "1px solid #888",
            "padding": "20px",
        }
        self.content.load_css(css_content)
        css_padding = "padding: 2px 16px;"

        self.header.load_css(css_padding)
        self.body.load_css(css_padding)
        self.footer.load_css(css_padding)

        self.btn_close.load_css("float: right;")

    def show(self):
        self.html_attr("style.display","block")
    def close(self):
        self.html_attr("style.display","none")

    def __getattribute__(self, item):
        if item=="title":
            return self.header.title_element.get_elements()["text"]
        else:

            return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if key=="title":
            self.header.title_element.html_attr("innerHTML",value)
        else:
            super().__setattr__(key, value)
