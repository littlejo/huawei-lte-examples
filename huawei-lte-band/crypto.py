from Crypto.Cipher import AES
import base64

secret_key_utf8 = '1234567890123456'.encode("utf-8")

def encode_password(password):
    passw = password.rjust(32)
    cipher = AES.new(secret_key_utf8, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(passw.encode("utf-8"))).decode("utf-8")

def decode_password(encoded_password):
    cipher = AES.new(secret_key_utf8, AES.MODE_ECB)
    return cipher.decrypt(base64.b64decode(encoded_password.encode("utf-8"))).strip()
