# header_middle = {
#
#     " width": "-moz-fit-content",
#     "  width": "-webkit-fit-content",
#     "width": "fit-content",
#     "margin": "auto",
#     # "background-color": "magenta",
#     # "position":"absolute",
#     # "left":"50%",
#     # "transform":"translateX(-50%)",
# }
# gui.load_css("#middle", header_middle)

def init_design(gui):
    print("=== init design ===")
    design_wrappers(gui)


def design_wrappers(gui):

    def core():
        def coarse_layout():
            gui.load_css("html, body", "height: 99%")

            left = {
                "display": "block",
                "width": "25%",
                "height": "100%",
                "float": "left",
                #"white-space": "nowrap"
            }
            gui.left.load_css(left)

            right = {
                "display": "block",
                "width": "74%",
                "height": "100%",
                "float": "left",
                #"white-space": "nowrap"
                #"background-color": "black",
            }
            gui.right.load_css(right)

            header = {
                "display": "block",
                "width": "100%",
                "height": "5%",
                "margin-bottom": "1%",
                "float": "left",

               # "background-color": "yellow",
            }
            gui.header.load_css(header)

            conversation = {
                "display": "block",
                "width": "90%",
                "height": "75%",
                "margin-bottom": "1%",
                "float": "left",
                "overflow-y": "scroll",
                "padding-left": "2%",
                "padding-right": "2%",

                #"background-color": "green",
            }
            gui.conversation.load_css(conversation)



            input = {
                "display": "block",
                "width": "100%",
                "height": "16%",
                "float": "left",
                "border-top" : "1px solid black",
                "padding-top": "2%",

                #"background-color": "blue",
            }
            gui.input.load_css(input)

        def listbox():
            lb_conversations = {
                "display": "block",
                "width": "80%",
                "height": "80%",
                "float": "left",

                #"background-color": "blue",
            }
            gui.lb_conversations.load_css(lb_conversations)
            gui.lb_conversations.html_attr("size", "40")

        def prompt():
            gui.tb_prompt.load_css(
                {
                    "width": "80%",
                    "height": "90%",
                }
            )

            gui.tb_prompt.html_attr("spellcheck",False)

            #gui.btn_prompt_settings.load_css({"display": "none"})
            #gui.btn_prompt_settings.load_css({"display": "none"})

        def conversations():
            class_question = {
                "width": "75%",
                "border": "1px solid black",
                "float": "left",
                "margin-bottom": "15px",
                "padding": "5px",
                "user-select": "text",
            }
            class_answer = {
                "width": "75%",
                "border": "1px solid black",
                "float": "right",
                "margin-bottom": "15px",
                "padding": "5px",
                "user-select": "text",
            }
            gui.load_css("#conversation .question", class_question)
            gui.load_css("#conversation .answer", class_answer)

        coarse_layout()
        listbox()
        prompt()
        conversations()

    def prompt_settings():
        settings_popup = {
            "width": "60%",
            "height": "60%",
            "position": "absolute",
            "left": "50%",
            "top": "50%",
            "transform": "translate(-50%, -50%)",
        }
        gui.load_css("#prompt_settings", settings_popup)

        #gui.prompt_settings.set_title_and_dragging("Prompt-Einstellungen", True)

    def prompt_history():
        history_popup = {
            "width": "60%",
            "height": "80%",
            "position": "absolute",
            "left": "50%",
            "top": "50%",
            "transform": "translate(-50%, -50%)",
            #"overflow-y": "scroll"
        }
        gui.load_css("#prompt_history", history_popup)

        gui.prompt_history.set_title_and_dragging("Eingabe-Verlauf", True)

    def init_design():
        core()
        prompt_settings()
        prompt_history()


    init_design()




