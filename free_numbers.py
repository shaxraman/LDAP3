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
            print('Вы подпустили ошибку☻\n')
            continue
        break


a = []


def search_user():
    conn = connect()
    userDN = {}
    search_filter = f'(&(objectClass=user)(msDS-parentdistname=OU=Domain Users,DC=icore,DC=local))'
    x = conn.search(base, search_filter, attributes=['telephoneNumber'])
    if x != False:
        userDN = conn.response
        for i in range(len(userDN)):
            if userDN[i]['attributes']['telephoneNumber']  :
                a.append(conn.response[i]['attributes']['telephoneNumber'])
    conn.unbind()



def main():
    search_user()
    aa = 700
    bb = 901

    print(f'Добрый день.\nПоиск работает в диапазоне от {aa} до {bb-1} и по {base}.')
    for i in range(aa, bb):
        if str(i) in a:
            continue
        print(i, end=' ')

    input('E for exit ')



if __name__ == '__main__':
    main()
