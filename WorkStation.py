class WorkStation:

    def __init__(self, iD, tag):
        self.iD = iD
        self.tag = tag
        self.devices = {}

    def add_device(self, device):
        if device.iD not in self.devices.keys():
            self.devices[str(device.iD)] = device

    def set_measurement(self, DiD, MiD, value):
        if DiD in self.devices.keys():
            self.devices[str(DiD)].set_measurement(MiD, value)

    def get_work_station(self):
        return self



