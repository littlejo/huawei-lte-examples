#!/usr/bin/python3

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder

from math_bands import *
from default_value import *
from huawei_lte_lib import *

class LoginPage(Screen):
    def verify_credentials(self):
        ip = self.ids["ip"].text
        password = self.ids["passw"].text

        if password == '':
            LoginApp().run()

        if ip == '':
            ip = default_ip

        huawei_lte.set_login(ip, login, password)

        if test_design or huawei_lte.check_connection():
            print("Good password")
            self.manager.current = "user"
        else:
            print("Bad password")

class BandPage(Screen):
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
    def builder(self):
        return Builder.load_file('login.kv')

if __name__ == '__main__':
    huawei_lte = HuaweiLte()
    LoginApp().run()
