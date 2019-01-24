import getpass

from ldap3 import Server, Connection

from infa import *


def connect():
    while True:
        try:
            userName = input('Напишите Ваш логин ')
            if '@' in userName:
                userName = userName[:userName.index('@')]
            elif '.i' in userName:
                userName = userName[:userName.index('.i')]
            password = getpass.getpass()
            server = Server(serverName)
            conn = Connection(server, read_only=True, user=f'{userName}@{domainName}', password=password,
                              auto_bind=True)
            print(f'Подключение к AD {serverName} под пользователем {userName} прошло успешно.\n')
            return conn
        except:
            print('Вы подпустили ошибку☻\n')
            continue
        break


def search_user(user):
    conn = connect()
    userDN = None
    search_filter = f'(&(objectClass=user)(sAMAccountName={user}))'
    x = conn.search(base, search_filter, attributes=['distinguishedName'])
    if x != False:
        userDN = conn.response[0]['attributes']['distinguishedName']
    conn.unbind()
    print(userDN)


# 212  LockedAccounts   154 without LockedAccounts
res = {}


def search_os():
    conn = connect()
    oper_sys = []
    search_filter = f'(&(objectClass=Computer))'
    conn.search(base2, search_filter, attributes=['operatingSystem'])
    a = 'Всего операционных систем в ou=domain computers', len(conn.response)
    for i in conn.response:
        if 'LockedAccounts' in i['dn']:
            continue
        oper_sys.append(i['attributes']['operatingSystem'])
        print(i)
    conn.unbind()
    print('\n\n', a)
    print('Не считая LockedAccounts ', len(oper_sys))
    for i in oper_sys:
        if i not in res.keys():
            res[i] = 1  # Добавляем ключ: значение в словарь
        else:
            res[i] = res.get(i) + 1  # Обновляем значение у выбранного ключа
    [print(i) for i in res.items()]
    return res


def main():
    search_os()

    input('Нажмите любую клавишу для выхода.')


if __name__ == '__main__':
    main()
