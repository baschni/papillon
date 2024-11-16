from config import DATA_BASE_PATH
import sqlite3
from os.path import exists
from datetime import datetime
def get_db_handler(path):
    if not exists(path):
        db = initiate_database(path)
    else:
        db = sqlite3.connect(path)

    return db


def create_table_queries():
    sql_conversations = """
    CREATE TABLE conversations (
    id_conv INTEGER PRIMARY KEY,
    creation_date TEXT,
    title TEXT,
    visible INTEGER
    )
    """

    sql_prompt_history = """
    CREATE TABLE prompt_history (
    id_hist INTEGER PRIMARY KEY,
    id_parent_conv INTEGER
    )
    """

    sql_history_changes = """
    CREATE TABLE prompt_history_changes (
    id_change INTEGER PRIMARY KEY,
    id_parent_hist INTEGER,
    date TEXT,
    prompt TEXT
    )
    """


    sql_configurations = """
    CREATE TABLE configurations (
    id_conf INTEGER PRIMARY KEY,
    model_name TEXT,
    name TEXT,
    visible INTEGER
    )
    """


    sql_configuration_values = """
    CREATE TABLE configuration_values (
    id_parent_conf INTEGER,
    valid_from TEXT,
    valid_until TEXT,
    name TEXT,
    value_text TEXT,
    value_float REAL,
    value_int INTEGER
    )
    """

    sql_configuration_by_conversation = """
    CREATE TABLE configurations_for_conversations (
    id_conv INTEGER,
    id_conf INTEGER
    )
    """

    sql_prompts = """
    CREATE TABLE prompts (
    id_prompt INTEGER PRIMARY KEY,
    id_parent_conv INTEGER,
    id_conf INTEGER,
    creation_date TEXT,
    prompt TEXT,
    total_prompt TEXT
    )
    """

    # sql_prompt_parameters = """
    # CREATE TABLE prompt_parameters (
    # id_prompt INTEGER,
    # parameter_name TEXT,
    # parameter_value_str TEXT,
    # parameter_value_int INTEGER,
    # parameter_value_float REAL
    # )
    # """

    # prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",

    sql_responses = """
    CREATE TABLE responses (
    id_resp INTEGER PRIMARY KEY,
    id_parent_conv INTEGER,
    id_parent_prompt INTEGER,
    creation_date TEXT,
    output TEXT,
    total_time REAL,
    total_tokens INTEGER
    )
    """

    sql_response_details = """
    CREATE TABLE response_details (
    id_resp INTEGER,
    version TEXT,
    model TEXT,
    created_at TEXT,
    started_at TEXT,
    completed_at TEXT,
    status TEXT,
    data_removed TEXT,
    error TEXT,
    replicate_id TEXT,
    logs TEXT,
    total_time REAL,
    predict_time REAL,
    time_to_first_token REAL,
    tokens_per_second REAL,
    input_token_count INTEGER,
    output_token_count INTEGER
    )
    """

    return [sql_configurations, sql_configuration_values, sql_configuration_by_conversation, sql_conversations, sql_prompt_history, sql_history_changes, sql_prompts, sql_responses, sql_response_details]


def initiate_database(path):
    db = sqlite3.connect(path)
    cursor = db.cursor()

    queries = create_table_queries()

    for query in queries:
        try:
            cursor.execute(query)
        except Exception:
            print(query)
            raise Exception

    db.commit()
    return db
def commit_query(query, params=None, db=None):
    query=query.strip()

    if db is None:
        db = get_db_handler(DATA_BASE_PATH)

    cursor = db.cursor()
    try:
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
    except Exception:
        print(query)
        raise Exception

    db.commit()

    if query[:len("INSERT")].lower() == "insert":
        return_value =  cursor.lastrowid
    #check for select query
    elif cursor.description is not None:
        return_value = cursor.fetchall()
    else:
        return_value = None
    # print("now", cursor.lastrowid)
    # rowid = int(cursor.lastrowid)
    # print(rowid)
    cursor.close()
    db.close()

    return return_value

def get_max_date():
    return "9999-12-31 24:59:59.999"

def get_date_str(date=None):
    if date is None:
        date = datetime.now()

    return date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def from_date_str(date_str):
    return datetime.strptime(date_str+"000", "%Y-%m-%d %H:%M:%S.%f")


def update_bitemporal_configuration_value(id_conf, name, value, type):

    max_date = get_max_date()

    query = """
    UPDATE configuration_values
    SET valid_until = :now
    WHERE
    id_parent_conf = :id_conf
    AND
    valid_from <= :now
    and 
    valid_until > :now
    and
    name = :name
    """
    now = get_date_str()
    parameters = {"id_conf": id_conf, "now": now, "name": name}

    commit_query(query, parameters)

    query = f"""
    INSERT INTO configuration_values
    (id_parent_conf, name, value_{type}, valid_from, valid_until)
    VALUES
    (
    :id_conf,
    :name,
    :value,
    :now,
    :max_date
    )
    """
    print(query)
    print(value)

    parameters = {"id_conf": id_conf, "name": name, "value": value, "now": now, "max_date": max_date}

    commit_query(query, parameters)