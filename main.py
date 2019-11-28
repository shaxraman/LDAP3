from pprint import pprint
from ldap3 import Server, Connection, MODIFY_REPLACE

from infa import *


def connect():
    """ Подключение к AD """
    while True:
        try:
            log = logging()  # Вынесли логин и пароль в infa.py
            server = Server(serverName)
            conn = Connection(server, read_only=False, user=f'{log[0]}@{domainName}', password=log[1],
                              auto_bind=True)
            print(
                f'Подключение к AD {serverName} под пользователем {log[0]} прошло успешно.\n')
            return conn
        except:
            print('Вы подпустили ошибку☻\n')
            continue
        break


def search_ext1(user):
    """ Поиск ext1 у конкретного юзера"""
    conn = connect()
    userDN = None
    search_filter = f'(&(objectClass=user)(sAMAccountName={user}))'
    x = conn.search(base, search_filter, attributes=[
                    'extensionAttribute1', 'distinguishedName'])
    if x != False:
        userDN = (conn.response[0]['attributes']['extensionAttribute1'],
                  conn.response[0]['attributes']['distinguishedName'])
    # print(conn.modify('CN=Stanislav Nezamov,OU=Domain Users,DC=icore,DC=local', {'extensionAttribute1': (MODIFY_REPLACE, ['3769'])}))   # замена атрибута
    print(userDN)


def search_ext1_all():
    """ Ищет всех пользователей и выводит их атрибуты"""
    conn = connect()
    all_user = None
    search_filter = f'(&(objectClass=user)(msDS-parentdistname=OU=Domain Users,DC=icore,DC=local))'  # f'(&(objectClass=user)(msDS-parentdistname=OU=Domain Users,DC=icore,DC=local))'  f'(&(objectClass=user))'
    x = conn.search(base, search_filter, attributes=[
                    'extensionAttribute1', 'distinguishedName', 'telephoneNumber', 'ipPhone'])
    if x != False:
        all_user = (conn.response)
    conn.unbind()
    return all_user


def replace_attribute(all_users):
    """ Принимает список юзеров с их атрибутами (search_ext1_all) и заменяет определенные """
    conn = connect()
    for user in all_users:
        try:
            if user['attributes']['telephoneNumber']:
                print(user['attributes']['extensionAttribute1'])
                print(conn.modify(user['attributes']['distinguishedName'], {'extensionAttribute1': (
                    MODIFY_REPLACE, [str(3) + str(user['attributes']['telephoneNumber'])])}))
        except Exception as e:
            pprint(e)

    conn.unbind()


def replace_ip_phone_attribute(all_users):
    """ Принимает список юзеров с их атрибутами (ip_phone) и заменяет определенные """
    conn = connect()
    for user in all_users:
        try:
            if user['attributes']['telephoneNumber']:
                print(user['attributes']['ipPhone'])
                print(conn.modify(user['attributes']['distinguishedName'], {'ipPhone': (
                    MODIFY_REPLACE, [str(1) + str(user['attributes']['telephoneNumber'])])}))
        except Exception as e:
            pprint(e)

    conn.unbind()


def search_user(user):
    """ Поиск пользователя """
    conn = connect()
    userDN = None
    search_filter = f'(&(objectClass=user)(sAMAccountName={user}))'
    x = conn.search(base, search_filter, attributes=['distinguishedName'])
    if x != False:
        userDN = conn.response[0]['attributes']['distinguishedName']
    conn.unbind()
    print(userDN)


def search_email_user(users):
    """ Поиск почты у списка пользователей """
    conn = connect()
    userDN = []
    for user in users:
        search_filter = f'(&(objectClass=user)(distinguishedName={user}))'
        x = conn.search(base, search_filter, attributes=['mail'])
        if x != False:
            userDN.append(conn.response[0]['attributes']['mail'])

    conn.unbind()
    pprint(userDN)
    pprint(len(userDN))


def search_users_in_group(group):
    """ Поиск участников группы. Выводитх их cn """
    conn = connect()
    userDN = None
    search_filter = f'(&(objectClass=group))'
    x = conn.search(base3, search_filter, attributes=['member'])
    if x != False:
        userDN = conn.response[0]['attributes']['member']
    conn.unbind()
    # pprint(userDN)
    return userDN


def search_os():
    """ Поиск os по AD """
    conn = connect()
    search_filter = f'(&(objectClass=Computer))'
    for kk in ou:
        base1 = f'ou={kk},dc=icore,dc=local'
        conn.search(base1, search_filter, attributes=['operatingSystem'])
        a = 'Всего операционных систем в ou=domain computers', len(
            conn.response)
        for i in conn.response:
            if 'LockedAccounts' in i['dn']:
                continue
            oper_sys.append(i['attributes']['operatingSystem'])
            print(i)
        print('\n\n', a)
        print('Не считая LockedAccounts ', len(oper_sys))
    conn.unbind()
    for i in oper_sys:
        # print(res.keys())
        try:
            if i not in res.keys():
                res[i] = 1  # Добавляем ключ: значение в словарь
            else:
                # Обновляем значение у выбранного ключа
                res[i] = res.get(i) + 1
        except TypeError:
            print('какая-то шибка')

    print('os = ')
    [print(i) for i in res.items()]

    return res


if __name__ == '__main__':
    all = search_ext1_all()
    # pprint(all)
    replace_ip_phone_attribute(all)
    replace_attribute(all)
