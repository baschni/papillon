from init.logics.sql_queries import get_responses_and_corresponding_answers,set_configuration_id_for_conversation,get_configuration_id_for_conversation,get_configuration_object,update_prompt_history,insert_prompt, insert_response, get_prompt_and_siblings
from init.logics.handle_replicate import retrieve_response
from init.logics.configuration import Prompt
from init.logics.response import Response
from init.logics_gui_core.conversation import display_conversation, update_input_elements_from_history, update_input_elements_from_last_history
from html import escape
from gui.Element import Element
import asyncio
def show_prompt_history(gui):
    gui.prompt_history.show()
    # if gui.current_id_change is not None:
    #     gui.scroll_into_view("change" + gui.current_id_change)
def change_prompt(Element, gui):
    print("change prompt event")
    update_prompt_history(gui.tb_prompt.value, gui.conversation_index_for_prompt_change)
    update_input_elements_from_last_history(gui)

def clear_prompt(Element, gui):
    gui.tb_prompt.value = ""

    gui.tb_prompt.focus()
    update_prompt_history(gui.tb_prompt.value, gui.conversation_index_for_prompt_change)
    update_input_elements_from_last_history(gui)

def get_continuous_conversation_prompt(conv_id, last_prompt):
    history = get_responses_and_corresponding_answers(conv_id)
    total_prompt = ""
    for (prompt, answer) in history:
        total_prompt += f'''
              <|start_header_id|>user<|end_header_id|>
              {escape(prompt)}
              <|eot_id|>
        '''

        if answer != "" and answer is not None:
            total_prompt += f"""
              <|start_header_id|>assistant<|end_header_id|>
              {escape(answer)}
              <|eot_id|>"""

    total_prompt += f'''
          <|start_header_id|>user<|end_header_id|>
          {escape(last_prompt)}
          <|eot_id|>
    '''
    return total_prompt
def submit_prompt(gui):
    #You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.

    conv_id = gui.lb_conversations.get_selected_data("id_conv")
    conf_id = get_configuration_id_for_conversation(conv_id)
    prompt_text = gui.tb_prompt.value
    #print("start submit prompt")
    gui.conversation_index_for_prompt_change = conv_id
    gui.tb_prompt.value = ""
    update_prompt_history(gui.tb_prompt.value, gui.conversation_index_for_prompt_change)
    update_input_elements_from_last_history(gui)
    gui.tb_prompt.focus()
    #print(prompt_text)
    # get configuration object

    if conf_id is None:
        gui.alert("Bitte legen Sie eine Konfiguration für die aktuelle Konversation fest!")
        return

    config = get_configuration_object(conf_id)

    if config.parameters["conversation_or_isolated"].value == 1:
        total_prompt = get_continuous_conversation_prompt(conv_id, prompt_text)
        id_prompt = insert_prompt(prompt_text, conv_id, conf_id, total_prompt=total_prompt)
    else:
        id_prompt = insert_prompt(prompt_text, conv_id, conf_id)
        total_prompt = prompt_text

    # insert prompt

    #gui.tb_prompt.value = ""
    #print("html", prompt_text)
    # show answer and add element for response
    newline_char = "\n"
    html = f"<div class='question'>{escape(prompt_text).replace(newline_char,'<br />')}</div><div class='answer' id='anwser_{id_prompt}'></div>"
    gui.conversation.prepend_html(html)
    answer_container = gui.add(Element,"anwser_" + str(id_prompt))

    def append_prediction_part(word):
        answer_container.append_html(escape(word).replace("\n","<br />"))

    # execute configuration object and bind function to update with every word
    #gui.active_requests.append(config)
    #https://pythonalgos.com/runtimeerror-event-loop-is-closed-asyncio-fix/
    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    response = config.execute_prompt(gui, total_prompt, {parameter.name: parameter.get_value() for parameter in config.parameters.values()}, append_prediction_part)
    #gui.active_requests.remove(config)
    # on finish write total result + meta data to database


    #id_conv = gui.lb_conversations.get_selected_data("id_conv")

    insert_response(response, conv_id, id_prompt)

    #display_conversation(None, gui, None, do_not_update_input=True)




        #response_text = retrieve_response(prompt, append)

        #response = Response("".join(response_text))



        #display_conversation(None, gui, None)

def toggle_prompt_height(Element, gui, info):
    if Element.innerHTML == "+":
        Element.innerHTML = "-"
        gui.conversation.load_css({"height": "41%"})
        gui.input.load_css({"height": "50%"})
    else:
        Element.innerHTML = "+"
        gui.conversation.load_css({"height": "75%"})
        gui.input.load_css({"height": "16%"})

# def display_prompt_settings(Element, gui, info):
#     gui.prompt_settings.show()
#
#
# def display_prompt_history(Element, gui, info):
#     gui.prompt_history.show()


def redo_change(gui):
    prompt_from_history = get_prompt_and_siblings(gui.higher_id_change)
    update_input_elements_from_history(gui, prompt_from_history)


def undo_change(gui):
    prompt_from_history = get_prompt_and_siblings(gui.lower_id_change)
    update_input_elements_from_history(gui, prompt_from_history)