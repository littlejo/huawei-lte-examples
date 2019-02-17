#!/usr/bin/python3

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.config import Config
from kivy.core.window import Window

import webbrowser
import crypto

from math_bands import *
from default_value import *
from huawei_lte_lib import *
from design import *

import time

Window.softinput_mode = 'pan'


class LoginPage(BoxLayout):
    def __init__(self,**kwargs):
        super(LoginPage,self).__init__(**kwargs)
        self.monitor_popup = MonitorPage()
        self.about_popup = AboutPage()

    def get_login(self, attribute):
        if Config.has_section(default_section):
            return Config.get(default_section, attribute)
        else:
            return default_login_dict[attribute]

    def get_password(self):
        attribute = 'password'
        if Config.has_section(default_section):
            encoded_passw = Config.get(default_section, attribute)
            return crypto.decode_password(encoded_passw)
        else:
            return default_login_dict[attribute]

    def write_config(self, user, password, ip):
        if not Config.has_section(default_section):
            Config.add_section(default_section)
        Config.set(default_section, 'user', user)
        Config.set(default_section, 'password', crypto.encode_password(password))
        Config.set(default_section, 'ip', ip)
        Config.write()

    def display_about(self):
        self.about_popup.open()

    def verify_credentials(self):
        ip = self.ids["ip"].text
        user = self.ids["user"].text
        password = self.ids["passw"].text

        if ip == '':
            ip = default_login_dict['ip']

        if user == '':
            user = default_login_dict['user']

        huawei_lte.set_login(ip, user, password)

        if test_design or huawei_lte.check_connection():
            print("Good password")
            self.write_config(user, password, ip)
            self.monitor_popup.open()
            self.monitor_popup.monitor()
        else:
            print("Bad password")

class AboutPage(Popup):
    licence_url = 'https://github.com/littlejo/huawei-lte-examples/blob/master/LICENSE'
    github_url = 'https://github.com/littlejo/huawei-lte-examples/'

    def open_url(self, url):
        webbrowser.open(url)

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
        if not test_design:
            info = huawei_lte.get_all_monitor_information()
            print(info)
            self.title = "Monitoring %s" %str(self.score)
            self.title_color =  running_color_list
            self.separator_color = running_color_list
            graphic_signal = Graphic_Signal_Info(info['rsrq'], info['rsrp'], info['sinr'])

            self.rsrq.text = graphic_signal.get_rsrq_string()
            self.rsrq_quality.text = graphic_signal.get_quality_rsrq_string()
            self.rsrq_quality_pr.value = info['rsrq'] * 5 + 115
            self.rsrp.text = graphic_signal.get_rsrp_string()
            self.rsrp_quality.text = graphic_signal.get_quality_rsrp_string()
            self.rsrp_quality_pr.value = (info['rsrp'] + 140) / 1.84
            self.sinr.text = graphic_signal.get_sinr_string()
            self.sinr_quality.text = graphic_signal.get_quality_sinr_string()
            self.sinr_quality_pr.value = (info['sinr'] + 10) * 2.5
            self.upload_rate.text = human_readable_size(info['upload_rate'], 1)
            self.upload_band.text = bands_ui_dict[info['upload_band']]
            self.download_rate.text = human_readable_size(info['download_rate'], 1)
            self.download_band.text = convert_bands_list2str(info['download_band'])
            if self.score >= self.iterations:
                self.title = "Stop"
                self.title_color = stop_color_list
                self.separator_color = stop_color_list
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
    normal_size = '17sp'
    large_size = '35sp'
    def builder(self):
        return Builder.load_file('login.kv')

if __name__ == '__main__':
    huawei_lte = HuaweiLte()
    LoginApp().run()
