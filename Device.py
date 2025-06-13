class Device:

    def __init__(self, iD, tag):
        self.iD = iD
        self.tag = tag
        self.measurements = {}

    def add_measurement(self, measurement):
        if measurement.iD not in self.measurements.keys():
            self.measurements[str(measurement.iD)] = measurement

    def set_measurement(self, iD, value):
        if iD in self.measurements.keys():
            self.measurements[str(iD)].set_measurement(value)

    def get_device(self):
        return self

