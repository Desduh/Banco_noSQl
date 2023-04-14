import json
from datetime import datetime
import pymongo
cliente = pymongo.MongoClient("mongodb+srv://betina:7IySyQ3Vf6gDPv8L@bety.dhgqumi.mongodb.net/?retryWrites=true&w=majority")
db = cliente.test
global mydb
mydb = cliente.mercadolivre

def find_clientes():
    global mydb
    mycol = mydb.usuarios
    return mycol.find()

def find_produtos():
    global mydb
    mycol = mydb.produtos
    return mycol.find()

def pega_clientes():
    verificador()
    clientes = find_clientes()
    print("Lista de clientes: ")
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

def selectUsuario(nome):
    clientex = find_clientes()
    for cliente in clientex:
        if cliente.get("nome") == nome:
            return cliente
    print("Cliente não existe!")
    clientes()

def update_usuario(email,novo):
    global mydb
    mycol = mydb.usuarios
    mycol.update_one({"email": email}, {"$set": novo})

def update_usuario_favoritos(email,favoritos):
    global mydb
    mycol = mydb.usuarios
    mycol.update_one({"email": email}, {"$set": {"favoritos": favoritos}})

def pega_produtos():
    produtos = find_produtos()
    for produto in produtos:
        print("Nome: " + produto.get("nome"))
        print("Preço: " + produto.get("preco"))
        print("Quantia disponível: " + produto.get("quantia"))
        print("")

import redis
conR = redis.Redis(host='redis-10282.c15.us-east-1-2.ec2.cloud.redislabs.com',port=10282,password='6RCxUTS4iOA4fGV4jpSogwPwR1RflNxQ')

import json
from bson import ObjectId, Decimal128

def json_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, Decimal128):
        return str(obj.to_decimal())
    else:
        return json.JSONEncoder().default(obj)

def devolver_mongo():
    verificador()
    global chaves_alteracoes
    if chaves_alteracoes != '':
        for chave in chaves_alteracoes:
            if "s" == str(input(f"Você aceita salvar definitivamente a chave {chave}? (s/n) ")):
                ObjDevolver = json.loads(conR.get(chave))
                separacao = chave.split(":")
                if separacao[1] == "usuario":
                    update_usuario(separacao[0],ObjDevolver)
                elif separacao[1] == "favoritos":
                    produtosNome = ObjDevolver
                    produtoAdc = []
                    produtos = find_produtos()
                    for produto in produtos:
                        for produtoNome in produtosNome:
                            if (produto.get("nome") == produtoNome):
                                produtoAdc.append(produto)
                    update_usuario_favoritos(separacao[0],produtoAdc)
        print("Salvo com sucesso!")
    else:
        print("Salve algo no redis antes!")
    chaves_alteracoes = ''
    print("")
    opcoes_usuario()

def salvar_redis(emailI, valores, tipo):
    StringObjeto = json.dumps(valores,  default=json_serializer)
    conR.set(f'{emailI}:{tipo}', StringObjeto, ex=60)
    global chaves_alteracoes
    chaves_alteracoes = []
    chaves_alteracoes.append(f'{emailI}:{tipo}')
    print("Salvo no redis!")
    print("")
    opcoes_usuario()

def atualizar_cliente():
    global chaves_alteracoes
    verificador()
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
    salvar_redis(emailI, novosValores, "usuario")

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
        chave = (input("Deseja adicionar outro produto? (s/n): ") == 's')
    salvar_redis(email, produtosNome, "favoritos")


def opcoes_usuario():
    verificador()
    print("Qual opção deseja?")
    print("01 - Visualizar dados dos usuários")
    print("02 - Atualizar dados de usuário")
    print("03 - Adicionar Favoritos à um usuário")
    print("04 - Sincronizar dados com o MongoDB")
    print("00 - Sair")
    print("")
    opcao = int(input("Opção: "))
    print("")

    if(opcao == 0): 
        print("Beijos :)")

    elif(opcao == 1):
        pega_clientes()
        opcoes_usuario()
    
    elif(opcao == 2):
        atualizar_cliente()
        opcoes_usuario()

    elif(opcao == 3):
        cadastrar_favoritos()

    elif(opcao == 4):
        devolver_mongo()
        opcoes_usuario()

def login():
    print("Login:")
    global email
    email = str(input("Email: "))
    senha = str(input("Senha: "))
    data_e_hora_atuais = datetime.now()
    data = data_e_hora_atuais.strftime('%d-%m-%Y %H:%M')
    conR.set(f'{email}:sessao', f"senha:{senha}")
    conR.expire(f'{email}:sessao', '120')
    print('')
    global logado
    logado = True 

def verificador():
    global email
    if conR.exists(f'{email}:sessao') == 1 : return True 
    else: 
        print('')
        print('##################')
        print('Sua sessão expirou :(')
        print('')
        login()
        return opcoes_usuario()

def voltar_opcoes():
    print("Escolha uma opção")
    print("01 - Voltar  ao menu")
    print("02 - Sair")
    opcao = int(input("Opção: "))
    print("")
    if(opcao == 1):
        opcoes_usuario()

login()
opcoes_usuario()