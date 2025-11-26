from config.cinemadb import criar_conexao

def cadastrar_cliente(nome: str, cpf: str, email: str, telefone: str, data_nascimento: str):
    connect = None
    cursor = None

    if not all([nome, cpf, email, telefone, data_nascimento]):
        print("Erro: Todos os campos são obrigatórios!")
        return False
    
    if len(cpf) < 11:
        print("Erro: CPF inválido!")
        return False
        
    if "@" not in email:
        print("Erro: E-mail inválido!")
        return False

    try:
        connect = criar_conexao()
        cursor = connect.cursor()

        cursor.execute("SELECT id_cliente FROM cinema_cliente WHERE email = %s", (email,))
        if cursor.fetchone():
            print(f"Erro: E-mail '{email}' já está cadastrado!")
            return False

        cursor.execute("SELECT id_cliente FROM cinema_cliente WHERE cpf = %s", (cpf,))
        if cursor.fetchone():
            print(f"Erro: CPF '{cpf}' já está cadastrado!")
            return False

        query = """
        INSERT INTO cinema_cliente 
        (nome, cpf, email, telefone, data_nascimento, conta_ativa) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (nome, cpf, email, telefone, data_nascimento, True))
        connect.commit()

        print(f"Cliente '{nome}' cadastrado com sucesso!")
        return True
        
    except Exception as error:
        print(f"Erro ao cadastrar cliente: {error}")
        if connect:
            connect.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()


def visualizar_clientes():
    connect = None
    cursor = None
    try:
        connect = criar_conexao()
        cursor = connect.cursor()

        query = "SELECT * FROM cinema_cliente ORDER BY id_cliente"
        cursor.execute(query)
        clientes = cursor.fetchall()

        if not clientes:
            print("Nenhum cliente cadastrado!")
            return True
        
        print("LISTA DE CLIENTES")
        print(f"{'ID':<4} {'STATUS':<8} {'NOME':<20} {'CPF':<15} {'EMAIL':<25} {'TELEFONE':<12} {'NASCIMENTO':<12}")
        print("-" * 100)
        
        for cliente in clientes:
            id_cliente, nome, cpf, email, telefone, data_nascimento, conta_ativa = cliente
            if conta_ativa == 1:
                conta_ativa = "Ativo"
            elif conta_ativa == 0:
                conta_ativa = "Inativo"
            print(f"{id_cliente:<4} {conta_ativa:<8} {nome:<20} {cpf:<15} {email:<25} {telefone:<12} {data_nascimento} ")
        
        print(f"Total de clientes: {len(clientes)}")
        return True
        
    except Exception as error:
        print(f"Erro ao buscar clientes: {error}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()

def descadastrar_cliente(id_cliente:int):
    connect = None
    cursor = None
    try:
        connect = criar_conexao()
        cursor = connect.cursor()

        cursor.execute("SELECT nome, conta_ativa FROM cinema_cliente WHERE id_cliente = %s", (id_cliente,))
        cliente = cursor.fetchone()
        
        if not cliente:
            print(f"Erro: Cliente com ID {id_cliente} não encontrado!")
            return False

        nome, conta_ativa = cliente
        
        if not conta_ativa:
            print(f"Cliente '{nome}' já está descadastrado!")
            return False

        query = "UPDATE cinema_cliente SET conta_ativa = false WHERE id_cliente = %s"
        cursor.execute(query, (id_cliente,))
        connect.commit()

        print(f"Cliente '{nome}' descadastrado com sucesso!")
        return True

    except Exception as error:
        print(f"Erro ao descadastrar cliente: {error}")
        if connect:
            connect.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()