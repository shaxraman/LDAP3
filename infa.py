import getpass

serverName = 'icdc0.icore.local'
domainName = 'icore'


# userName = ''
# password = ''

def logging():
    userName = input('Напишите Ваш логин ')
    password = getpass.getpass()
    #userName = 'snezamov'
    #password = ''
    if '@' in userName:
        return userName[:userName.index('@')], password
    elif '.i' in userName:
        return userName[:userName.index('.i')], password
    else:
        return userName, password


base = 'ou=domain users,dc=icore,dc=local'
base2 = 'ou=domain computers,dc=icore,dc=local'
