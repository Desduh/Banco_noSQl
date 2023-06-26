from neo4j import GraphDatabase

# Conexão com o banco de dados Neo4j
uri = "neo4j+s://5e717879.databases.neo4j.io"
username = "neo4j"
password = "VA8rWocb35AN47e4PQ-CXTFPNHj0Cik6KspocRomrkI"

driver = GraphDatabase.driver(uri, auth=(username, password))

def insert_usuario(nome, sobrenome, email, endereco):
    with driver.session() as session:
        session.run(
            "CREATE (u:Usuario {nome: $nome, sobrenome: $sobrenome, email: $email})"
            "FOREACH (e IN $endereco | CREATE (u)-[:TEM_ENDERECO]->(:Endereco {cep: e.cep, numero: e.numero}))",
            nome=nome, sobrenome=sobrenome, email=email, endereco=endereco
        )

def insert_vendedor(nome, sobrenome, email):
    with driver.session() as session:
        session.run(
            "CREATE (v:Vendedor {nome: $nome, sobrenome: $sobrenome, email: $email})",
            nome=nome, sobrenome=sobrenome, email=email
        )

def insert_produtos(nome, quantia, preco):
    with driver.session() as session:
        session.run(
            "CREATE (p:Produto {nome: $nome, quantia: $quantia, preco: $preco})",
            nome=nome, quantia=quantia, preco=preco
        )

def insert_compra(email_usuario, produtos):
    with driver.session() as session:
        session.run(
            "MATCH (u:Usuario {email: $email_usuario}) "
            "UNWIND $produtos AS produto "
            "MATCH (p:Produto) WHERE ID(p) = produto "
            "CREATE (u)-[:REALIZOU_COMPRA]->(c:Compra)-[:CONTEM_PRODUTO]->(p)",
            email_usuario=email_usuario, produtos=produtos
        )

def insert_produto(email_vendedor, produtos):
    with driver.session() as session:
        session.run(
            "MATCH (v:Vendedor {email: $email_vendedor}) "
            "UNWIND $produtos AS produto "
            "MATCH (p:Produto) WHERE ID(p) = produto "
            "CREATE (v)-[:RESPONSAVEL]->(r:Responsavel)-[:CONTEM_PRODUTO]->(p)",
            email_vendedor=email_vendedor, produtos=produtos
        )

def find_clientes():
    with driver.session() as session:
        result = session.run(
            "MATCH (u:Usuario) RETURN u.nome AS nome, u.sobrenome AS sobrenome, u.email AS email"
        )
        return result.data()

def find_vendedores():
    with driver.session() as session:
        result = session.run(
            "MATCH (v:Vendedor)-[:RESPONSAVEL]->(r:Responsavel)-[:CONTEM_PRODUTO]->(p:Produto) "
            "RETURN v.nome AS nome, v.sobrenome AS sobrenome, v.email AS email, COLLECT(p) AS produtos"
        )
        return result.data()

def find_produtos():
    with driver.session() as session:
        result = session.run(
            "MATCH (p:Produto) RETURN ID(p) AS id, p.nome AS nome, p.quantia AS quantia, p.preco AS preco"
        )
        return result.data()

def find_compras():
    with driver.session() as session:
        result = session.run(
            "MATCH (u:Usuario)-[:REALIZOU_COMPRA]->(c:Compra)-[:CONTEM_PRODUTO]->(p:Produto) "
            "RETURN u.email AS email_usuario, COLLECT(p) AS produtos"
        )
        return result.data()

def update_usuario(email, novo):
    with driver.session() as session:
        session.run(
            "MATCH (u:Usuario {email: $email})"
            "SET u += $novo",
            email=email, novo=novo
        )

def update_vendedor(email, novo):
    with driver.session() as session:
        session.run(
            "MATCH (v:Vendedor {email: $email})"
            "SET v += $novo",
            email=email, novo=novo
        )

def update_produto(nome, novo):
    with driver.session() as session:
        session.run(
            "MATCH (p:Produto {nome: $nome})"
            "SET p += $novo",
            nome=nome, novo=novo
        )

def recebe_cadastro_usuario():
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    email = input("Email: ")
    print("Endereços")
    enderecos = []
    adicao = True
    while adicao:
        cep = input("CEP: ")
        numero = input("Número: ")
        enderecos.append({"cep": cep,"numero": numero})
        adicao = (input("Deseja adicionar outro endereço? (s/n): ") == 's')
    insert_usuario(nome, sobrenome, email, enderecos)
    tudo_ok()
    voltar_opcoes()

