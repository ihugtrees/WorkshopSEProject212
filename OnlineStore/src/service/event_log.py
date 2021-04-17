
class Event_Log:
    def __init__(self, log_list = list(), error_list = list()):
        self.log_list = log_list
        self.error_list = error_list


    def add_event(self, event):
        self.log_list.append(event)

    def add_error(self, event):
        self.error_list.append(event)