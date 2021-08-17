def get_int(value):
    return float(value.split('d')[0])

class SignalInfo():
    def __init__(self, client):
        self.signal_info = client.device.signal()

    def get_rsrq(self):
        return get_int(self.signal_info['rsrq'])

    def get_rsrp(self):
        return get_int(self.signal_info['rsrp'])

    def get_sinr(self):
        return get_int(self.signal_info['sinr'])
