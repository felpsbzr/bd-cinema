from config.cinemadb import criar_conexao

def cadastrar_sala(nome_sala: str, capacidade: int, tipo_sala: str):
    connect = None
    cursor = None
    
    if not all([nome_sala, capacidade, tipo_sala]):
        print("Erro: Todos os campos são obrigatórios!")
        return False
        
    if capacidade <= 0:
        print("Erro: Capacidade deve ser maior que zero!")
        return False
        
    tipos_validos = ["2D", "3D", "IMAX", "VIP"]
    if tipo_sala not in tipos_validos:
        print(f"Erro: Tipo de sala deve ser 2D, 3D, IMAX, ou VIP!")
        return False

    try:
        connect = criar_conexao()
        cursor = connect.cursor()

        query = """
        INSERT INTO cinema_sala 
        (nome_sala, capacidade, tipo_sala) 
        VALUES (%s, %s, %s)
        """
        
        cursor.execute(query, (nome_sala, capacidade, tipo_sala))
        connect.commit()

        print(f"Sala {nome_sala} ({tipo_sala}) cadastrada com sucesso!")
        print(f"Capacidade: {capacidade} lugares")
        return True
        
    except Exception as error:
        print(f"Erro ao cadastrar sala: {error}")
        if connect:
            connect.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()

def visualizar_salas():
    connect = None
    cursor = None
    try:
        connect = criar_conexao()
        cursor = connect.cursor()

        query = "SELECT * FROM cinema_sala ORDER BY nome_sala"
        cursor.execute(query)
        salas = cursor.fetchall()

        if not salas:
            print("Nenhuma sala cadastrada!")
            return True
        
        print("LISTA DE SALAS")
        print(f"{'ID':<4} {'NOME':<8} {'CAPACIDADE':<12} {'TIPO':<10}")
        print("-" * 40)
        
        for sala in salas:
            id_sala, capacidade, nome_sala, tipo_sala = sala
            print(f"{id_sala:<4} {nome_sala:<8} {capacidade:<12} {tipo_sala:<10}")
        
        print(f"Total de salas: {len(salas)}")
        return True
        
    except Exception as error:
        print(f"Erro ao buscar salas: {error}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()

def descadastrar_sala(id_sala: int):
    connect = None
    cursor = None
    
    if id_sala <= 0:
        print("Erro: ID da sala deve ser maior que zero!")
        return False
    
    try:
        connect = criar_conexao()
        cursor = connect.cursor()

        cursor.execute("SELECT nome_sala, tipo_sala FROM cinema_sala WHERE id_sala = %s", (id_sala,))
        sala = cursor.fetchone()
        
        if not sala:
            print(f"Erro: Sala com ID {id_sala} não encontrada!")
            return False

        cursor.execute("SELECT COUNT(*) FROM cinema_sessao WHERE id_sala = %s", (id_sala,))
        sessoes_vinculadas = cursor.fetchone()[0]
        
        if sessoes_vinculadas > 0:
            print(f"Erro: Não é possível descadastrar a sala {sala[0]} ({sala[1]})!")
            print(f"Existem {sessoes_vinculadas} sessões vinculadas a esta sala.")
            return False

        query = "DELETE FROM cinema_sala WHERE id_sala = %s"
        cursor.execute(query, (id_sala,))
        connect.commit()

        print(f"Sala {sala[0]} ({sala[1]}) descadastrada com sucesso!")
        return True
        
    except Exception as error:
        print(f"Erro ao descadastrar sala: {error}")
        if connect:
            connect.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()