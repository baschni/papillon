from init.logics.sql_queries import load_conversations, update_prompt_history
from init.logics_gui_core.listbox import KEYS_TO_DISPLAY,add_conversation, remove_conversation
from init.logics_gui_core.conversation import display_conversation
from init.logics_gui_core.input import \
    clear_prompt, show_prompt_history, change_prompt, submit_prompt, toggle_prompt_height, \
    undo_change, redo_change
from threading import Thread
def display_conversations(gui):

    # load conversation data from sqlite
    conversations = load_conversations()
    gui.active_requests = []
    gui.lb_conversations.register_event("change", display_conversation)

    gui.lb_conversations.load_dictionary(conversations, KEYS_TO_DISPLAY)
    # restructure into listbox data
    # load first listbox entry


    gui.btn_add_conversation.on_click(add_conversation)
    gui.btn_remove_conversation.on_click(remove_conversation)

    gui.btn_toggle_prompt_height.on_click(toggle_prompt_height)

    gui.btn_prompt_settings.on_click(lambda gui: gui.prompt_settings.show(gui.lb_conversations.get_selected_data("id_conv")))
    #gui.btn_prompt_history.on_click(lambda gui: gui.prompt_history.show())
    gui.btn_prompt_history.on_click(show_prompt_history)
    #gui.btn_send_prompt.on_click(submit_prompt_as_thread)
    gui.btn_send_prompt.on_click(lambda gui: Thread(target=submit_prompt,args=(gui,)).start())

    #gui.tb_prompt.register_event("input", lambda gui: gui.add_global("conversation_index_for_prompt_change",gui.lb_conversations.get_selected_data(key="id_conv")))
    gui.tb_prompt.register_event("focus", lambda gui: gui.add_global("conversation_index_for_prompt_change",gui.lb_conversations.get_selected_data(key="id_conv")))
    gui.tb_prompt.register_event("change", change_prompt)

    gui.btn_clear_prompt.on_click(clear_prompt)
    gui.btn_redo_change.on_click(redo_change)
    gui.btn_undo_change.on_click(undo_change)

# def submit_prompt_as_thread(gui):
#     print("start thread")
#     t1 = Thread(target=submit_prompt, args=(gui,))
#     t1.daemon = True
#     t1.start()
#     print("finished starting thread")
