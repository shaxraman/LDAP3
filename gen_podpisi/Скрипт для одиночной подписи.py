import os
import shutil

from ldap3 import Server, Connection

base = 'ou=domain users,dc=icore,dc=local'
serverName = 'icdc0.icore.local'
domainName = 'icore'


def logging():
    userName = 'python'
    password = '123456Qq'
    return userName, password


def connect():
    while True:
        try:
            log = logging()  # Вынесли логин и пароль в infa.py
            server = Server(serverName)
            conn = Connection(server, read_only=True, user=f'{log[0]}@{domainName}', password=log[1],
                              auto_bind=True)
            print(f'Подключение к AD {serverName} под пользователем {log[0]} прошло успешно.\n')
            return conn
        except:
            print('Вы подпустили ошибку?\n')
            continue
        break


a = []


def search_user():
    conn = connect()
    search_filter = f'(&(objectClass=user)(msDS-parentdistname=OU=Domain Users,DC=icore,DC=local))'
    x = conn.search(base, search_filter, attributes=['sAMAccountName'])
    if x != False:
        userDN = conn.response
        print('Всего пользователей в OU=Domain Users -', len(userDN))
        for i in range(len(userDN)):
            a.append(conn.response[i]['attributes']['sAMAccountName'])
    conn.unbind()


def get_attributes(user):
    conn = connect()
    userDN = {}
    search_filter = f'(&(objectClass=user)(sAMAccountName={user}))'
    x = conn.search(base, search_filter,
                    attributes=['displayName', 'mail', 'mobile', 'title', 'telephoneNumber', 'sAMAccountName'])
    if x != False:
        userDN = conn.response[0]['attributes']
    conn.unbind()
    return userDN


def zamena(slovar):
    files = os.listdir(path="./info")  # Откуда берем образец файлов
    new_directory = 'Signatures_' + slovar.get('sAMAccountName')  # Имя для новой директории

    try:
        shutil.copytree(os.path.abspath('./info'),
                        os.path.abspath(f'./{new_directory}'))  # Копируем директорию в новыую папку
    except:
        pass

    for file in files:
        if '.py' in file:
            continue  # Игнорируем питоновские файлы

        if os.path.isfile(f'./{new_directory}/{file}'):  # Проверяем файл ли это
            try:
                s = open(f'./{new_directory}/{file}',
                         encoding='Windows-1251').read()  # Читаем и копируем изменные данные
                print(f'Чтение {file} прошло успешно')
                bb = slovar.get('mobile')
                new_number = ''
                for i in range(len(bb)):
                    if i in [1, 2, 5, 8]:
                        new_number += ' '
                    new_number += bb[i]
                # , ext. vnnumb
                if not slovar.get('telephoneNumber'):
                    lo2 = [', ext. vnnumb', '']
                else:
                    lo2 = ['vnnumb', slovar.get('telephoneNumber')]
                podmena = {
                    'RU_User': slovar.get('displayName'),
                    lo2[0]: lo2[1],
                    'numb': new_number,
                    'RU_Titl': slovar.get('title'),
                    'email': slovar.get('mail'),
                }

                for key, value in podmena.items():  # Замена файлов из словаря
                    s = s.replace(key, value)
            except:
                print(f'Ошибка при чтении файла {file}')

            try:
                f = open(f'{new_directory}/{file}', 'w',
                         encoding='Windows-1251')  # Пишем в другую директорию файл с измененными файлами
                f.write(s)
                f.close()
                print(f'Запись в файл {file} успешна')
            except:
                print(f'Ошибка при записи в файл {file}')


def script_for_all():
    search_user()
    for name in a:
        zamena(get_attributes(name))


if __name__ == '__main__':
    # search_user('snezamov')
    # zamena(search_user())
    zamena(get_attributes('snezamov'))
    zamena(get_attributes('erustamov'))
