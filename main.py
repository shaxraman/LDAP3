from ldap3 import Server, Connection

from infa import *


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


ou = ['computers', 'domain computers', 'Domain Controllers', 'Domain Servers']
# 212  LockedAccounts   154 without LockedAccounts
res = {}
oper_sys = []

def search_os():
    conn = connect()
    search_filter = f'(&(objectClass=Computer))'
    for kk in ou:
        base1 = f'ou={kk},dc=icore,dc=local'
        conn.search(base1, search_filter, attributes=['operatingSystem'])
        a = 'Всего операционных систем в ou=domain computers', len(conn.response)
        for i in conn.response:
            if 'LockedAccounts' in i['dn']:
                continue
            oper_sys.append(i['attributes']['operatingSystem'])
            print(i)
        print('\n\n', a)
        print('Не считая LockedAccounts ', len(oper_sys))
    conn.unbind()
    for i in oper_sys:
        #print(res.keys())
        try:
            if i not in res.keys():
                res[i] = 1  # Добавляем ключ: значение в словарь
            else:
                res[i] = res.get(i) + 1  # Обновляем значение у выбранного ключа
        except TypeError:
            print('какая-то шибка')

    print('os = ')
    [print(i) for i in res.items()]


    return res


def main():
    search_os()
    #[print(i) for i in res.items()]
    input('Нажмите любую клавишу для выхода.')


if __name__ == '__main__':
    main()
