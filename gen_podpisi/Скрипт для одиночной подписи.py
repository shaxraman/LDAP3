import os
import shutil
import getpass
from ldap3 import Server, Connection

base = 'ou=domain users,dc=icore,dc=local'
serverName = 'icdc0.icore.local'
domainName = 'icore'


def logging():
    """ Данные для подключения к AD"""
    userName = 'python'
    password = '123456Qq'
    return userName, password


def connect():
    """ Цикл подключения к AD"""
    while True:
        try:
            log = logging()
            server = Server(serverName)
            conn = Connection(server, read_only=True, user=f'{log[0]}@{domainName}', password=log[1],
                              auto_bind=True)
            print(
                f'Подключение к AD {serverName} под пользователем {log[0]} прошло успешно.\n')
            return conn
        except:
            print('Вы подпустили ошибку?\n')
            continue
        break


a = []


def get_attributes(user):
    """ Парсит нужные данные для из AD """
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
    """ Делает копию папки infi с нужным человоком """
    files = os.listdir(path="./info")  # Откуда берем образец файлов
    new_directory = 'Signatures_' + \
        slovar.get('sAMAccountName')  # Имя для новой директории

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


def zamena2(name):
    """ Делает копию папки infi с нужным человоком """
    files = os.listdir(path="./info")  # Откуда берем образец файлов
    # Новая папка
    new_directory = f'C:/Users/{getpass.getuser()}/AppData/Roaming/Microsoft/Signatures'

    try:
        shutil.copytree(os.path.abspath('./info'),
                        os.path.abspath(f'{new_directory}'))  # Копируем директорию в новыую папку
    except Exception as e:
        print("type error: " + str(e))

    for file in files:
        if '.py' in file:
            continue  # Игнорируем питоновские файлы

        if os.path.isfile(f'{new_directory}/{file}'):  # Проверяем файл ли это
            try:
                s = open(f'{new_directory}/{file}',
                         encoding='Windows-1251').read()  # Читаем и копируем изменные данные
                print(f'Чтение {file} прошло успешно')
                bb = name.get('mobile')
                new_number = ''
                for i in range(len(bb)):
                    if i in [1, 2, 5, 8]:
                        new_number += ' '
                    new_number += bb[i]
                # , ext. vnnumb
                if not name.get('telephoneNumber'):
                    lo2 = [', ext. vnnumb', '']
                else:
                    lo2 = ['vnnumb', name.get('telephoneNumber')]
                podmena = {
                    'RU_User': name.get('displayName'),
                    lo2[0]: lo2[1],
                    'numb': new_number,
                    'RU_Titl': name.get('title'),
                    'email': name.get('mail'),
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


def script_for_one():
    name = input('Введите логин пользователя ')
    zamena(get_attributes(name))


if __name__ == '__main__':
    # script_for_one()
    while True:
        choice = input("1 - Создать файл для текущего пользователя\n\
                        2 - Для текущего и добавить в нужную папку\n\
                        3 - Указать имя вручную\n\
                        0 - Для выхода\n")
        if choice == str(1):
            zamena(get_attributes(getpass.getuser()))
            print("Пока")
            break

        if choice == str(2):
            zamena2(get_attributes(getpass.getuser()))
            print("Пока")
            break

        if choice == str(3):
            script_for_one()
            print("Пока")
            break

        if choice == str(0):
            print("Пока")
            break
