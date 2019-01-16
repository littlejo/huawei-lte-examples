#!/usr/bin/python3

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder

from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.exceptions import ResponseErrorLoginCsfrException
from huawei_lte_api.exceptions import LoginErrorUsernamePasswordWrongException

login = 'admin'
default_ip = '192.168.1.1'
test_design = True

bands_list = [
    'b1',
    'b2',
    'b3',
    'b4',
    'b5',
    'b6',
    'b7',
    'b8',
    'b19',
    'b20',
    'b26',
    'b28',
    'b32',
    'b38',
    'b40',
    'b41',
]


def convert_bands_list2hex(bands_list):
    res_int = 0
    for band in bands_list:
        power = int(band.replace('b', '')) - 1
        res_int += 2 ** power
    return str(hex(res_int)).replace('0x', '')

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
        print(convert_bands_list2hex(down_bands))
        print(convert_bands_list2hex(up_bands))

    def get_bands(self, postfix_str=''):
        res_bands_list = []
        for band in bands_list:
            if self.ids[band + postfix_str].active:
                res_bands_list.append(band)
        return res_bands_list

class ScreenManagement(ScreenManager):
    pass


class LoginApp(App):
    band_color_1 = [0.1, 0.1 , 0.1 , 0.1]
    band_color_2 = [0.2, 0.2, 0.5, 0.2]
    def builder(self):
        return Builder.load_file('login.kv')

if __name__ == '__main__':
    LoginApp().run()
