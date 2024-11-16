from init.logics.parameter import Integer, Float, Text, Boolean
from html import escape
from json import dumps as j
from gui.Listbox import Listbox
from gui.Textarea import Textarea
from gui.Textbox import Textbox
from gui.Button import Button
from gui.Richtext import Richtext
from gui.Iframe import Iframe
from gui.Modal import Modal
from gui.Element import Element
from gui.Popup import Popup
from gui.Input import Input
from init.logics.handle_replicate import predict
import asyncio

class Prompt():
    def __init__(self, prompt):

        self.parameters = []

    def stop_prompt(self):
        pass

class Replicate(Prompt):


    def __init__(self):
        self.prediction = None

    async def execute_prompt_async(self, gui, prompt, parameters,  update_func):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.gui = gui
        result = await predict(self.model, prompt, parameters, update_func, self.set_prediction)


        return result

    def execute_prompt(self, gui, prompt, parameters,  update_func):
        #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.gui = gui
        result = predict(self.model, prompt, parameters, update_func, self.set_prediction)


        return result

    def set_prediction(self, prediction):
        self.prediction = prediction
        #self.gui.active_requests.append(prediction)

    def stop_prompt(self):
        if self.prediction is not None:
            try:
                self.prediction.cancel()
            except Exception:
                pass
    def layout_parameters(self, prefix):
        html = "<table>"

        for parameter in self.parameters.values():
            id = prefix + "_" + parameter.name
            parameter.id = id
            parameter.id_conf = self.id_conf
            value = parameter.get_value()

            html += "<tr><td>" + escape(parameter.name) + "</td><td>"

            if isinstance(parameter, Text):
                html += f"<textarea id='{id}'>{escape(value)}</textarea>"
                parameter.gui_class = Textbox

            elif isinstance(parameter, Integer):
                if None in parameter.range:
                    html += f"<input type='text' value='{j(value)}' id='{id}' />"
                    parameter.gui_class = Textbox
                else:
                    html += f"<input type='range' min='{parameter.range[0]}' max='{parameter.range[1]}' value='{j(value)}' step='1' id='{id}' oninput='this.nextElementSibling.value = this.value' /><output>{escape(str(value))}</output>"
                    parameter.gui_class = Input

            elif isinstance(parameter, Float):
                if None in parameter.range:
                    html += f"<input type='text' value='{j(value)}' id='{id}' />"
                    parameter.gui_class = Textbox
                else:
                    html += f"<input type='range' min='{parameter.range[0]}' max='{parameter.range[1]}' value='{j(value)}' step='0.01' id='{id}' oninput='this.nextElementSibling.value = this.value' /><output>{escape(str(value))}</output>"
                    parameter.gui_class = Input

            elif isinstance(parameter, Boolean):
                    html += f"<input type='checkbox' {'checked=''checked''' if value == 1 else ''} id='{id}' />"
                    parameter.gui_class = Input

            html += f"</td><td>{escape(parameter.description) if parameter.description is not None else ''}</td></tr>"

        return html

    def connect_parameter_events(self, gui):
        for parameter in self.parameters.values():
            parameter.element = parameter.gui_class(parameter.id, gui)
            #parameter.element.value = parameter.value
            parameter.connect_events()
    # def add_gui_parameter(self, gui_class, html_id):
    #     #short inner
    #     if len(html_id) > len(self.id) and html_id[:len(self.id)+1] == self.id + "_":
    #         sub_id = html_id[len(self.id)+1:]
    #     else:
    #         sub_id = html_id
    def set_value(self, name, value):

            self.parameters[name].value = value
    def get_values(self):
        values = {}
        for name, parameter_object in self.parameters:
            self.values[name] = parameter_object.value

        return values

