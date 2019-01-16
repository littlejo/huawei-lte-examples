from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.exceptions import ResponseErrorLoginCsfrException
from huawei_lte_api.exceptions import LoginErrorUsernamePasswordWrongException

def check_connection(ip, login, password):
    try:
        connection = AuthorizedConnection(f'http://{ip}/', login, password)
        client = Client(connection)
        client.user.logout()
    except LoginErrorUsernamePasswordWrongException:
        return False
    return True
    
