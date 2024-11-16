from init.logics.sql_queries import load_conversation_data, get_last_prompt_and_siblings, get_prompt_history, get_prompt_and_siblings
from init.logics.layout import layout_conversation, layout_prompt_history


def show_prompt_history(gui):
    id_conv = gui.lb_conversations.get_selected_data("id_conv")
    gui.prompt_history.clear_contents()
    prompt_history = get_prompt_history(id_conv)
    #gui.prompt_history.innerHTML = gui.prompt_history.innerHTML + layout_prompt_history(prompt_history)


def update_input_elements_from_history(gui, prompt_from_history):
    if prompt_from_history is not None:
        (id_hist, prompt, date, id_change, lower_id_change, higher_id_change) = prompt_from_history

        gui.higher_id_change = higher_id_change
        gui.current_id_change = id_change
        gui.lower_id_change = lower_id_change

        gui.tb_prompt.value = prompt

        if higher_id_change is None:
            gui.btn_redo_change.hide()
        else:
            gui.btn_redo_change.show()

        if lower_id_change is None:
            gui.btn_undo_change.hide()
        else:
            gui.btn_undo_change.show()

def update_input_elements_from_last_history(gui):
    #print("updated input elements")
    id_conv = gui.lb_conversations.get_selected_data("id_conv")
    last_prompt_from_history = get_last_prompt_and_siblings(id_conv)
    update_input_elements_from_history(gui, last_prompt_from_history)
def display_conversation(Element, gui, info, do_not_update_input=False):
    for config in gui.active_requests:
        config.stop_prompt()

    gui.active_prompts = []

    id_conv = gui.lb_conversations.get_selected_data("id_conv")

    conversation_data = load_conversation_data(id_conv)

    if not do_not_update_input:
        update_input_elements_from_last_history(gui)

    html = layout_conversation(conversation_data)

    gui.conversation.innerHTML = html



    gui.prompt_history.on_show(show_prompt_history)