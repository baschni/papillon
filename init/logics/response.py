from init.logics.sql_queries import get_date_str

class Response():

    def __init__(self, response_text):

        self.output = response_text
        self.creation_date = get_date_str()

        self.version = None

        self.created_at = None
        self.started_at = None
        self.completed_at = None

        self.status = None
        self.data_removed = None
        self.error = None
        self.replicate_id = None
        self.logs = None

        self.total_time = None
        self.predict_time = None
        self.tokens_per_second = None

        self.input_token_count = None
        self.output_token_count = None
        self.total_tokens = None


