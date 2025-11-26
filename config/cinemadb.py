import psycopg2

def criar_conexao():
    try:
        connect = psycopg2.connect(
            dbname = 'cinema',
            user = 'postgres',
            password = 'Bauzudo17',
            host = 'localhost',
            port = '5432'
        )
        print("Conexão realizada com sucesso!")
        return connect
    
    except Exception as error:
        print(f"Erro de Conexão {error}")
