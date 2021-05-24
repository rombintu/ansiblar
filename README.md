# Audit Automated System

## Зависимости (установка дальше)
```
ansible
python3
openssh
```

## Подготовка
```
pip3 install venv
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
ansible-vault decrypt config.json.encode
cp config.json.encode config.json
python model.py
```
    *test vault-pass = 1*  
    edit file config.json  

```
cp config.json config.json.encode
ansible-vault decrypt config.json.encode
```

## Создание файла Inventory
```
python3 main.py init
```
    output file: 
        * inventory

## Запуск сканирования уязвимости систем
```
ansible-playbook audit.yml -i inventory
```

## Сбор логов
```
python main.py getlogs
```
    create files: 
        * audit.log
        * lynis.log

### Проверка соединения
```
python main.py ping
```
    output:  
    PONG! =>> Linux alpine  
    PONG! =>> Linux alpine  

### Выборка данных с базы данных
```
python main.py select
```
    output:  
    | Host: 192.168.1.35 | Last update: 2021-05-24 14:43:22.469166 |  
    | Host: 192.168.1.36 | Last update: 2021-05-24 14:43:22.469166 |  