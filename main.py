from config.cinemadb import criar_conexao
from functions.menu import menu
from config.bcrypt import insert_user_adm, login

def autenticar():
    while True:
        print("\n=== LOGIN DO SISTEMA ===")
        print("1 - Entrar")
        print("2 - Registrar Administrador")
        print("3 - Sair")
        
        try:
            opcao = int(input("Escolha: "))
            
            if opcao == 1:
                nome = input("Nome: ")
                senha = input("Senha: ")
                if login(nome, senha):
                    return True
                    
            elif opcao == 2:
                nome = input("Novo administrador: ")
                senha = input("Senha: ")
                if insert_user_adm(nome, senha):
                    print("Registrado! Faça login.")
                    
            elif opcao == 3:
                return False
                
            else:
                print("Opção inválida!")
                
        except ValueError:
            print("Digite um número!")

if autenticar():
    while True:
        print("""
            1 - Manipular Clientes
            2 - Manipular Filmes
            3 - Manipular Sessões
            4 - Manipular Salas
            5 - Manipular Ingressos
            6 - Exit
        """)
        try:
            opcao = int(input("Digite uma opção: "))
            
            if opcao == 6:
                print("Saindo do sistema...")
                break
                
            menu(opcao)
            
        except ValueError:
            print("Erro: Digite um número válido!")
        except Exception as error:
            print(f"Erro inesperado: {error}")