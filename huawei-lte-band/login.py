#!/usr/bin/python3

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder

from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.exceptions import ResponseErrorLoginCsfrException
from huawei_lte_api.exceptions import LoginErrorUsernamePasswordWrongException

from math_bands import *
from default_value import *

class LoginPage(Screen):
    def verify_credentials(self):
        ip = self.ids["ip"].text
        password = self.ids["passw"].text

        if password == '':
            LoginApp().run()

        if ip == '':
            ip = default_ip

        try:
            if not test_design:
                connection = AuthorizedConnection(f'http://{ip}/', login, password)
                client = Client(connection)
                client.user.logout()
            self.manager.current = "user"
        except LoginErrorUsernamePasswordWrongException:
            pass

class BandPage(Screen):
    def configure_router(self):
        down_bands = self.get_bands()
        up_bands = self.get_bands('_ul')
        down_bands_hex = convert_bands_list2hex(down_bands)
        up_bands_hex = convert_bands_list2hex(up_bands)
        down_list = convert_bands_hex2list(down_bands_hex)
        up_list = convert_bands_hex2list(up_bands_hex)
        print('Download: %s %s' %(down_bands_hex, str(down_list)))
        print('Upload: %s %s' %(up_bands_hex, str(up_list)))

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
    LoginApp().run()
