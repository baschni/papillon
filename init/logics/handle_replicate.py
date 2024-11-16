import replicate
from config import REPLICATE_API_KEY
import os
from json import loads
from copy import deepcopy
from config import REPLICATE_API_KEY
import asyncio
from webview import JavascriptException
def retrieve_response(prompt, append_func):
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY
    output = ""

    # for event in replicate.stream(
    #         prompt.model,
    #         input={
    #             "top_k": prompt.top_k,
    #             "top_p": prompt.top_p,
    #             "prompt": prompt.prompt,
    #             "max_tokens": prompt.max_tokens,
    #             "min_tokens": prompt.min_tokens,
    #             "temperature": prompt.temperature,
    #             "prompt_template": prompt.prompt_template,
    #             "presence_penalty": prompt.presence_penalty,
    #             "frequency_penalty": prompt.frequency_penalty
    #         },
    # ):
    #     append_func(str(event))
    #     output += str(event)
    #     print(str(event))

    result = replicate.run(
            prompt.model,
            input={
                "top_k": prompt.top_k,
                "top_p": prompt.top_p,
                "prompt": prompt.prompt,
                "max_tokens": prompt.max_tokens,
                "min_tokens": prompt.min_tokens,
                "temperature": prompt.temperature,
                "prompt_template": prompt.prompt_template,
                "presence_penalty": prompt.presence_penalty,
                "length_penalty": prompt.length_penalty,
                "system_prompt": prompt.system_prompt,
                "stop_sequences": prompt.stop_sequences
            })

    return result

def predict(model, prompt, parameters, update, set_prediction):

    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY
    input = {}
    prompt = deepcopy(prompt)


    for key, value in parameters.items():
        if value is not None:
            input[key] = value

    if "pre_prompt" in input:
        prompt = input["pre_prompt"] + "\n\n" + prompt
        del input["pre_prompt"]

    from pprint import pprint

    input["prompt"] = prompt


    #<pprint(input)
    #print(input, model, prompt, parameters)
    prediction = replicate.models.predictions.create(
        model,
        input=input
    )

    set_prediction(prediction)


    resp = {
        "status": prediction.status
    }
    previous_output = ""

    while resp["status"] != "succeeded" and resp["status"] != "failed":
        # resp = prediction._client._async_request(
        #     "GET",
        #     prediction.urls["get"]
        # )
        resp = prediction._client._request("GET",prediction.urls["get"])
        # _json_to_prediction(resp._client, resp.json())
        # print(resp.decod.json())

        resp = loads(resp.content.decode("utf-8"))
        #pprint(resp)
        if "output" in resp and resp["output"] is not None:
            output = "".join(resp["output"])

            try:
                update(output[len(previous_output):])
            except JavascriptException:
                pass

            previous_output = output


    return resp
