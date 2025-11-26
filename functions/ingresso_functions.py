from config.cinemadb import criar_conexao

def atribuir_ingresso(tipo_ingresso: str, valor_base: float, forma_pagamento: str, id_sessao: int, id_cliente: int):
    connect = None
    cursor = None
    
    if not all([tipo_ingresso, forma_pagamento, id_sessao, id_cliente]):
        print("Erro: Todos os campos são obrigatórios!")
        return False
        
    if valor_base <= 0:
        print("Erro: Valor base deve ser maior que zero!")
        return False
        
    tipo_ingresso = tipo_ingresso.lower()
    if tipo_ingresso not in ["inteira", "meia"]:
        print("Erro: Tipo de ingresso deve ser 'inteira' ou 'meia'!")
        return False
        
    formas_validas = ["dinheiro", "cartão crédito", "cartão débito", "pix", "cartao credito", "cartao debito"]
    if forma_pagamento.lower() not in [f.lower() for f in formas_validas]:
        print("Erro: Forma de pagamento inválida!")
        return False

    try:
        connect = criar_conexao()
        cursor = connect.cursor()

        cursor.execute("SELECT id_sessao FROM cinema_sessao WHERE id_sessao = %s", (id_sessao,))
        if not cursor.fetchone():
            print(f"Erro: Sessão ID {id_sessao} não encontrada!")
            return False

        cursor.execute("SELECT id_cliente FROM cinema_cliente WHERE id_cliente = %s", (id_cliente,))
        if not cursor.fetchone():
            print(f"Erro: Cliente ID {id_cliente} não encontrado!")
            return False

        cursor.execute("""
            SELECT COUNT(*) FROM cinema_ingresso 
            WHERE id_sessao = %s AND ingresso_ativo = TRUE
        """, (id_sessao,))
        ingressos_vendidos = cursor.fetchone()[0]

        cursor.execute("""
            SELECT sa.capacidade 
            FROM cinema_sessao s 
            JOIN cinema_sala sa ON s.id_sala = sa.id_sala 
            WHERE s.id_sessao = %s
        """, (id_sessao,))
        capacidade = cursor.fetchone()[0]

        if ingressos_vendidos >= capacidade:
            print(f"ERRO: Sala lotada! Capacidade: {capacidade}, Ingressos vendidos: {ingressos_vendidos}")
            return False

        if tipo_ingresso == "meia":
            valor_final = valor_base / 2
        else:
            valor_final = valor_base

        query = """
        INSERT INTO cinema_ingresso 
        (tipo_ingresso, valor, forma_pagamento, id_sessao, id_cliente) 
        VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (tipo_ingresso.title(), valor_final, forma_pagamento, id_sessao, id_cliente))
        connect.commit()

        print(f"Ingresso {tipo_ingresso} cadastrado com sucesso!")
        print(f"Valor base: R$ {valor_base:.2f}")
        print(f"Valor final: R$ {valor_final:.2f}")
        print(f"Forma de pagamento: {forma_pagamento}")
        print(f"Sessão ID: {id_sessao}")
        print(f"Cliente ID: {id_cliente}")
        return True
        
    except Exception as error:
        print(f"Erro ao cadastrar ingresso: {error}")
        if connect:
            connect.rollback()
        return False
        
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()

def cancelar_ingresso(id_ingresso: int, motivo: str):
    connect = None
    cursor = None
    
    if id_ingresso <= 0:
        print("Erro: ID do ingresso deve ser maior que zero!")
        return False
        
    if not motivo:
        print("Erro: Motivo do cancelamento é obrigatório!")
        return False
    
    try:
        connect = criar_conexao()
        cursor = connect.cursor()

        cursor.execute("SELECT * FROM cinema_ingresso WHERE id_ingresso = %s", (id_ingresso,))
        ingresso = cursor.fetchone()
        
        if not ingresso:
            print(f"Erro: Ingresso com ID {id_ingresso} não encontrado!")
            return False

        id_ingresso_original, tipo_ingresso, valor, forma_pagamento, id_sessao, id_cliente = ingresso

        query = """
        INSERT INTO cinema_ingresso_cancelado 
        (id_ingresso_original, tipo_ingresso, valor, forma_pagamento, id_sessao, id_cliente, motivo_cancelamento) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (id_ingresso_original, tipo_ingresso, valor, forma_pagamento, id_sessao, id_cliente, motivo))
        
        query_delete = "DELETE FROM cinema_ingresso WHERE id_ingresso = %s"
        cursor.execute(query_delete, (id_ingresso,))
        
        connect.commit()

        print(f"Ingresso cancelado com sucesso!")
        print(f"Motivo: {motivo}")
        return True
        
    except Exception as error:
        print(f"Erro ao cancelar ingresso: {error}")
        if connect:
            connect.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()