class llama3_70b_instruct(Replicate):


    def __init__(self, id_conf=None):
        super().__init__()

        #self.prompt = prompt
        self.model = "meta/meta-llama-3-70b-instruct"
        self.id_conf = id_conf

        parameters = [


            Text("system_prompt","You are a helpful assistant","System prompt to send to the model. This is prepended to the prompt and helps guide system behavior."),
            Text("pre_prompt","","Concrete prompt to send before the actual user prompt. Similar to system prompt"),
            Text("prompt_template","""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>""", "Template for formatting the prompt. Can be an arbitrary string, but must contain the substring `{prompt}`."),
            Text("stop_sequences","<|end_of_text|>,<|eot_id|>","A comma-separated list of sequences to stop generation at. For example, '<end>,<stop>' will stop generation at the first instance of 'end' or '<stop>'."),
            Integer("min_tokens",0,(-1,None),"Minimum number of tokens to generate. To disable, set to -1. A word is generally 2-3 tokens."),
            Integer("max_tokens",512,(1,None),"Maximum number of tokens to generate. A word is generally 2-3 tokens."),
            Float("temperature",0.7,(0,5),"Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic, 0.75 is a good starting value."),
            Float("top_p",0.95,(0,1),"When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens."),
            Integer("top_k",0,(-1,None),"When decoding text, samples from the top k most likely tokens; lower to ignore less likely tokens."),
            Float("length_penalty",1,(0,5),"A parameter that controls how long the outputs are. If < 1, the model will tend to generate shorter outputs, and > 1 will tend to generate longer outputs."),
            Float("presence_penalty",1,(None,None),"A parameter that penalizes repeated tokens regardless of the number of appearances. As the value increases, the model will be less likely to repeat tokens in the output."),
            Integer("seed", None,(None,None),"Random seed. Leave blank to randomize the seed.",  can_be_none=True),
            Boolean("conversation_or_isolated",False,"Specifies if each request is executed isolatedly or as a follow up in the current conversation")
        ]

        #self.parameters = parameters

        self.parameters = dict()

        for parameter in parameters:
            self.parameters[parameter.name] = parameter
            self.__dict__[parameter.name] = parameter


class llama31_405b_instruct(Replicate):


    def __init__(self, id_conf=None):
        super().__init__()

        #self.prompt = prompt
        self.model = "meta/meta-llama-3.1-405b-instruct"
        self.id_conf = id_conf

        parameters = [


            Text("system_prompt","You are a helpful assistant","System prompt to send to the model. This is prepended to the prompt and helps guide system behavior."),
            Text("pre_prompt","","Concrete prompt to send before the actual user prompt. Similar to system prompt"),
            Text("prompt_template","""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>""", "Template for formatting the prompt. Can be an arbitrary string, but must contain the substring `{prompt}`."),
            Text("stop_sequences","<|end_of_text|>,<|eot_id|>","A comma-separated list of sequences to stop generation at. For example, '<end>,<stop>' will stop generation at the first instance of 'end' or '<stop>'."),
            Integer("min_tokens",0,(-1,None),"Minimum number of tokens to generate. To disable, set to -1. A word is generally 2-3 tokens."),
            Integer("max_tokens",1024,(1,None),"Maximum number of tokens to generate. A word is generally 2-3 tokens."),
            Float("temperature",0.6,(0,5),"Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic, 0.75 is a good starting value."),
            Float("top_p",0.9,(0,1),"When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens."),
            Integer("top_k",50,(-1,None),"When decoding text, samples from the top k most likely tokens; lower to ignore less likely tokens."),
            Float("presence_penalty",1,(None,None),"A parameter that penalizes repeated tokens regardless of the number of appearances. As the value increases, the model will be less likely to repeat tokens in the output."),
            Float("frequency_penalty",0,(None,None),""),
          
            Boolean("conversation_or_isolated",False,"Specifies if each request is executed isolatedly or as a follow up in the current conversation")
        ]

        #self.parameters = parameters

        self.parameters = dict()

        for parameter in parameters:
            self.parameters[parameter.name] = parameter
            self.__dict__[parameter.name] = parameter



