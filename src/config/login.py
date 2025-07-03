import getpass

def login():
    user = input("Usuário: ")
    pw = getpass.getpass(prompt='Senha: ')
    dsn = input("Conexao DSN (ex: ip:porta/servico)")

    return user, pw, dsn