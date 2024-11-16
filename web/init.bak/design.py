

def init_design(gui):
    gui.lb_level1.load_css({"width": "50%"})
    gui.lb_level1.html_attr("size","4")
    gui.lb_level1.html_attr({"size":"10"})

    gui.rt_text.html_attr("contentEditable","true")
    gui.if_pdf.load_css("background-color", "red")

    gui.md_popup.set_default_css()