from signature import check_sign, sign_init

s, k = sign_init('tmp/192.168.122.36/audit.log')

print(s, k)