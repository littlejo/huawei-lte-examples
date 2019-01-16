from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.exceptions import ResponseErrorLoginCsfrException
from huawei_lte_api.exceptions import LoginErrorUsernamePasswordWrongException

class HuaweiLte:
    def set_login(self, ip, login, password):
        self.ip = ip
        self.login = login
        self.password = password

    def check_connection(self):
        try:
            connection = AuthorizedConnection(f'http://{self.ip}/', self.login, self.password)
            client = Client(connection)
            client.user.logout()
        except LoginErrorUsernamePasswordWrongException:
            return False
        return True

    def get_bands_number(self):
        try:
            connection = AuthorizedConnection(f'http://{self.ip}/', self.login, self.password)
            client = Client(connection)
            self.net_mode = client.net.net_mode()
            client.user.logout()
        except LoginErrorUsernamePasswordWrongException:
            return False
        return self.net_mode['LTEBand']