def recebe_cadastro_vendedor():
    produtosid = find_produtos()
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    email = input("Email: ")
    insert_vendedor(nome, sobrenome, email)
    print("Produtos:")
    print()
    pega_produtos()
    produtos = []
    adicao = True
    while adicao:
        nome_produto = input("Adicionar produto: ")
        chave = True
        for prod in produtosid:
            if(prod.get("nome") == nome_produto):
                produtos.append(prod.get("id"))
                chave = False
        if(chave):
            print("Nome informado não existe")
        adicao = (input("Deseja adicionar outro produto? (s/n): ") == 's')
    insert_produto(email, produtos)
    tudo_ok()
    voltar_opcoes()

def recebe_cadastro_produto():
    nome = input("Nome: ")
    quantia = input("Quantia: ")
    preco = input("Preço: ")
    insert_produtos(nome, quantia, preco)
    tudo_ok()
    voltar_opcoes()

def cadastrar_compras():
    produtosid = find_produtos()
    email = input("Email do usuário: ")
    print("Produtos:")
    print()
    pega_produtos()
    produtos = []
    adicao = True
    while adicao:
        nome_produto = input("Adicionar produto: ")
        chave = True
        for prod in produtosid:
            if prod.get("nome") == nome_produto:
                produtos.append(prod.get("id"))
                chave = False
        if chave:
            print("Nome informado não existe")
        adicao = (input("Deseja adicionar outro produto? (s/n): ") == 's')
    insert_compra(email, produtos)
    tudo_ok()
    voltar_opcoes()

def adicionarProduto():
    produtosid = find_produtos()
    email = input("Email do vendedor: ")
    print("Produtos:")
    print()
    pega_produtos()
    produtos = []
    adicao = True
    while adicao:
        nome_produto = input("Adicionar produto: ")
        chave = True
        for prod in produtosid:
            if prod.get("nome") == nome_produto:
                produtos.append(prod.get("id"))
                chave = False
        if chave:
            print("Nome informado não existe")
        adicao = (input("Deseja adicionar outro produto? (s/n): ") == 's')
    insert_produto(email, produtos)
    tudo_ok()
    voltar_opcoes()

def atualizar_usuario():
    email = input("Email do usuário: ")
    print("Novos dados")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    update_usuario(email, {"nome": nome, "sobrenome": sobrenome})
    tudo_ok()
    voltar_opcoes()

def atualizar_vendedor():
    email = input("Email do vendedor: ")
    print("Novos dados")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    update_vendedor(email, {"nome": nome, "sobrenome": sobrenome})
    tudo_ok()
    voltar_opcoes()

def atualizar_produto():
    nome = input("Nome do produto: ")
    print("Novos dados")
    quantia = input("Quantia: ")
    preco = input("Preço: ")
    update_produto(nome, {"quantia": quantia, "preco": preco})
    tudo_ok()
    voltar_opcoes()

def pega_clientes():
    clientes = find_clientes()
    for cliente in clientes:
        print("Nome: " + cliente.get("nome"))
        print("Sobrenome: " + cliente.get("sobrenome"))
        print("Email: " + cliente.get("email"))
        posicao = 1
        if cliente.get("enderecos") != None:
            print("Endereços: ")
            enderecos = cliente.get("enderecos")
            for endereco in enderecos:
                cep = endereco.get("cep")
                numero = endereco.get("numero")
                print(f"0{posicao} - CEP: {cep}, Número: {numero}")
                posicao += 1
        posicao = 1
        if cliente.get("favoritos") != None:
            print("Favoritos: ")
            favoritos = cliente.get("favoritos")
            for favorito in favoritos:
                nome = favorito.get("nome")
                valor = favorito.get("valor")
                print(f"0{posicao} - Nome do produto: {nome}, Valor: {valor}")
                posicao += 1
                posicao = 1
        if cliente.get("compras") != None:
            print("Compras: ")
            produtos = cliente.get("compras")
            for produto in produtos:
                nome = produto.get("nome")
                preco = produto.get("preco")
                quantia = produto.get("quantia")
                print(f"0{posicao} - Produto: {nome}, Preço: {preco}, Quantia: {quantia}")
                posicao += 1
        print("")
    tudo_ok()
    voltar_opcoes()

