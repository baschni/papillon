#https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite

from init.logics.sqlite_helper import commit_query, get_date_str, from_date_str, get_max_date
from datetime import datetime
from init.logics.configuration import llama3_70b_instruct, llama31_405b_instruct
import dateutil
def convert_conversations_for_listbox(results):
    data = {
        "id_conv": [],
        "date": [],
        "date_display": [],
        "title": [],

    }
    for row in results:
        data["id_conv"].append(row[0])
        data["date"].append(from_date_str(row[1]))
        data["date_display"].append(from_date_str(row[1]).strftime("%y-%m-%d"))
        data["title"].append(row[2])

    return data
def load_conversations():


   query = """
   SELECT id_conv, creation_date, title FROM conversations
   WHERE visible = 1
   ORDER BY creation_date DESC
   """

   results = commit_query(query)

   return convert_conversations_for_listbox(results)

    # # [[id_conv], [creation_date], [title]]
    # conversations = get_conversations(db)
    # #id_conv -> [[type, date, text1, text2, text3]]
    # # type= prompt or response
    # conversations_content = get_conversations_content(db)
    #
    # return conversations, conversations_content

def load_conversation_data(id_conv):
    responses_query = """
    SELECT r.id_resp, r.id_parent_prompt, r.output, r.total_time, r.total_tokens, d.completed_at
    FROM responses r
    LEFT JOIN response_details d
    ON r.id_resp = d.id_resp
    WHERE r.id_parent_conv = :id_conv
    """

    query = """
    SELECT p.id_prompt, p.creation_date, p.prompt,
    r.id_resp, r.output, r.total_time, r.total_tokens, r.completed_at
    FROM prompts p
    LEFT JOIN
    (
    """ + responses_query + """
    ) r
    ON p.id_prompt = r.id_parent_prompt
    
    WHERE p.id_parent_conv = :id_conv
    ORDER BY p.creation_date DESC
    """

    results = commit_query(query, {"id_conv": id_conv})

    return results

def update_prompt_history(prompt, id_conv):
    print("updated prompt history")
    prompt_value = prompt.strip()
    query = """
        SELECT max(id_hist)
        FROM prompt_history
        WHERE id_parent_conv = :id_conv
        """
    previous_history = commit_query(query, {"id_conv": id_conv})

    # if prompt == "" or len(previous_history) == 0:
    #     # insert new history entry
    #     query = """
    #     INSERT INTO prompt_history
    #     (id_parent_conv, creation_date, update_date, prompt)
    #     VALUES
    #     (
    #     :id_conv,
    #     :date,
    #     :date,
    #     :prompt
    #     )
    #     """
    # else:
    #     # update existing history
    #     query = """
    #     UPDATE prompt_history
    #     SET
    #     prompt = :prompt,
    #     update_date = :date
    #     WHERE id_parent_conv = :id_conv
    #     AND update_date =
    #     ( SELECT max(update_date)
    #     FROM prompt_history
    #     WHERE id_parent_conv = :id_conv )
    #     """

    if prompt_value == "" or len(previous_history) == 0 or previous_history[0][0] is None:
        # insert new history entry

        query = """
        INSERT INTO prompt_history
        (id_parent_conv)
        VALUES
        (
        :id_conv
        )
        """

        id_hist = commit_query(query, {"id_conv": id_conv})




    else:
        # update existing history


        id_hist = previous_history[0][0]

    query = """
    INSERT INTO prompt_history_changes
    (id_parent_hist, date, prompt)
    VALUES
    (
    :id_hist,
    :date,
    :prompt
    )
    """

    params = {"id_hist": id_hist, "date": get_date_str(), "prompt": prompt_value}
    commit_query(query, params)

def get_prompt_history(id_conv):
    query = """
    SELECT id_hist, id_change, prompt, date
    FROM prompt_history
    LEFT JOIN prompt_history_changes
    on id_hist = id_parent_hist
    WHERE
    id_parent_conv = :id_conv
    ORDER BY date DESC
    """

    return commit_query(query,{"id_conv": id_conv})

def get_prompt_and_siblings(id_change):
    query = """
    SELECT id_parent_hist,
    prompt,
    date,
    id_change,
    (SELECT max(c2.id_change) FROM prompt_history_changes c2 WHERE id_parent_hist = c1.id_parent_hist AND c2.id_change < c1.id_change) as lower_id_change,
    (SELECT min(c2.id_change) FROM prompt_history_changes c2 WHERE id_parent_hist = c1.id_parent_hist AND c2.id_change > c1.id_change) as higher_id_change
    FROM prompt_history_changes c1
    WHERE id_change = :id_change
    """

    result = commit_query(query,{"id_change": id_change})

    return result[0] if len(result) == 1 else None

