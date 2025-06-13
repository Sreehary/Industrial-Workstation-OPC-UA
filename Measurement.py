from datetime import datetime


class Measurement:

    def __init__(self, iD, tag, value_type, value):
        self.iD = iD
        self.tag = tag
        self.value = value
        self.value_type = value_type
        self.error_string = "No Error"
        self.error_code = "E000"
        self.start_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.run_time = 0

    def set_measurement(self, value):
        self.value = value

    def get_measurement(self):
        self.run_time = str(datetime.now() - datetime.strptime(self.start_time, "%Y-%m-%d %H:%M:%S"))
        return self

