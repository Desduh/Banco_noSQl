import pymongo

cliente = pymongo.MongoClient("mongodb+srv://betina:7IySyQ3Vf6gDPv8L@bety.dhgqumi.mongodb.net/?retryWrites=true&w=majority")
db = cliente.test
global mydb
mydb = cliente.mercadolivre

# funções de banco
def insert_usuario(nome,sobrenome,email,endereco):
    global mydb
    mycol = mydb.usuarios
    mydict = {"nome": nome, "sobrenome": sobrenome, "email": email, "enderecos": endereco}
    x = mycol.insert_one(mydict)

def insert_vendedor(nome,sobrenome,email):
    global mydb
    mycol = mydb.vendedores
    mydict = {"nome": nome, "sobrenome": sobrenome, "email": email}
    x = mycol.insert_one(mydict)

def insert_produtos(nome,quantia,preco):
    global mydb
    mycol = mydb.produtos
    mydict = {"nome": nome, "quantia": quantia, "preco": preco}
    x = mycol.insert_one(mydict)

def insert_compras(email,produtos):
    global mydb
    mycol = mydb.compras
    mydict = {"email": email, "produtos": produtos}
    x = mycol.insert_one(mydict)

def find_clientes():
    global mydb
    mycol = mydb.usuarios
    return mycol.find()

def find_vendedores():
    global mydb
    mycol = mydb.vendedores
    return mycol.find()

def find_produtos():
    global mydb
    mycol = mydb.produtos
    return mycol.find()

def find_compras():
    global mydb
    mycol = mydb.compras
    return mycol.find()

def delete_usuario(email):
    global mydb
    mycol = mydb.usuarios
    mycol.delete_one({"email": email})
    tudo_ok()
    voltar_opcoes()

def delete_vendedor(email):
    global mydb
    mycol = mydb.vendedores
    mycol.delete_one({"email": email})
    tudo_ok()
    voltar_opcoes()

def delete_produto(nome):
    global mydb
    mycol = mydb.produtos
    mycol.delete_one({"nome": nome})
    tudo_ok()
    voltar_opcoes()

def delete_compra(email):
    global mydb
    mycol = mydb.compras
    mycol.delete_one({"email": email})
    tudo_ok()
    voltar_opcoes()

def update_usuario(email,novo):
    global mydb
    mycol = mydb.usuarios
    mycol.update_one({"email": email}, {"$set": novo})

def update_vendedor(email,novo):
    global mydb
    mycol = mydb.vendedores
    mycol.update_one({"email": email}, {"$set": novo})

def update_produto(nome,novo):
    global mydb
    mycol = mydb.produtos
    mycol.update_one({"nome": nome}, {"$set": novo})

def update_usuario_compras(email,compras):
    global mydb
    mycol = mydb.usuarios
    mycol.update_one({"email": email}, {"$set": {"compras": compras}})

def update_usuario_favoritos(email,favoritos):
    global mydb
    mycol = mydb.usuarios
    mycol.update_one({"email": email}, {"$set": {"favoritos": favoritos}})

#funcoes recebe 
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
    insert_usuario(nome,sobrenome,email,enderecos)
    tudo_ok()
    voltar_opcoes()

def recebe_cadastro_vendedor():
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    email = input("Email: ")
    # print("Produtos")
    # produtos = []
    # adicao = True
    # while adicao:
    #     id = input("ID do produto: ")
    #     produtos.append({"id": id})
    #     adicao = (input("Deseja adicionar outro produto? (s/n): ") == 's')
    insert_vendedor(nome,sobrenome,email)
    tudo_ok()
    voltar_opcoes()

def recebe_cadastro_produto():
    nome = input("Nome: ")
    valor  = input("Valor: ")
    quantia = input("Quantia em estoque: ")
    insert_produtos(nome,quantia,valor)
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
        produtos = vendedor.get("produtos")
        if produtos != None:
            print("Vende esses produtos: ")
            for produto in produtos:
                nome = produto.get("nome")
                print(f"0{posicao} - Nome do produto: {nome}")
                posicao += 1
        print("")
    tudo_ok()
    voltar_opcoes()

def pega_produtos():
    produtos = find_produtos()
    for produto in produtos:
        print("Nome: " + produto.get("nome"))
        print("Preço: " + produto.get("preco"))
        print("Quantia disponível: " + produto.get("quantia"))
        print("")

def pega_compras():
    compras = find_compras()
    for compra in compras:
        print("Email: " + compra.get("email"))
        posicao = 1
        if compra.get("produtos") != None:
            print("Compras: ")
            produtos = compra.get("produtos")
            for produto in produtos:
                nome = produto.get("nome")
                preco = produto.get("preco")
                quantia = produto.get("quantia")
                print(f"0{posicao} - Produto: {nome}, Preço: {preco}, Quantia: {quantia}")
                posicao += 1
        print("")

