import time

class Timer:
    def __init__(self, message = "", muted=False):
        self.stamps = [time.time()]
        self.muted = muted
        if message != "" and not muted:
            print(message)

    def print(self, message = ""):
        if not self.muted:
            current_stamp, previous_stamp = self.add_time_stamp()
            print(message,current_stamp-previous_stamp)

    def get_last_stamp(self):
        return self.stamps[-1]

    def get_current_stamp(self):
        return time.time()
    def add_time_stamp(self):
        previous_stamp = self.get_last_stamp()
        current_stamp = self.get_current_stamp()
        self.stamps.append(current_stamp)
        return(current_stamp, previous_stamp)

    def time_difference_last_stamp_to_now(self):
        return self.get_current_stamp() - self.get_last_stamp()