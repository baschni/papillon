from init.logics.sql_queries import insert_conversation, delete_conversation, load_conversations, load_conversation_data
from init.logics.layout import layout_conversation
KEYS_TO_DISPLAY = ["date_display", "title"]

def add_conversation(Element, gui, info):
    title = gui.prompt("Bitte geben Sie einen Betreff für die Unterhaltung ein.")
    if title is None:
        return
    id_conv = insert_conversation(title)
    print(id_conv)

    gui.lb_conversations.load_dictionary(load_conversations(), keys_to_display=KEYS_TO_DISPLAY)
    gui.lb_conversations.set_selected({"id_conv": id_conv})

def remove_conversation(Element, gui, info):
    id_conv = gui.lb_conversations.get_selected_data("id_conv")
    if id_conv is not None:
        delete_conversation(id_conv)

    gui.lb_conversations.load_dictionary(load_conversations(), keys_to_display=KEYS_TO_DISPLAY)

    #todo: select conversation before or after deleted



