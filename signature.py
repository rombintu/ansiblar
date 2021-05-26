import os

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Util import asn1
from base64 import b64decode

def sign_init(file_name):
    # Генерируем новый ключ
    key = RSA.generate(1024, os.urandom)
    # Получаем хэш файла
    hesh = SHA256.new()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hesh.update(chunk)

    # Подписываем хэш
    signature = pkcs1_15.new(key).sign(hesh)

    # Получаем открытый ключ из закрытого
    pubkey = key.publickey()
    print(pubkey, signature)
    return pubkey, signature

def check_sign(file_name, k_pem, s_pem):
    def read_pem(file):
        with open(file, "rb") as f:
            return f.read()
    
    pubkey = read_pem(k_pem)
    signature = b64decode(read_pem(s_pem))

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