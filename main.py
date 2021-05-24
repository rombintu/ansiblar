import os
import json
import sys
import paramiko 


# https://ru.wikibooks.org/wiki/SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Берем наш класс (модель таблички с историями)
from model import Audited

from datetime import datetime

# GLOBAL
config = os.getcwd() + '/config.json'
tmp = os.getcwd() + '/tmp'

# FUNCTIONS
def get_hosts_data(config='config.json'):
    hosts = []
    users = []
    passw = []
    ports = []
        
    with open(config, 'r') as f:
        data = json.loads(f.read())
        arr = [el for el in data.items()]

        for el in arr:
            hosts.append(el[1]['host'])
            users.append(el[1]['user'])
            passw.append(el[1]['pass'])
            ports.append(el[1]['port'])

    return hosts, users, passw, ports

def init():
    hosts, users, passw, ports = get_hosts_data(config)

    with open(os.getcwd() + '/inventory', 'w') as f:
        f.write("[hosts]\n")
        for i, host in enumerate(hosts):
            f.write(f'{host} ansible_ssh_user={users[i]} ansible_sudo_pass={passw[i]}\n')
        f.close()
    print('Создан новый файл INVENTORY')

def select():
    # Если нужна postgres то раскоменчиваем следующую строчку
    # engine = create_engine('postgresql://test:password@localhost:5432/audit')
    engine = create_engine('sqlite:///db.sqlite')
    Session = sessionmaker(bind=engine)
    session = Session()
    audit_data = session.query(Audited).all()
    if audit_data:
        for ad in audit_data:
            print(f"| Host: {ad.host} | Last update: {ad.date} |")
    else:
        print('Нет данных')
    session.close()

def ping():
    hosts, users, passw, ports = get_hosts_data(config)

    for i, host in  enumerate(hosts):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=users[i], password=passw[i], port=ports[i])
        stdin, stdout, stderr = client.exec_command('uname -a')
        print('PONG! =>> ')
        data = stdout.read() + stderr.read()
        print(data.decode())
        client.close()

def getlogs():
    hosts, users, passw, ports = get_hosts_data(config)
    date = datetime.utcnow()
    engine = create_engine('sqlite:///db.sqlite')
    Session = sessionmaker(bind=engine)
    session = Session()

    for i, host in  enumerate(hosts):
        try:
            os.mkdir(tmp + f'/{host}')
        except:
            print("Директория уже существует, пропускается")

        os.system(f'scp -P {ports[i]} {users[i]}@{host}:/tmp/* {tmp}/{host}')
        audit_data = Audited(host, date)
        # Добавляем
        session.add(audit_data)

    # Сохраняем
    session.commit()

if __name__ == "__main__":
    print('Start program...')
    user_command = sys.argv[1]

    if user_command == 'init':
        init()
    elif user_command == 'select':
        select()
    elif user_command == 'getlogs':
        getlogs()
    elif user_command == 'ping':
        ping()