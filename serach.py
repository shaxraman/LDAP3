ou = ['Computers', 'domain computers', 'Domain Controllers', 'Domain Servers']
# Frankfurt_Office
#base = 'ou=domain users,dc=icore,dc=local'


def search_os():
    conn = connect()
    oper_sys = []
    search_filter = f'(&(objectClass=Computer))'
    conn.search(base2, search_filter, attributes=['operatingSystem'])
    a = 'Всего операционных систем в ou=domain computers', len(conn.response)
    for i in conn.response:
        #print (i[])
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
