from html import escape
def layout_conversation(conversation_data):
    html = ""
    for line in conversation_data:
        (id_prompt, creation_date, prompt, id_resp, output, total_time, total_tokens, completed_at) = line
        html+= "<div class='question'>" + escape(prompt).replace("\n","<br />") + "</div>"
        if output is not None:
            html += "<div class='answer'>" + escape(output).replace("\n","<br />") + "</div>"
    return html

def layout_prompt_history(prompt_history):
    html=""
    previous_hist = -1
    for line in prompt_history:
        (id_hist, id_change, prompt, date) = line

        if previous_hist != id_hist and previous_hist != -1:
            html+="<hr />"

        if prompt is not None and prompt.strip() != "":
            html+=f"<div class='hist_entry' id='change{id_change}'>" + escape(prompt) + "</div>"

        previous_hist = id_hist

    return html

