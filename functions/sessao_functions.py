from config.cinemadb import criar_conexao
from datetime import datetime, timezone, timedelta

def cadastrar_sessao(ano: int, mes: int, dia: int, hora: int, minuto: int, idioma: str, tipo_exibicao: str, id_filme: int, id_sala: int):
    connect = None
    cursor = None
    
    campos = [ano, mes, dia, hora, minuto, idioma, tipo_exibicao, id_filme, id_sala]
    if any(campo is None for campo in campos):
        print("Erro: Todos os campos são obrigatórios!")
        return False
    
    try:
        from datetime import datetime
        data_hora = datetime(ano, mes, dia, hora, minuto, 0)
        
        connect = criar_conexao()
        cursor = connect.cursor()

        cursor.execute("SELECT capacidade FROM cinema_sala WHERE id_sala = %s", (id_sala,))
        sala = cursor.fetchone()
        
        if not sala:
            print(f"Erro: Sala ID {id_sala} não encontrada!")
            return False
            
        if sala[0] <= 0:
            print(f"Erro: Sala tem capacidade zero!")
            return False

        cursor.execute("SELECT id_filme FROM cinema_filme WHERE id_filme = %s", (id_filme,))
        if not cursor.fetchone():
            print(f"Erro: Filme ID {id_filme} não encontrado!")
            return False

        query = """
        INSERT INTO cinema_sessao 
        (data_hora, idioma, tipo_exibicao, id_filme, id_sala) 
        VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (data_hora, idioma, tipo_exibicao, id_filme, id_sala))
        connect.commit()

        print(f"Sessão cadastrada com sucesso!")
        print(f"Data/Hora: {data_hora.strftime('%d/%m/%Y %H:%M')}")
        print(f"Idioma: {idioma}")
        print(f"Tipo: {tipo_exibicao}")
        return True
        
    except Exception as error:
        print(f"Erro ao cadastrar sessão: {error}")
        if connect:
            connect.rollback()
        return False
        
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()
            
def visualizar_sessoes():
    connect = None
    cursor = None
    try:
        connect = criar_conexao()
        cursor = connect.cursor()

        query = """
        SELECT s.id_sessao, s.data_hora, s.idioma, s.tipo_exibicao, f.titulo, sa.nome_sala
        FROM cinema_sessao s
        JOIN cinema_filme f ON s.id_filme = f.id_filme
        JOIN cinema_sala sa ON s.id_sala = sa.id_sala
        ORDER BY s.data_hora
        """
        cursor.execute(query)
        sessoes = cursor.fetchall()

        if not sessoes:
            print("Nenhuma sessão cadastrada!")
            return True
        
        brasilia_tz = timezone(timedelta(hours=-3))
        
        print("LISTA DE SESSÕES")
        print(f"{'ID':<4} {'DATA/HORA':<20} {'IDIOMA':<15} {'TIPO':<10} {'FILME':<25} {'SALA':<10}")
        print("-" * 90)
        
        for sessao in sessoes:
            id_sessao, data_hora, idioma, tipo_exibicao, titulo_filme, nome_sala = sessao
            data_hora_brasilia = data_hora.astimezone(brasilia_tz)
            data_formatada = data_hora_brasilia.strftime("%d/%m/%Y %H:%M")
            
            print(f"{id_sessao:<4} {data_formatada:<20} {idioma:<15} {tipo_exibicao:<10} {titulo_filme:<25} {nome_sala:<10}")
        
        print(f"Total de sessões: {len(sessoes)}")
        return True
        
    except Exception as error:
        print(f"Erro ao buscar sessões: {error}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()

def cancelar_sessao(id_sessao: int, motivo: str):
    connect = None
    cursor = None
    
    if id_sessao <= 0:
        print("Erro: ID da sessão deve ser maior que zero!")
        return False
        
    if not motivo:
        print("Erro: Motivo do cancelamento é obrigatório!")
        return False
    
    try:
        connect = criar_conexao()
        cursor = connect.cursor()

        cursor.execute("""
            SELECT s.id_sessao, s.data_hora, f.titulo, sa.nome_sala
            FROM cinema_sessao s
            JOIN cinema_filme f ON s.id_filme = f.id_filme
            JOIN cinema_sala sa ON s.id_sala = sa.id_sala
            WHERE s.id_sessao = %s
        """, (id_sessao,))
        sessao = cursor.fetchone()
        
        if not sessao:
            print(f"Erro: Sessão com ID {id_sessao} não encontrada!")
            return False

        id_sessao, data_hora, titulo_filme, nome_sala = sessao

        cursor.execute("""
            SELECT COUNT(*) FROM cinema_ingresso 
            WHERE id_sessao = %s AND ingresso_ativo = TRUE
        """, (id_sessao,))
        ingressos_ativos = cursor.fetchone()[0]

        if ingressos_ativos > 0:
            cursor.execute("""
                INSERT INTO cinema_ingresso_cancelado 
                (id_ingresso_original, tipo_ingresso, valor, forma_pagamento, id_sessao, id_cliente, motivo_cancelamento)
                SELECT id_ingresso, tipo_ingresso, valor, forma_pagamento, id_sessao, id_cliente, %s
                FROM cinema_ingresso 
                WHERE id_sessao = %s AND ingresso_ativo = TRUE
            """, (f"Sessão cancelada: {motivo}", id_sessao))

        cursor.execute("DELETE FROM cinema_ingresso WHERE id_sessao = %s AND ingresso_ativo = TRUE", (id_sessao,))

        cursor.execute("DELETE FROM cinema_sessao WHERE id_sessao = %s", (id_sessao,))
        
        connect.commit()

        print(f"Sessão cancelada com sucesso!")
        print(f"ID da sessão: {id_sessao}")
        print(f"Filme: {titulo_filme}")
        print(f"Sala: {nome_sala}")
        print(f"Data/Hora: {data_hora.strftime('%d/%m/%Y %H:%M')}")
        print(f"Motivo: {motivo}")
        if ingressos_ativos > 0:
            print(f"{ingressos_ativos} ingresso(s) cancelado(s) automaticamente")
        else:
            print("ℹNenhum ingresso ativo para esta sessão")
        
        return True
        
    except Exception as error:
        print(f"Erro ao cancelar sessão: {error}")
        if connect:
            connect.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()