def atualizar_usuario():
    emailI = input("Email do usuário à atualizar: ")
    print("Quais campos irá atualizar?")
    print("01 - Nome")
    print("02 - Sobrenome")
    print("03 - Email")
    campos = input("Quais os campos? *modelo: 01,02,03: ")
    campos = campos.split(",")
    novosValores = {}
    for campo in campos:
        campo = int(campo)
        if(campo == 1):
            nome = input("Novo nome: ")
            novosValores["nome"] = nome

        elif(campo == 2):
            sobrenome = input("Novo sobrenome: ")
            novosValores["sobrenome"] = sobrenome 

        elif(campo == 3):
            email = input("Novo email: ")
            novosValores["email"] = email
    update_usuario(emailI, novosValores)
    tudo_ok()
    voltar_opcoes()

def atualizar_vendedor():
    emailI = input("Email do vendedor à atualizar: ")
    print("Quais campos irá atualizar?")
    print("01 - Nome")
    print("02 - Sobrenome")
    print("03 - Email")
    campos = input("Quais os campos? *modelo: 01,02,03: ")
    campos = campos.split(",")
    novosValores = {}
    for campo in campos:
        campo = int(campo)
        if(campo == 1):
            nome = input("Novo nome: ")
            novosValores["nome"] = nome

        elif(campo == 2):
            sobrenome = input("Novo sobrenome: ")
            novosValores["sobrenome"] = sobrenome 

        elif(campo == 3):
            email = input("Novo email: ")
            novosValores["email"] = email
    update_vendedor(emailI, novosValores)
    tudo_ok()
    voltar_opcoes()

def atualizar_produto():
    nomeI = input("Nome do produto à atualizar: ")
    print("Quais campos irá atualizar?")
    print("01 - Nome")
    print("02 - Valor")
    print("03 - Quantia")
    campos = input("Quais os campos? *modelo: 01,02,03: ")
    campos = campos.split(",")
    novosValores = {}
    for campo in campos:
        campo = int(campo)
        if(campo == 1):
            nome = input("Novo nome: ")
            novosValores["nome"] = nome

        elif(campo == 2):
            preco = input("Novo preço: ")
            novosValores["preco"] = preco

        elif(campo == 3):
            quantia = input("Nova quantidade: ")
            novosValores["quantia"] = quantia
    update_produto(nomeI, novosValores)
    tudo_ok()
    voltar_opcoes()

def cadastrar_compras():
    email = input("Email do usuário que ira comprar: ")
    print('')
    print("Produtos disponíveis:")
    pega_produtos()
    produtosNome = []
    chave = True
    while chave:
        produtoNome = input("Nome do produto comprado: ")
        produtosNome.append(produtoNome)
        chave = (input("Deseja adicionar outra compra? (s/n): ") == 's')
    produtoAdc = []
    produtos = find_produtos()
    for produto in produtos:
        for produtoNome in produtosNome:
            if (produto.get("nome") == produtoNome):
                produtoAdc.append(produto)
    insert_compras(email, produtoAdc)
    update_usuario_compras(email, produtoAdc)
    tudo_ok()
    voltar_opcoes()

def cadastrar_favoritos():
    email = input("Email do usuário: ")
    print('')
    print("Produtos disponíveis:")
    pega_produtos()
    produtosNome = []
    chave = True
    while chave:
        produtoNome = input("Nome do produto favoritado: ")
        produtosNome.append(produtoNome)
        chave = (input("Deseja adicionar outra compra? (s/n): ") == 's')
    produtoAdc = []
    produtos = find_produtos()
    for produto in produtos:
        for produtoNome in produtosNome:
            if (produto.get("nome") == produtoNome):
                produtoAdc.append(produto)
    update_usuario_favoritos(email, produtoAdc)
    tudo_ok()
    voltar_opcoes()

# Opções

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
    print("04 - Deletar dados")
    print("05 - Adicionar compras")
    print("06 - Adicionar Favoritos")
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

    elif(opcao == 4):
        email = input("Email do usuário: ")
        delete_usuario(email)

    elif(opcao == 5):
        cadastrar_compras()

    elif(opcao == 6):
        cadastrar_favoritos()        

def opcoes_vendedor():
    print("Qual opção deseja?")
    print("01 - Cadastrar")
    print("02 - Visualizar dados")
    print("03 - Atualizar dados")
    print("04 - Deletar dados")
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
        email = input("Email do vendedor: ")
        delete_vendedor(email)

def opcoes_produtos():
    print("Qual opção deseja?")
    print("01 - Cadastrar")
    print("02 - Visualizar dados")
    print("03 - Atualizar dados")
    print("04 - Deletar dados")
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

    elif(opcao == 4):
        nome = input("Nome do produto: ")
        delete_produto(nome)

def opcoes_compras():
    print("Qual opção deseja?")
    print("01 - Visualizar dados")
    print("02 - Deletar dados")
    print("00 - Voltar")
    print("")
    opcao = int(input("Opção: "))
    print("")

    if(opcao == 0): 
        opcoes()

    elif(opcao == 1):
        pega_compras()
        tudo_ok()
        voltar_opcoes()

    elif(opcao == 2):
        email = input("Email do usuário relacionado a compra: ")
        delete_compra(email)

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