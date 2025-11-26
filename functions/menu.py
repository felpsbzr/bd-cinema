from .cliente_functions import cadastrar_cliente, visualizar_clientes, descadastrar_cliente
from .filme_functions import visualizar_filmes, cadastrar_filme, descadastrar_filme
from .sala_functions import visualizar_salas, cadastrar_sala, descadastrar_sala
from .sessao_functions import visualizar_sessoes, cadastrar_sessao, cancelar_sessao
from .ingresso_functions import visualizar_ingressos, atribuir_ingresso, cancelar_ingresso
from datetime import datetime

# OPCAO 1 - CLIENTES
# OPCAO 2 - FILMES
# OPCAO 3 - SESSOES
# OPCAO 4 - SALAS
# OPCAO 5 - INGRESSOS
# OPCAO 6 - EXIT

def menu(opcao):
    while True:
        
        if opcao == 6:
            break

        elif opcao == 1:
            while True:
                print("""
                  1 - Visualizar Clientes
                  2 - Cadastrar Cliente
                  3 - Descadastrar Cliente
                  4 - Retornar ao Menu
                  
                  """)
                try:
                    opcao_cliente = int(input(""))
                    break
                except ValueError:
                    print("ERRO: Digite apenas números para as opções!")

            if opcao_cliente == 1:
                visualizar_clientes()

            elif opcao_cliente == 2:
                while True:
                    nome = input("DIGITE SEU NOME: ")
                    if nome:
                        break
                    print("ERRO: Nome é obrigatório!")
                    
                while True:
                    cpf = input("DIGITE SEU CPF: ")
                    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    
                    if cpf_limpo and len(cpf_limpo) == 11:
                        cpf = cpf_limpo  # Usa o CPF limpo (apenas números)
                        break
                    print("ERRO: CPF deve ter 11 dígitos numéricos!")
                    
                while True:
                    email = input("DIGITE SEU EMAIL: ")
                    if email and "@" in email:
                        break
                    print("ERRO: E-mail inválido!")
                    
                while True:
                    telefone = input("DIGITE OS NUMEROS DO SEU TELEFONE: ")
    
                    telefone_limpo = ''.join(filter(str.isdigit, telefone))
    
                    if not telefone_limpo:
                            print("ERRO: Telefone é obrigatório!")
                            continue
        
                    if len(telefone_limpo) not in [10, 11]:
                        print("ERRO: Telefone deve ter 10 ou 11 dígitos (com DDD)!")
                        continue
        
                    break
                
                while True:
                    data_nascimento = input("DIGITE SUA DATA DE NASCIMENTO (AAAA-MM-DD): ")
    
                    try:
                        datetime.strptime(data_nascimento, '%Y-%m-%d')
                        break
                    except ValueError:
                        print("ERRO: Data inválida! Digite no formato AAAA-MM-DD (ex: 1990-05-15)")

                cadastrar_cliente(nome,cpf,email,telefone,data_nascimento)

            elif opcao_cliente == 3:
                while True:
                    try:
                        cliente_id = int(input("DIGITE O ID DO CLIENTE QUE SERÁ DESCADASTRADO: "))
                        descadastrar_cliente(cliente_id)
                        break
                    except ValueError:
                        print("ERRO: ID deve ser um número!")
            
            elif opcao_cliente == 4:
                break

            else:
                print("OPÇÃO INVÁLIDA! TENTE NOVAMENTE.")

        elif opcao == 2:
            while True:
                print("""
                      1 - Visualizar Catálogo de Filmes
                      2 - Cadastrar Filme
                      3 - Descadastrar Filme
                      4 - Retornar ao Menu
                      
                      """)
                try:
                    opcao_filme = int(input(""))
                    break
                except ValueError:
                    print("ERRO: Digite apenas números para as opções!")

            if opcao_filme == 1:
                visualizar_filmes()

            elif opcao_filme == 2:
                while True:
                    titulo = input("DIGITE O TÍTULO DO FILME: ")
                    if titulo:
                        break
                    print("ERRO: Título é obrigatório!")
                    
                while True:
                    genero = input("DIGITE O GÊNERO DO FILME: ")
                    if genero:
                        break
                    print("ERRO: Gênero é obrigatório!")
                    
                while True:
                    try:
                        duracao = int(input("DIGITE A DURAÇÃO EM MINUTOS: "))
                        if duracao > 0:
                            break
                        print("ERRO: Duração deve ser maior que zero!")
                    except ValueError:
                        print("ERRO: Duração deve ser um número!")
                    
                while True:
                    classificacao = input("DIGITE A CLASSIFICAÇÃO INDICATIVA: ")
                    if classificacao:
                        break
                    print("ERRO: Classificação é obrigatória!")
                    
                cadastrar_filme(titulo, genero, duracao, classificacao)

            elif opcao_filme == 3:
                while True:
                    try:
                        filme_id = int(input("DIGITE O ID DO FILME QUE SERÁ DESCADASTRADO: "))
                        descadastrar_filme(filme_id)
                        break
                    except ValueError:
                        print("ERRO: ID deve ser um número!")

            elif opcao_filme == 4:
                break

            else:
                print("OPÇÃO INVÁLIDA! TENTE NOVAMENTE.")
            
        elif opcao == 3:
            while True:
                print("""
                     1 - Visualizar Sessões Ativas
                     2 - Marcar Sessão
                     3 - Cancelar Sessão
                     4 - Retornar ao Menu
                     
                     """)
                try:
                    opcao_sessao = int(input(""))
                    break
                except ValueError:
                    print("ERRO: Digite apenas números para as opções!")

            if opcao_sessao == 1:
                visualizar_sessoes()

            elif opcao_sessao == 2:
                while True:
                    try:
                        ano = int(input("ANO (AAAA): "))
                        ano_atual = datetime.now().year
                        if ano_atual <= ano <= ano_atual + 10:
                            break
                        print(f"ERRO: Ano deve ser entre {ano_atual} e {ano_atual + 10}!")
                    except ValueError:
                        print("ERRO: Ano deve ser um número!")
                
                while True:
                    try:
                        mes = int(input("MES (MM):"))
                        ano_atual = datetime.now().year
                        mes_atual = datetime.now().month

                        if mes < 1 or mes > 12:
                           print("ERRO: Mês deve ser entre 1 e 12!")
                           continue
            
                        if ano == ano_atual and mes < mes_atual:
                            print("ERRO: Mês já passou!")
                            continue
            
                        break
                    except ValueError:
                       print("ERRO: Mês deve ser um número!")

                while True:
                    try:
                        dia = int(input("DIA (DD): "))
                        ano_atual = datetime.now().year
                        mes_atual = datetime.now().month
                        dia_atual = datetime.now().day

                        if dia < 1 or dia > 31:
                            print("ERRO: Dia deve ser entre 1 e 31!")
                            continue
            
                        if ano == ano_atual and mes == mes_atual and dia < dia_atual:
                            print("ERRO: Dia já passou!")
                            continue
                        
                        break

                    except ValueError:
                        print("ERRO: Dia deve ser um número!")

                while True:
                    try:
                        hora = int(input("HORA (HH): "))
                        if 0 <= hora <= 23:
                            break
                        print("ERRO: Hora deve ser entre 0 e 23!")
                    except ValueError:
                        print("ERRO: Hora deve ser um número!")
                    
                while True:
                    try:
                        minuto = int(input("MINUTO (MM): "))
                        if 0 <= minuto <= 59:
                            break
                        print("ERRO: Minuto deve ser entre 0 e 59!")
                    except ValueError:
                        print("ERRO: Minuto deve ser um número!")
                    
                while True:
                    idioma = input("IDIOMA: ")
                    if idioma:
                        break
                    print("ERRO: Idioma é obrigatório!")
                    
                while True:
                    tipo_exibicao = input("TIPO DE EXIBIÇÃO (2D/3D/IMAX/VIP): ")
                    if tipo_exibicao in ["2D", "3D", "IMAX", "VIP"]:
                        break
                    print("ERRO: Tipo deve ser 2D, 3D, IMAX ou VIP!")
                    
                while True:
                    try:
                        id_filme = int(input("ID DO FILME: "))
                        if id_filme > 0:
                            break
                        print("ERRO: ID do filme deve ser maior que zero!")
                    except ValueError:
                        print("ERRO: ID do filme deve ser um número!")
                    
                while True:
                    try:
                        id_sala = int(input("ID DA SALA: "))
                        if id_sala > 0:
                            break
                        print("ERRO: ID da sala deve ser maior que zero!")
                    except ValueError:
                        print("ERRO: ID da sala deve ser um número!")
                    
                cadastrar_sessao(ano, mes, dia, hora, minuto, idioma, tipo_exibicao, id_filme, id_sala)

            elif opcao_sessao == 3:
                while True:
                    try:
                        sessao_id = int(input("DIGITE O ID DA SESSÃO QUE SERÁ CANCELADA: "))
                        if sessao_id > 0:
                            break
                        print("ERRO: ID da sessão deve ser maior que zero!")
                    except ValueError:
                        print("ERRO: ID da sessão deve ser um número!")
                    
                while True:
                    motivo = input("DIGITE O MOTIVO DO CANCELAMENTO: ")
                    if motivo:
                        break
                    print("ERRO: Motivo é obrigatório!")
                    
                cancelar_sessao(sessao_id, motivo)

            elif opcao_sessao == 4:
                break

            else:
                print("OPÇÃO INVÁLIDA! TENTE NOVAMENTE.")

        elif opcao == 4:
            while True:
                print("""
                 1 - Visualizar Salas
                 2 - Cadastrar Sala
                 3 - Descadastrar Sala
                 4 - Retornar ao Menu
                 
                 """)
                try:
                    opcao_sala = int(input(""))
                    break
                except ValueError:
                    print("ERRO: Digite apenas números para as opções!")

            if opcao_sala == 1:
                visualizar_salas()

            elif opcao_sala == 2:
                while True:
                    nome_sala = input("NOME DA SALA: ")
                    if nome_sala:
                        break
                    print("ERRO: Nome da sala é obrigatório!")
                    
                while True:
                    try:
                        capacidade = int(input("CAPACIDADE: "))
                        if capacidade > 0:
                            break
                        print("ERRO: Capacidade deve ser maior que zero!")
                    except ValueError:
                        print("ERRO: Capacidade deve ser um número!")
                    
                while True:
                    tipo_sala = input("TIPO DA SALA (2D/3D/IMAX/VIP): ")
                    if tipo_sala in ["2D", "3D", "IMAX", "VIP"]:
                        break
                    print("ERRO: Tipo deve ser 2D, 3D, IMAX ou VIP!")
                    
                cadastrar_sala(nome_sala, capacidade, tipo_sala)

            elif opcao_sala == 3:
                while True:
                    try:
                        sala_id = int(input("DIGITE O ID DA SALA QUE SERÁ DESCADASTRADA: "))
                        descadastrar_sala(sala_id)
                        break
                    except ValueError:
                        print("ERRO: ID deve ser um número!")

            elif opcao_sala == 4:
                break

            else:
                print("OPÇÃO INVÁLIDA! TENTE NOVAMENTE.")

        elif opcao == 5:
            while True:
                print("""
                 1 - Visualizar Ingressos por Cliente
                 2 - Atribuir Ingresso
                 3 - Cancelar Ingresso
                 4 - Retornar ao Menu
                 
                 """)
                try:
                    opcao_ingresso = int(input(""))
                    break
                except ValueError:
                    print("ERRO: Digite apenas números para as opções!")

            if opcao_ingresso == 1:
                visualizar_ingressos()

            elif opcao_ingresso == 2:
                while True:
                    tipo_ingresso = input("TIPO (inteira/meia): ")
                    if tipo_ingresso in ["inteira", "meia"]:
                        break
                    print("ERRO: Tipo deve ser 'inteira' ou 'meia'!")
                    
                while True:
                    try:
                        valor_base = float(input("VALOR BASE: "))
                        if valor_base > 0:
                            break
                        print("ERRO: Valor deve ser maior que zero!")
                    except ValueError:
                        print("ERRO: Valor deve ser um número!")
                    
                while True:
                    forma_pagamento = input("FORMA DE PAGAMENTO: ")
                    formas_validas = ["dinheiro", "cartão crédito", "cartão débito", "pix"]
                    if forma_pagamento.lower() in [f.lower() for f in formas_validas]:
                        break
                    print("ERRO: Forma de pagamento inválida!")
                    
                while True:
                    try:
                        id_sessao = int(input("ID DA SESSÃO: "))
                        if id_sessao > 0:
                            break
                        print("ERRO: ID da sessão deve ser maior que zero!")
                    except ValueError:
                        print("ERRO: ID da sessão deve ser um número!")
                    
                while True:
                    try:
                        id_cliente = int(input("ID DO CLIENTE: "))
                        if id_cliente > 0:
                            break
                        print("ERRO: ID do cliente deve ser maior que zero!")
                    except ValueError:
                        print("ERRO: ID do cliente deve ser um número!")
                    
                atribuir_ingresso(tipo_ingresso, valor_base, forma_pagamento, id_sessao, id_cliente)

            elif opcao_ingresso == 3:
                while True:
                    try:
                        ingresso_id = int(input("DIGITE O ID DO INGRESSO QUE SERÁ CANCELADO: "))
                        if ingresso_id > 0:
                            break
                        print("ERRO: ID do ingresso deve ser maior que zero!")
                    except ValueError:
                        print("ERRO: ID do ingresso deve ser um número!")
                    
                while True:
                    motivo = input("DIGITE O MOTIVO DO CANCELAMENTO: ")
                    if motivo:
                        break
                    print("ERRO: Motivo é obrigatório!")
                    
                cancelar_ingresso(ingresso_id, motivo)

            elif opcao_ingresso == 4:
                break

            else:
                print("OPÇÃO INVÁLIDA! TENTE NOVAMENTE.")

        else:
            print("OPÇÃO INVÁLIDA! TENTE NOVAMENTE.")
            break