def pega_vendedores():
    vendedores = find_vendedores()
    for vendedor in vendedores:
        print("Nome: " + vendedor.get("nome"))
        print("Sobrenome: " + vendedor.get("sobrenome"))
        print("Email: " + vendedor.get("email"))
        posicao = 1
        if vendedor.get("produtos") != None:
            print("Produtos: ")
            produtos = vendedor.get("produtos")
            for produto in produtos:
                print("")
                print("Nome: " + produto.get("nome"))
                print("Quantia: " + produto.get("quantia"))
                print("Preço: " + produto.get("preco"))
                posicao += 1
        print("")
    tudo_ok()
    voltar_opcoes()

def pega_produtos():
    produtos = find_produtos()
    # print(produtos)
    for produto in produtos:
        print("Nome: " + produto.get("nome"))
        print("Quantia: " + produto.get("quantia"))
        print("Preço: " + produto.get("preco"))
        print("")

def pega_compras():
    compras = find_compras()
    for compra in compras:
        print("Email: " + compra.get("email"))
        posicao = 1
        if compra.get("produtos") != None:
            print("Produtos: ")
            print(" ")
            produtos = compra.get("produtos")
            produtosAll = find_produtos()
            for produto in produtos:
                for produtoAll in produtosAll:
                    if(produto == produtoAll.get("id")):
                        print("Nome: " + produtoAll.get("nome"))
                        print("Quantia: " + produtoAll.get("quantia"))
                        print("Preço: " + produtoAll.get("preco"))
                        print("")
                posicao += 1
        print("")
    tudo_ok()
    voltar_opcoes()

def tudo_ok():
    print("Operação concluída com sucesso!\n")

def voltar_opcoes():
    opcoes()


def opcoes():
    print("Olá, qual opção gostaria?")
    print("01 - Usuário")
    print("02 - Vendedor")
    print("03 - Produtos")
    print("04 - Compras")

    opcao = int(input("Opção: "))
    print("")

    if(opcao == 1):
        opcoes_usuario()

    elif(opcao == 2):
        opcoes_vendedor()

    elif(opcao == 3):
        opcoes_produtos()

    elif(opcao == 4):
        opcoes_compras()

    else:
        print("A opção escolhida não existe!")
        print("-----------------------------")
        opcoes()

def opcoes_usuario():
    print("Qual opção deseja?")
    print("01 - Cadastrar")
    print("02 - Visualizar dados")
    print("03 - Atualizar dados")
    print("05 - Adicionar compras")
    print("00 - Voltar")
    print("")
    opcao = int(input("Opção: "))
    print("")

    if(opcao == 0): 
        opcoes()

    elif(opcao == 1):
        recebe_cadastro_usuario()
    
    elif(opcao == 2):
        pega_clientes()

    elif(opcao == 3):
        atualizar_usuario()

    elif(opcao == 5):
        cadastrar_compras()

def opcoes_vendedor():
    print("Qual opção deseja?")
    print("01 - Cadastrar")
    print("02 - Visualizar dados")
    print("03 - Atualizar dados")
    print("04 - Adicionar produto")
    print("00 - Voltar")
    print("")
    opcao = int(input("Opção: "))
    print("")

    if(opcao == 0): 
        opcoes()

    elif(opcao == 1):
        recebe_cadastro_vendedor()

    elif(opcao == 2):
        pega_vendedores()

    elif(opcao == 3):
        atualizar_vendedor()

    elif(opcao == 4):
        adicionarProduto()


def opcoes_produtos():
    print("Qual opção deseja?")
    print("01 - Cadastrar")
    print("02 - Visualizar dados")
    print("03 - Atualizar dados")
    print("00 - Voltar")
    print("")
    opcao = int(input("Opção: "))
    print("")

    if(opcao == 0): 
        opcoes()

    elif(opcao == 1):
        recebe_cadastro_produto()

    elif(opcao == 2):
        pega_produtos()  
        tudo_ok()
        voltar_opcoes()

    elif(opcao == 3):
        atualizar_produto()

def opcoes_compras():
    print("Qual opção deseja?")
    print("01 - Visualizar dados")
    print("02 - Realizar Compras")
    print("00 - Voltar")
    print("")
    opcao = int(input("Opção: "))
    print("")

    if opcao == 0: 
        opcoes()
    elif opcao == 1:
        pega_compras()
        tudo_ok()
        voltar_opcoes()
    elif opcao == 2:
        cadastrar_compras()

def tudo_ok():
    print("Sua operação foi realizada!")
    print("---------------------------")
    print("")

def voltar_opcoes():
    print("Escolha uma opção")
    print("01 - Voltar  ao menu")
    print("02 - Sair")
    opcao = int(input("Opção: "))
    print("")
    if(opcao == 1):
        opcoes()

opcoes()