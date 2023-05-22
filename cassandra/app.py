from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.util import uuid

cloud_config= {
  'secure_connect_bundle': 'secure-connect-bety.zip'
}
auth_provider = PlainTextAuthProvider("jxbiZCoHJMGchSaeNztzfbTn", "6y9NvWWsP4jDRFCWZZ72XU8cBrFuY5-qgLzNZQfW3rYwchFtT4G-Arlxni23Sy8DXIrOnhksAeMWzjS4KovDq_BZiuKq_Mc2z-TsT+wL,BdqFB15gdc,kyJWAz_.KfZ6")
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect("mercado_livre")



def insert_usuario(session, sobrenome, email, nome, endereco):
    id = uuid.uuid4()
    session.execute("INSERT INTO usuarios (id, sobrenome, email, nome, endereco) VALUES (%s,%s,%s,%s,%s)", [id, sobrenome, email, nome, endereco])

def insert_vendedor(session, nome,sobrenome,email):
  id = uuid.uuid4()
  session.execute("INSERT INTO vendedores (id, sobrenome, email, nome) VALUES (%s,%s,%s,%s)", [id, sobrenome, email, nome])

def insert_produtos(session,nome,quantia,preco):
  id = uuid.uuid4()
  session.execute("INSERT INTO produtos (id, preco, quantia, nome) VALUES (%s,%s,%s,%s)", [id, preco, quantia, nome])

def insert_compras(session,email,produto):
  id = uuid.uuid4()
  session.execute("INSERT INTO compras (id, email, produto) VALUES (%s,%s,%s)", [id, email,produto])



def find_clientes():
  result = session.execute("SELECT * FROM usuarios")
  return result

def find_vendedores():
  result = session.execute("SELECT * FROM vendedores")
  return result

def find_produtos():
  result = session.execute("SELECT * FROM produtos")
  return result

def find_compras():
  result = session.execute("SELECT * FROM compras;")
  return result

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
    insert_usuario(session, sobrenome, email, nome, enderecos)
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
    insert_vendedor(session, sobrenome, email, nome)
    tudo_ok()
    voltar_opcoes()

def recebe_cadastro_produto():
    nome = input("Nome: ")
    valor  = input("Valor: ")
    quantia = input("Quantia em estoque: ")
    insert_produtos(session,nome,quantia,valor)
    tudo_ok()
    voltar_opcoes()

def pega_clientes():
    clientes = find_clientes()
    for cliente in clientes:
        print("Nome: " + cliente.nome)
        print("Sobrenome: " + cliente.sobrenome)
        print("Email: " + cliente.email)
        posicao = 1
        if cliente.endereco is not None:
            print("Endereços: ")
            for endereco in cliente.endereco:
                cep = endereco["cep"]
                numero = endereco["numero"]
                print(f"0{posicao} - CEP: {cep}, Número: {numero}")
                posicao += 1
        print("")
    tudo_ok()
    voltar_opcoes()

def pega_vendedores():
    vendedores = find_vendedores()
    for vendedor in vendedores:
        print("Nome: " + str(vendedor.nome))
        print("Sobrenome: " + str(vendedor.sobrenome))
        print("Email: " + str(vendedor.email))
        posicao = 1
        produtos = vendedor.produtos
        if produtos is not None:
            print("Vende esses produtos: ")
            for produto in produtos:
                nome = produto.get("nome", "")
                print(f"0{posicao} - Nome do produto: {nome}")
                posicao += 1
        print("")
    tudo_ok()
    voltar_opcoes()

def pega_produtos():
    produtos = find_produtos()
    for produto in produtos:
        print("Nome: " + produto.nome)
        print("Preço: " + produto.preco)
        print("Quantia disponível: " + produto.quantia)
        print("")

def pega_compras():
    clientes = find_clientes()
    produtos = find_produtos()
    for cliente in clientes:
        print(f'Cliente: {cliente.nome}')
        compras = find_compras()
        for compra in compras:
          if(compra.email == cliente.email):
            for produto in produtos:
                if compra.produto == produto.id:
                    total = 0
                    posicao = 1
                    for produto in produtos:
                        nome = produto.nome
                        preco = produto.preco
                        quantia = produto.quantia
                        print(f"0{posicao} - Produto: {nome}, Preço: {preco}, Quantia: {quantia}")
                        total += float(quantia.replace(",", "."))
                        posicao += 1
                    print(f"Total: R${str(total).replace('.', ',')}")


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
    produtos = find_produtos()
    for produto in produtos:
        for produtoNome in produtosNome:
            if (produto.nome == produtoNome):
                insert_compras(session,email,produto.id)
    tudo_ok()
    voltar_opcoes()



# def update_user(session, new_age, lastname):
#     # TO DO: execute a BoundStatement that updates the age of one user
#     prepared = session.prepare("UPDATE users SET age = ? WHERE lastname = ?")
#     session.execute(prepared, [new_age, lastname])

# def delete_user(session, lastname):
#     # TO DO: execute a BoundStatement that updates the age of one user
#     prepared = session.prepare("DELETE FROM users WHERE lastname = ?")
#     session.execute(prepared, [lastname])

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

def main():
    session.execute("""
        CREATE TABLE IF NOT EXISTS mercado_livre.usuarios (
            id UUID PRIMARY KEY,
            nome text,
            sobrenome text,
            email text,
            endereco list<frozen<map<text, text>>>
        )
    """)

    session.execute("""
        CREATE TABLE IF NOT EXISTS mercado_livre.vendedores (
            id UUID PRIMARY KEY,
            nome text,
            sobrenome text,
            email text,
            produtos list<text>
        )
    """)

    session.execute("""
        CREATE TABLE IF NOT EXISTS mercado_livre.produtos (
            id UUID PRIMARY KEY,
            nome text,
            quantia text,
            preco text
        )
    """)

    session.execute("""
        CREATE TABLE IF NOT EXISTS mercado_livre.compras (
            id UUID PRIMARY KEY,
            email text,
            produto UUID
        )
    """)



    # get_user(session)

    # update_user(session, new_age, lastname)

    # get_user(session, lastname)

    # delete_user(session, lastname)

main()
opcoes()
