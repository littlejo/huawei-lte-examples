from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.exceptions import ResponseErrorLoginCsfrException
from huawei_lte_api.exceptions import LoginErrorUsernamePasswordWrongException

class HuaweiLte:
    def set_login(self, ip, login, password):
        self.url = f'http://{ip}/'
        self.login = login
        self.password = password

    def init_connection(self):
        connection = AuthorizedConnection(self.url, self.login, self.password)
        self.client = Client(connection)

    def close_connection(self):
        self.client.user.logout()

    def check_connection(self):
        try:
            self.init_connection()
            self.close_connection()
        except LoginErrorUsernamePasswordWrongException:
            return False
        return True

    def init_net_mode(self):
        self.net_mode = self.client.net.net_mode()
        self.network_mode = self.net_mode['NetworkMode']
        self.network_band = self.net_mode['NetworkBand']
        self.lte_band = self.net_mode['LTEBand']

    def get_bands_number(self):
        try:
            self.init_connection()
            self.init_net_mode()
            self.close_connection()
        except LoginErrorUsernamePasswordWrongException:
            return False
        return self.lte_band

    def set_bands_number(self, number):
        try:
            self.init_connection()
            self.lte_band = number
            self.net_mode = self.client.net.set_net_mode(self.lte_band, self.network_band, self.network_mode)
            self.close_connection()
        except LoginErrorUsernamePasswordWrongException:
            return False