def visualizar_ingressos():
    connect = None
    cursor = None
    try:
        id_cliente = int(input("DIGITE O ID DO CLIENTE: "))
        
        print("TIPOS: 1-Ativos 2-Expirados 3-Cancelados 4-Resumo por Tipo")
        opcao = int(input("ESCOLHA O TIPO: "))
        
        if opcao not in [1, 2, 3, 4]:
            print("Opção inválida!")
            return False

        connect = criar_conexao()
        cursor = connect.cursor()

        if opcao == 1:
            cursor.execute("""
                SELECT i.id_ingresso, i.tipo_ingresso, i.valor, i.forma_pagamento,
                       f.titulo, s.data_hora
                FROM cinema_ingresso i
                JOIN cinema_sessao s ON i.id_sessao = s.id_sessao
                JOIN cinema_filme f ON s.id_filme = f.id_filme
                WHERE i.id_cliente = %s AND i.ingresso_ativo = TRUE
                ORDER BY s.data_hora
            """, (id_cliente,))
            tipo_nome = "ATIVOS"
            
        elif opcao == 2:
            cursor.execute("""
                SELECT i.id_ingresso, i.tipo_ingresso, i.valor, i.forma_pagamento,
                       f.titulo, s.data_hora
                FROM cinema_ingresso i
                JOIN cinema_sessao s ON i.id_sessao = s.id_sessao
                JOIN cinema_filme f ON s.id_filme = f.id_filme
                WHERE i.id_cliente = %s AND i.ingresso_ativo = FALSE
                ORDER BY s.data_hora DESC
            """, (id_cliente,))
            tipo_nome = "EXPIRADOS"
            
        elif opcao == 3:
            cursor.execute("""
                SELECT ic.id_ingresso_original, ic.tipo_ingresso, ic.valor, 
                       f.titulo, s.data_hora, ic.motivo_cancelamento
                FROM cinema_ingresso_cancelado ic
                JOIN cinema_sessao s ON ic.id_sessao = s.id_sessao
                JOIN cinema_filme f ON s.id_filme = f.id_filme
                WHERE ic.id_cliente = %s
                ORDER BY ic.data_cancelamento DESC
            """, (id_cliente,))
            tipo_nome = "CANCELADOS"

        elif opcao == 4:
            cursor.execute("""
                SELECT tipo_ingresso, ingresso_ativo, COUNT(*) 
                FROM cinema_ingresso 
                WHERE id_cliente = %s 
                GROUP BY tipo_ingresso, ingresso_ativo
                UNION ALL
                SELECT tipo_ingresso, FALSE as ingresso_ativo, COUNT(*) 
                FROM cinema_ingresso_cancelado 
                WHERE id_cliente = %s 
                GROUP BY tipo_ingresso
                ORDER BY tipo_ingresso, ingresso_ativo
            """, (id_cliente, id_cliente))
            
            resultados = cursor.fetchall()
            
            if not resultados:
                print("Nenhum ingresso encontrado para este cliente!")
                return True
            
            print(f"\nRESUMO DE INGRESSOS - CLIENTE ID: {id_cliente}")
            print(f"{'TIPO':<10} {'STATUS':<12} {'QUANTIDADE':<12}")
            print("-" * 35)
            
            for tipo, ativo, quantidade in resultados:
                if ativo:
                    status = "ATIVO"
                elif tipo in [r[0] for r in resultados if r[1] is not None]:
                    status = "EXPIRADO"
                else:
                    status = "CANCELADO"
                
                print(f"{tipo:<10} {status:<12} {quantidade:<12}")
            
            return True

        ingressos = cursor.fetchall()

        if not ingressos:
            print(f"Nenhum ingresso {tipo_nome.lower()} encontrado!")
            return True
        
        print(f"\nINGRESSOS {tipo_nome} - CLIENTE ID: {id_cliente}")
        
        if opcao == 3:
            print(f"{'ID ORIG.':<8} {'FILME':<20} {'DATA':<12} {'TIPO':<8} {'VALOR':<8} {'MOTIVO':<15}")
            print("-" * 75)
            for ingresso in ingressos:
                print(f"{ingresso[0]:<8} {ingresso[3]:<20} {ingresso[4].strftime('%d/%m/%Y'):<12} {ingresso[1]:<8} R${ingresso[2]:<6.2f} {(ingresso[5][:12] + '...') if len(ingresso[5]) > 15 else ingresso[5]:<15}")
        else:
            print(f"{'ID':<4} {'FILME':<20} {'DATA/HORA':<16} {'TIPO':<8} {'VALOR':<8} {'PAGAMENTO':<12}")
            print("-" * 75)
            for ingresso in ingressos:
                print(f"{ingresso[0]:<4} {ingresso[4]:<20} {ingresso[5].strftime('%d/%m/%Y %H:%M'):<16} {ingresso[1]:<8} R${ingresso[2]:.2f} {ingresso[3]:<12}")

        print(f"\nTotal: {len(ingressos)} ingresso(s)")
        return True
        
    except ValueError:
        print("Erro: ID deve ser um número!")
        return False
    except Exception as error:
        print(f"Erro: {error}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()