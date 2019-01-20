#!/usr/bin/python3

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock

from math_bands import *
from default_value import *
from huawei_lte_lib import *
from GraphicSignalInfo import *

import time

def human_readable_size(size, decimal_places):
    for unit in ['bps','Kbps','Mbps','Gbps','Tbps']:
        if size < 1000.0:
            if unit == 'bps':
                decimal_places = 0
            break
        size /= 1000.0
    return f"{size:.{decimal_places}f}{unit}"

def convert_bands_list2str(bands_list):
    res_str = ''
    for band in bands_list:
        res_str += bands_ui_dict[band] + '\n'
    return res_str


class LoginPage(BoxLayout):
    def __init__(self,**kwargs):
        super(LoginPage,self).__init__(**kwargs)
        self.monitor_popup = MonitorPage()
        self.band_popup = BandPage()

    def verify_credentials(self):
        ip = self.ids["ip"].text
        password = self.ids["passw"].text

        if ip == '':
            ip = default_ip

        huawei_lte.set_login(ip, login, password)

        if test_design or huawei_lte.check_connection():
            print("Good password")
            self.monitor_popup.open()
            self.monitor_popup.monitor()
        else:
            print("Bad password")

class MonitorPage(Popup):
    def __init__(self,**kwargs):
        super(MonitorPage,self).__init__(**kwargs)
        self.band_popup = BandPage()

    def display_info(self):
        print(huawei_lte.get_all_monitor_information())

    def monitor(self, iteration=10):
        self.iterations = iteration
        self.score = 0
        self.event = Clock.schedule_interval(self.set_label, 1)


    def set_label(self, dt):
        self.score += 1
        info = huawei_lte.get_all_monitor_information()
        print(info)
        self.title = "Monitoring %s" %str(self.score)
        graphic_signal = Graphic_Signal_Info(info['rsrq'], info['rsrp'], info['sinr'])

        self.rsrq.text = graphic_signal.get_rsrq_string()
        self.rsrq_quality.text = graphic_signal.get_quality_rsrq_string()
        self.rsrp.text = graphic_signal.get_rsrp_string()
        self.rsrp_quality.text = graphic_signal.get_quality_rsrp_string()
        self.sinr.text = graphic_signal.get_sinr_string()
        self.sinr_quality.text = graphic_signal.get_quality_sinr_string()
        self.upload_rate.text = human_readable_size(info['upload_rate'], 1)
        self.upload_band.text = bands_ui_dict[info['upload_band']]
        self.download_rate.text = human_readable_size(info['download_rate'], 1)
        self.download_band.text = convert_bands_list2str(info['download_band'])
        if self.score >= self.iterations:
            self.event.cancel()

class BandPage(Popup):

    def configure_router(self):
        down_bands = self.get_bands()
        up_bands = self.get_bands('_ul')
        self.down_bands_hex = convert_bands_list2hex(down_bands)
        self.up_bands_hex = convert_bands_list2hex(up_bands)
        self.set_bands()

    def get_bands(self):
        current_bands_hex = huawei_lte.get_bands_number()
        current_bands_list = convert_bands_hex2list(current_bands_hex)
        print(f'Download :  {current_bands_list} {current_bands_hex}')

    def set_bands(self):
        print(f'Set upload band: {self.up_bands_hex}')
        huawei_lte.set_bands_number(self.up_bands_hex)
        print(f'Set download band: {self.down_bands_hex}')
        huawei_lte.set_bands_number(self.down_bands_hex)
        self.get_bands()

    def get_bands(self, postfix_str=''):
        res_bands_list = []
        for band in bands_list:
            if self.ids[band + postfix_str].active:
                res_bands_list.append(band)
        return res_bands_list

class ScreenManagement(ScreenManager):
    pass


class LoginApp(App):
    band_color_1 = [0.1, 0.1, 0.1, 0.1]
    band_color_2 = [0.2, 0.2, 0.5, 0.2]
    bands_dict = bands_ui_dict
    def builder(self):
        return Builder.load_file('login.kv')

if __name__ == '__main__':
    huawei_lte = HuaweiLte()
    LoginApp().run()