def get_last_prompt_and_siblings(id_conv):
    query = """
    SELECT id_parent_hist,
    prompt,
    date,
    max(id_change),
    (SELECT max(c2.id_change) FROM prompt_history_changes c2 WHERE id_parent_hist = c1.id_parent_hist AND c2.id_change < c1.id_change) as lower_id_change,
    (SELECT min(c2.id_change) FROM prompt_history_changes c2 WHERE id_parent_hist = c1.id_parent_hist AND c2.id_change > c1.id_change) as higher_id_change
    FROM prompt_history
    LEFT JOIN prompt_history_changes c1
    on id_hist = id_parent_hist
    WHERE
    id_parent_conv = :id_conv
    """

    result = commit_query(query,{"id_conv": id_conv})

    return result[0] if len(result) == 1 else None

def get_last_prompt(id_conv):
    query = """
    SELECT id_hist, id_change, prompt, date
    FROM prompt_history
    LEFT JOIN prompt_history_changes
    on id_hist = id_parent_hist and
    date = (
        SELECT max(date)
        FROM prompt_history_changes
        WHERE id_parent_hist = id_hist --(SELECT id_hist FROM prompt_history WHERE id_parent_conv = :id_conv)
    )
    WHERE
    id_parent_conv = :id_conv
    """

    result = commit_query(query,{"id_conv": id_conv})

    return result[0] if len(result) == 1 else None
def insert_prompt(prompt, id_conv, id_conf, total_prompt = None):
    query_prompt = """
    INSERT INTO prompts
    (id_parent_conv, id_conf, creation_date, prompt, total_prompt)
    VALUES (
    :id_conv, :id_conf, :date, :prompt, :total_prompt
    )
    """
    id_prompt = commit_query(query_prompt, {"id_conv": id_conv, "id_conf": id_conf, "date": get_date_str(), "prompt": prompt, "total_prompt": total_prompt})

    # query_parameters = """
    # INSERT INTO prompt_parameters
    # (model, top_k, top_p, max_tokens, min_tokens, temperature, presence_penalty, frequency_penalty)
    # VALUES
    # (:model, :top_k, :top_p, :max_tokens, :min_tokens, :temperature, :presence_penalty, :frequency_penalty)
    # """
    # parameters = {
    #     "model": prompt.model,
    #     "top_k": prompt.top_k,
    #     "top_p": prompt.top_p,
    #     "max_tokens": prompt.max_tokens,
    #     "min_tokens": prompt.min_tokens,
    #     "temperature": prompt.temperature,
    #     "presence_penalty": prompt.presence_penalty,
    #     "frequency_penalty": prompt.frequency_penalty
    #
    # }
    # commit_query(query_parameters, parameters)
    return id_prompt

def from_replicate_date_str(date_str):
    # date_str = date_str[:-1]
    # splitted = date_str.split(".")
    # microsecs = splitted[1]
    # if len(microsecs) > 6:
    #     microsecs = microsecs[:6]
    # elif len(microsecs) < 6:
    #     microsecs.ljust(6,"0")

    #datestr = splitted[0] + "." + microsecs + "Z"
    #datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    return dateutil.parser.parse(date_str)
def insert_response(response, id_conv, id_prompt):
    from pprint import pprint
    #pprint(response)

    completed_at = from_replicate_date_str(response["completed_at"])
    metrics = response["metrics"]
    output_token = metrics["output_token_count"] if "output_token_count" in metrics else 0
    input_token = metrics["input_token_count"] if "input_token_count" in metrics else 0


    query = """
    INSERT INTO responses
    (id_parent_conv, id_parent_prompt, creation_date, output, total_time, total_tokens)
    VALUES
    (
    :id_conv, :id_prompt, :creation_date, :output, :total_time, :total_tokens
    )
    """

    params = {
       "id_conv": id_conv,
       "id_prompt": id_prompt,
       "creation_date": completed_at,
       "output": "".join(response["output"]),
       "total_time": response["metrics"]["predict_time"],
       "total_tokens": input_token + output_token
    }

    id_resp = commit_query(query, params)

    query_details = """
    INSERT INTO response_details
    (id_resp, version, created_at, started_at, completed_at, status, data_removed, error, replicate_id, logs, total_time, predict_time, tokens_per_second, input_token_count, output_token_count)
    Values
    (
    :id_resp,
    :version,
    :created_at,
    :started_at,
    :completed_at,
    :status,
    :data_removed,
    :error,
    :replicate_id,
    :logs,
    :total_time,
    :predict_time,
    :tokens_per_second,
    :input_token_count,
    :output_token_count
    )
    """
    started_at = from_replicate_date_str(response["started_at"])

    params = {
    "id_resp": id_resp,
    "version":response["version"],
    "model": response["model"],
    "created_at": from_replicate_date_str(response["created_at"]),
    "started_at": started_at,
    "completed_at": completed_at,
    "status":response["status"],
    "data_removed":response["data_removed"],
    "error": response["error"],
    "replicate_id": response["id"],
    "logs":response["logs"],
    "total_time": str(completed_at - started_at),
    "predict_time":response["metrics"]["predict_time"],
    "time_to_first_token":response["metrics"]["time_to_first_token"],
    "tokens_per_second":response["metrics"]["tokens_per_second"],
    "input_token_count": input_token,
    "output_token_count": output_token
    }

    commit_query(query_details, params)

    return id_resp

