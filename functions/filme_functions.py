from config.cinemadb import criar_conexao

def cadastrar_filme(titulo: str, genero: str, duracao_minutos: int, classificacao_indicativa: str):
    connect = None
    cursor = None

    if not all([titulo, genero, classificacao_indicativa]):
        print("Erro: Titulo, gênero e classificação são obrigatórios!")
        return False
        
    if duracao_minutos <= 0:
        print("Erro: Duração deve ser maior que zero!")
        return False
    
    try:
        connect = criar_conexao()
        cursor = connect.cursor()

        query = """
        INSERT INTO cinema_filme 
        (titulo, genero, duracao_minutos, classificacao_indicativa) 
        VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(query, (titulo, genero, duracao_minutos, classificacao_indicativa))
        connect.commit()

        print(f"Filme '{titulo}' cadastrado com sucesso!")
        return True
        
    except Exception as error:
        print(f"Erro ao cadastrar filme: {error}")
        if connect:
            connect.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()

def visualizar_filmes():
    connect = None
    cursor = None
    try:
        connect = criar_conexao()
        cursor = connect.cursor()

        query = "SELECT * FROM cinema_filme ORDER BY id_filme"
        cursor.execute(query)
        filmes = cursor.fetchall()

        if not filmes:
            print("Nenhum filme cadastrado!")
            return True
        
        print("LISTA DE FILMES")
        print(f"{'ID':<4} {'TÍTULO':<25} {'GÊNERO':<15} {'DURAÇÃO':<10} {'CLASSIFICAÇÃO':<15}")
        print("-" * 75)
        
        for filme in filmes:
            id_filme, titulo, genero, duracao_minutos, classificacao_indicativa = filme
            print(f"{id_filme:<4} {titulo:<25} {genero:<15} {duracao_minutos:<10} {classificacao_indicativa:<15}")
        
        print(f"Total de filmes: {len(filmes)}")
        return True
        
    except Exception as error:
        print(f"Erro ao buscar filmes: {error}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()
    
def descadastrar_filme(id_filme: int):
    connect = None
    cursor = None
    
    if id_filme <= 0:
        print("Erro: ID do filme deve ser maior que zero!")
        return False
    
    try:
        connect = criar_conexao()
        cursor = connect.cursor()

        cursor.execute("SELECT titulo FROM cinema_filme WHERE id_filme = %s", (id_filme,))
        filme = cursor.fetchone()
        
        if not filme:
            print(f"Erro: Filme com ID {id_filme} não encontrado!")
            return False

        cursor.execute("SELECT COUNT(*) FROM cinema_sessao WHERE id_filme = %s", (id_filme,))
        sessoes_vinculadas = cursor.fetchone()[0]
        
        if sessoes_vinculadas > 0:
            print(f"Erro: Não é possível descadastrar o filme '{filme[0]}'!")
            print(f"Existem {sessoes_vinculadas} sessões vinculadas a este filme.")
            return False

        query = "DELETE FROM cinema_filme WHERE id_filme = %s"
        cursor.execute(query, (id_filme,))
        connect.commit()

        print(f"Filme '{filme[0]}' descadastrado com sucesso!")
        return True
        
    except Exception as error:
        print(f"Erro ao descadastrar filme: {error}")
        if connect:
            connect.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()