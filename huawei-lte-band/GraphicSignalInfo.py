lte_quality_signal_dict = {
                   'rsrp': (-80, -90, -100),
                   'rsrq': (-10, -15, -20),
                   'sinr': (20, 13, 0),
                  }

class bcolors:
    OKBLUE = '[color=89cff0]'
    OKGREEN = '[color=39c563]'
    WARNING = '[color=e9d66b]'
    FAIL = '[color=ff3333]'

conditions_list = ['A+',  'A',  'B', 'C']
colors_list = [bcolors.OKBLUE, bcolors.OKGREEN, bcolors.WARNING, bcolors.FAIL]

stop_color = '[/color]'


def get_quality_signal(value, signal):
    for index, threshold in enumerate(lte_quality_signal_dict[signal]):
        if value >= threshold:
            return conditions_list[index]
    return conditions_list[3]

def get_color_signal(value, signal):
    for index, threshold in enumerate(lte_quality_signal_dict[signal]):
        if value >= threshold:
            return colors_list[index]
    return colors_list[3]

class Graphic_Signal_Info():
    def __init__(self, rsrq, rsrp, sinr):
        self.rsrq = rsrq
        self.rsrp = rsrp
        self.sinr = sinr

    def get_quality_rsrq(self):
        return get_quality_signal(self.rsrq, 'rsrq')

    def get_quality_rsrp(self):
        return get_quality_signal(self.rsrp, 'rsrp')

    def get_quality_sinr(self):
        return get_quality_signal(self.sinr, 'sinr')

    def get_color_rsrq(self):
        return get_color_signal(self.rsrq, 'rsrq')

    def get_color_rsrp(self):
        return get_color_signal(self.rsrp, 'rsrp')

    def get_color_sinr(self):
        return get_color_signal(self.sinr, 'sinr')

    def get_rsrq_string(self):
        rsrq = self.rsrq
        rsrq_cdt = self.get_quality_rsrq() 
        rsrq_color = self.get_color_rsrq() 
        return f'{rsrq_color}{rsrq}dB{stop_color}'

    def get_quality_rsrq_string(self):
        rsrq = self.rsrq
        rsrq_cdt = self.get_quality_rsrq() 
        rsrq_color = self.get_color_rsrq() 
        return f'{rsrq_color}{rsrq_cdt}{stop_color}'

    def get_rsrp_string(self):
        rsrp = self.rsrp
        rsrp_cdt = self.get_quality_rsrp() 
        rsrp_color = self.get_color_rsrp() 
        return f'{rsrp_color}{rsrp}dBm{stop_color}'

    def get_quality_rsrp_string(self):
        rsrp = self.rsrp
        rsrp_cdt = self.get_quality_rsrp() 
        rsrp_color = self.get_color_rsrp() 
        return f'{rsrp_color}{rsrp_cdt}{stop_color}'

    def get_sinr_string(self):
        sinr = self.sinr
        sinr_cdt = self.get_quality_sinr() 
        sinr_color = self.get_color_sinr() 
        return f'{sinr_color}{sinr}dB{stop_color}'

    def get_quality_sinr_string(self):
        sinr = self.sinr
        sinr_cdt = self.get_quality_sinr() 
        sinr_color = self.get_color_sinr() 
        return f'{sinr_color}{sinr_cdt}{stop_color}'

