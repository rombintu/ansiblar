import os

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Util import asn1
from base64 import b64decode

# TESTS
# keys = '/root/ansiblar/tmp'
# keys = 'tmp/192.168.122.76'

def sign_init(file_name):
    # Генерируем новый ключ
    private_key = RSA.generate(1024, os.urandom)
    # Получаем хэш файла
    hesh = SHA256.new()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hesh.update(chunk)

    # Подписываем хэш
    signature = pkcs1_15.new(private_key).sign(hesh)

    # Получаем открытый ключ из закрытого
    pub_key = private_key.publickey().exportKey(format='PEM')
    return pub_key, signature

def check_sign(file_name, k_pem, s_pem):
    def read_pem(file):
        if b:
            with open(file, "r") as f:
                return f.read()
    
    pubkey = RSA.importKey(read_pem(k_pem))
    signature = read_pem(s_pem)

    hesh = SHA256.new()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hesh.update(chunk)
    # Переменная для проверки подписи
    check_sign = False
    try:
        pkcs1_15.new(pubkey).verify(hesh, signature)
        check_sign = True
        return check_sign
    except Exception as e:
        print(e)
        return check_sign   