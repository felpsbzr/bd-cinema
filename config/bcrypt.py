import bcrypt
from config.cinemadb import criar_conexao

def insert_user_adm(nome: str, senha: str):
    connect = None
    cursor = None
    try:
        senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        
        connect = criar_conexao()
        cursor = connect.cursor()
        
        cursor.execute("SELECT nome FROM admin_users WHERE nome = %s", (nome,))
        if cursor.fetchone():
            print("Nome de administrador já existe!")
            return False
        
        senha_str = senha_criptografada.decode('utf-8')
        
        query = "INSERT INTO admin_users (nome, senha) VALUES (%s, %s)"
        cursor.execute(query, (nome, senha_str))
        connect.commit()
        
        print("Administrador registrado com sucesso!")
        return True
        
    except Exception as error:
        print(f"Erro ao registrar administrador: {error}")
        if connect:
            connect.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()

def login(nome: str, senha: str):
    connect = None
    cursor = None
    try:
        connect = criar_conexao()
        cursor = connect.cursor()
        
        cursor.execute("SELECT senha FROM admin_users WHERE nome = %s", (nome,))
        resultado = cursor.fetchone()
        
        if not resultado:
            print("Administrador não encontrado!")
            return False
        
        senha_criptografada = resultado[0].encode('utf-8')
        
        if bcrypt.checkpw(senha.encode('utf-8'), senha_criptografada):
            print(f"Bem-vindo, {nome}!")
            return True
        else:
            print("Senha incorreta!")
            return False
            
    except Exception as error:
        print(f"Erro ao fazer login: {error}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()

def listar_administradores():
    connect = None
    cursor = None
    try:
        connect = criar_conexao()
        cursor = connect.cursor()
        
        cursor.execute("SELECT id_admin, nome, data_criacao FROM admin_users ORDER BY data_criacao")
        admins = cursor.fetchall()
        
        if not admins:
            print("Nenhum administrador cadastrado!")
            return True
        
        print("\nLISTA DE ADMINISTRADORES")
        print(f"{'ID':<4} {'NOME':<20} {'DATA CRIAÇÃO':<20}")
        print("-" * 50)
        
        for admin in admins:
            id_admin, nome, data_criacao = admin
            data_formatada = data_criacao.strftime("%d/%m/%Y %H:%M")
            print(f"{id_admin:<4} {nome:<20} {data_formatada:<20}")
        
        print(f"\nTotal: {len(admins)} administrador(es)")
        return True
        
    except Exception as error:
        print(f"Erro ao listar administradores: {error}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()