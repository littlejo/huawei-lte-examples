import math
import TrafficInfo

def human_readable_size(size, decimal_places):
    for unit in ['bps','Kbps','Mbps','Gbps','Tbps']:
        if size < 1000.0:
            if unit == 'bps':
                decimal_places = 0
            break
        size /= 1000.0
    return f"{size:.{decimal_places}f}{unit}"

def number_scale(size):
    if size == 0:
        return 0
    elif int(math.log2(size)) <= 0:
        return 1
    else:
        return int(math.log2(size)) + 1

def get_scale(number_rate):
    unicode_int = 219
    if number_rate == 1:
        unicode_int = 221
    else:
        number_rate -= 1
    return number_rate  * bytes((unicode_int,)).decode('cp437')

class Graphic_Traffic_Info():
    def __init__(self, client):
        traffic_info = TrafficInfo.TrafficInfo(client)
        self.dwn_rate = traffic_info.get_download_rate()
        self.up_rate = traffic_info.get_upload_rate()

    def get_human_dwn_rate(self, decimal=2):
        return human_readable_size(self.dwn_rate, decimal)

    def get_human_up_rate(self, decimal=2):
        return human_readable_size(self.up_rate, decimal)

    def get_dwn_num_rate(self):
        return number_scale(self.dwn_rate / 80000)

    def get_up_num_rate(self):
        return number_scale(self.up_rate / 80000)

    def get_dwn_rate_scale(self):
        return get_scale(self.get_dwn_num_rate())

    def get_up_rate_scale(self):
        return get_scale(self.get_up_num_rate())

    def get_dwn_padding(self, max_length=10):
        return (max_length - self.get_dwn_num_rate()) * ' '

    def get_up_padding(self, max_length=10):
        return (max_length - self.get_up_num_rate()) * ' '

    def get_dwn_string(self):
        dwn_rate = self.get_human_dwn_rate()
        dwn_graphic_rate = self.get_dwn_rate_scale()
        dwn_padding = self.get_dwn_padding() 
        return f'|{dwn_graphic_rate}{dwn_padding}| {dwn_rate}'

    def get_up_string(self):
        up_rate = self.get_human_up_rate()
        up_graphic_rate = self.get_up_rate_scale()
        up_padding = self.get_up_padding() 
        return f'  |{up_graphic_rate}{up_padding}| {up_rate}'