def insert_conversation(title):
    query = """
        INSERT INTO conversations
        (creation_date, title, visible)
        VALUES
        (:date, :title, 1)
        """

    id_conv =  commit_query(query, params={"date": get_date_str(), "title": title})
    return id_conv


def delete_conversation(id_conv):
    query = """
    UPDATE conversations
    SET visible = 0
    WHERE
    id_conv = :id_conv
    """

    commit_query(query,params={"id_conv": id_conv})

def get_configurations():
    query = """
    SELECT id_conf, name
    FROM configurations
    WHERE
    visible = 1
    """

    results = commit_query(query)

    if len(results) == 0:
        ids = []
        names = []
    else:
        (ids, names) = map(list,zip(*results))

    return {"id_conf": ids, "name": names}

def get_configuration_id_for_conversation(conv_id):
    query = """
    SELECT id_conf
    FROM configurations_for_conversations
    WHERE id_conv = :conv_id
    """

    result = commit_query(query, {"conv_id": conv_id})

    if len(result) == 1:
        return result[0][0]
    else:
        return None


def set_configuration_id_for_conversation(conf_id, conv_id):
    query = """
    DELETE
    FROM configurations_for_conversations
    WHERE id_conv = :conv_id
    """

    commit_query(query, {"conv_id": conv_id})

    query = """
    INSERT INTO configurations_for_conversations
    (id_conf, id_conv)
    VALUES
    (:conf_id, :conv_id)
    """

    commit_query(query, {"conf_id": conf_id, "conv_id": conv_id})

def get_configuration_object(conf_id, time = None):
    config_object = None

    query = """
    SELECT model_name
    FROM configurations
    WHERE id_conf = :conf_id
    """

    result = commit_query(query, {"conf_id": conf_id})

    if len(result)==1:
        model_name = result[0][0]

        if model_name == "meta/meta-llama-3-70b-instruct":
            config_object = llama3_70b_instruct()
        elif model_name == "meta/meta-llama-3.1-405b-instruct":
            config_object = llama31_405b_instruct()

        else:
            return config_object

        config_object.id_conf = conf_id


        query = """
        SELECT name, IIF(value_text is not NULL, value_text, IIF(value_float is not NULL, value_float, value_int)) as value
        from configuration_values
        
        WHERE
        id_parent_conf = :conf_id
        and
        valid_from <= :date
        and 
        valid_until > :date
        """
    if time is None:
        time = datetime.now()
        results = commit_query(query, {"conf_id": conf_id, "date": get_date_str(time)})

        for parameter in results:
            config_object.set_value(parameter[0], parameter[1])


    return config_object


def add_new_configuration(name, model_name):
    query = """
    INSERT INTO CONFIGURATIONS
    (name, model_name, visible)
    VALUES
    (:name, :model_name, 1)
    """

    return commit_query(query, {"name": name, "model_name": model_name})

def remove_configuration(conf_id):
    query = """
    UPDATE configurations
    SET
    visible = 0
    WHERE conf_id = :conf_id
    """

    commit_query(query, {"conf_id": conf_id})

def get_responses_and_corresponding_answers(conv_id):
    query = """
    SELECT p.prompt, r.output
    FROM prompts p
    LEFT JOIN responses r
    ON r.id_parent_prompt = p.id_prompt
    WHERE p.id_parent_conv = :conv_id
    """

    return commit_query(query, {"conv_id": conv_id})

