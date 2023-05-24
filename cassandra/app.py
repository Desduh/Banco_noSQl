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

def insert_favoritos(session,email,produto):
  print("oi")
  id = uuid.uuid4()
  session.execute("INSERT INTO favoritos (id, email, produto) VALUES (%s,%s,%s)", [id, email,produto])



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

def find_favoritos():
  result = session.execute("SELECT * FROM favoritos;")
  return result



def delete_usuario(session, email):
    id_result = session.execute("SELECT id FROM usuarios WHERE email = %s", [email])
    id = id_result.one().id if id_result else None
    if id:
        prepared = session.prepare("DELETE FROM usuarios WHERE id = ?")
        session.execute(prepared, [id])
        tudo_ok()
    else:
        print("Usuário não encontrado.")
    voltar_opcoes()

def delete_vendedor(session,email):
    id_result = session.execute("SELECT id FROM vendedores WHERE email = %s", [email])
    id = id_result.one().id if id_result else None
    if id:
        prepared = session.prepare("DELETE FROM vendedores WHERE id = ?")
        session.execute(prepared, [id])
        tudo_ok()
    else:
        print("Vendedor não encontrado.")
    voltar_opcoes()

def delete_produto(session,nome):
    id_result = session.execute("SELECT id FROM produtos WHERE nome = %s", [nome])
    id = id_result.one().id if id_result else None
    if id:
        prepared = session.prepare("DELETE FROM produtos WHERE id = ?")
        session.execute(prepared, [id])
        tudo_ok()
    else:
        print("Produto não encontrado.")
    voltar_opcoes()

def delete_compra(session, email):
    nome_result = session.execute("SELECT nome FROM usuarios WHERE email = %s", [email])
    nome = nome_result.one().nome if nome_result else None
    if nome:
        print(f"Cliente: {nome}")
        compras = session.execute("SELECT * FROM compras WHERE email = %s", [email])
        posicao = 1
        for compra in compras:
            preco = session.execute("SELECT preco FROM produtos WHERE nome = %s", [compra.produto]).one().preco
            nome = compra.produto
            print(f"0{posicao} - Produto: {nome}, Preço: R${str(preco).replace('.', ',')}")
            posicao += 1
        chave = True
        while chave:
            produtoNome = input("Produto a excluir: ")
            chave = (input("Deseja excluir outro produto? (s/n): ") == 's')
            id_result = session.execute("SELECT id FROM compras WHERE email = %s AND produto = %s", [email, produtoNome])
            id = id_result.one().id if id_result else None
            if id:
                prepared = session.prepare("DELETE FROM compras WHERE id = ?")
                session.execute(prepared, [id])
                tudo_ok()
            else:
                print("Compra não encontrada.")
    else:
        print("Usuário não encontrado.")
    voltar_opcoes()

def deletar_favorito(session, email):
    nome_result = session.execute("SELECT nome FROM usuarios WHERE email = %s", [email])
    nome = nome_result.one().nome if nome_result else None
    if nome:
        print(f"Cliente: {nome}")
        favoritos = session.execute("SELECT * FROM favoritos WHERE email = %s", [email])
        posicao = 1
        for favorito in favoritos:
            preco = session.execute("SELECT preco FROM produtos WHERE nome = %s", [favorito.produto]).one().preco
            nome = favorito.produto
            print(f"0{posicao} - Produto: {nome}, Preço: R${str(preco).replace('.', ',')}")
            posicao += 1
        chave = True
        while chave:
            produtoNome = input("Produto a excluir: ")
            chave = (input("Deseja excluir outro produto? (s/n): ") == 's')
            id_result = session.execute("SELECT id FROM favoritos WHERE email = %s AND produto = %s", [email, produtoNome])
            id = id_result.one().id if id_result else None
            if id:
                prepared = session.prepare("DELETE FROM favoritos WHERE id = ?")
                session.execute(prepared, [id])
                tudo_ok()
            else:
                print("Favorito não encontrada.")
    else:
        print("Usuário não encontrado.")
    voltar_opcoes()



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
    insert_vendedor(session, nome, sobrenome, email)
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
        print("Favoritos: ")
        pega_favoritos(cliente.email)
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
    for cliente in clientes:
        print(f'Cliente: {cliente.nome}')
        posicao = 1
        total = 0  
        compras = session.execute("SELECT * FROM compras WHERE email = %s", [cliente.email])
        for compra in compras:
            preco = session.execute("SELECT preco FROM produtos WHERE nome = %s", [compra.produto]).one().preco
            nome = compra.produto
            print(f"0{posicao} - Produto: {nome}, Preço: R${str(preco).replace('.', ',')}")
            total += float(preco.replace(",", "."))
            posicao += 1
    print(f"Total: R${str(total).replace('.', ',')}")

def pega_favoritos(email):
        posicao = 1
        favoritos = session.execute("SELECT * FROM favoritos WHERE email = %s", [email])
        for favorito in favoritos:
            preco = session.execute("SELECT preco FROM produtos WHERE nome = %s", [favorito.produto]).one().preco
            nome = favorito.produto
            print(f"0{posicao} - Produto: {nome}, Preço: R${str(preco).replace('.', ',')}")
            posicao += 1



def atualizar_usuario():
    email = input("Email do usuário a atualizar: ")
    row = session.execute("SELECT id FROM usuarios WHERE email = %s", [email]).one()
    if not row:
        print("Usuário não encontrado.")
        voltar_opcoes()
    user_id = row.id
    print("Quais campos deseja atualizar?")
    print("01 - Nome")
    print("02 - Sobrenome")
    print("03 - Email")
    campos = input("Quais campos? (exemplo: 01,02,03): ")
    campos = campos.split(",")
    for campo in campos:
        campo = int(campo)
        if campo == 1:
            nome = input("Novo nome: ")
            session.execute("UPDATE usuarios SET nome = %s WHERE id = %s", [nome, user_id])
        elif campo == 2:
            sobrenome = input("Novo sobrenome: ")
            session.execute("UPDATE usuarios SET sobrenome = %s WHERE id = %s", [sobrenome, user_id])
        elif campo == 3:
            novo_email = input("Novo email: ")
            session.execute("UPDATE usuarios SET email = %s WHERE id = %s", [novo_email, user_id])
    tudo_ok()
    voltar_opcoes()

def atualizar_vendedor():
    email = input("Email do vendedor a atualizar: ")
    row = session.execute("SELECT id FROM vendedores WHERE email = %s", [email]).one()
    if not row:
        print("Vendedor não encontrado.")
        voltar_opcoes()
    user_id = row.id
    print("Quais campos deseja atualizar?")
    print("01 - Nome")
    print("02 - Sobrenome")
    print("03 - Email")
    campos = input("Quais campos? (exemplo: 01,02,03): ")
    campos = campos.split(",")
    for campo in campos:
        campo = int(campo)
        if campo == 1:
            nome = input("Novo nome: ")
            session.execute("UPDATE vendedores SET nome = %s WHERE id = %s", [nome, user_id])
        elif campo == 2:
            sobrenome = input("Novo sobrenome: ")
            session.execute("UPDATE vendedores SET sobrenome = %s WHERE id = %s", [sobrenome, user_id])
        elif campo == 3:
            novo_email = input("Novo email: ")
            session.execute("UPDATE vendedores SET email = %s WHERE id = %s", [novo_email, user_id])
    tudo_ok()
    voltar_opcoes()

def atualizar_produto():
    nome = input("Nome do produto a atualizar: ")
    row = session.execute("SELECT id FROM produtos WHERE nome = %s", [nome]).one()
    if not row:
        print("Produto não encontrado.")
        voltar_opcoes()
    id_prod = row.id
    print("Quais campos deseja atualizar?")
    print("01 - Nome")
    print("02 - Valor")
    print("03 - Quantia")
    campos = input("Quais campos? (exemplo: 01,02,03): ")
    campos = campos.split(",")
    for campo in campos:
        campo = int(campo)
        if campo == 1:
            nome = input("Novo nome: ")
            session.execute("UPDATE produtos SET nome = %s WHERE id = %s", [nome, id_prod])
        elif campo == 2:
            preco = input("Novo valor: ")
            session.execute("UPDATE produtos SET preco = %s WHERE id = %s", [preco, id_prod])
        elif campo == 3:
            quantia = input("Nova quantia: ")
            session.execute("UPDATE produtos SET quantia = %s WHERE id = %s", [quantia, id_prod])
    tudo_ok()
    voltar_opcoes()



def cadastrar_compras():
    email = input("Email do usuário que vai comprar: ")
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
                insert_compras(session,email,produto.nome)
    tudo_ok()
    voltar_opcoes()

def cadastrar_favoritos():
    email = input("Email do usuário que vai favoritar: ")
    print('')
    print("Produtos disponíveis:")
    pega_produtos()
    produtosNome = []
    chave = True
    while chave:
        produtoNome = input("Nome do produto favoritado: ")
        produtosNome.append(produtoNome)
        chave = (input("Deseja adicionar outro favorito? (s/n): ") == 's')
    produtos = find_produtos()
    for produto in produtos:
        for produtoNome in produtosNome:
            if (produto.nome == produtoNome):
                insert_favoritos(session,email,produto.nome)
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
    print("07 - Remover Favoritos")
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
        delete_usuario(session,email)

    elif(opcao == 5):
        cadastrar_compras()

    elif(opcao == 6):
        cadastrar_favoritos()        

    elif(opcao == 7):
        email = input("Email do usuário relacionado ao favorito: ")
        deletar_favorito(session,email)    

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
        delete_vendedor(session,email)

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
        delete_produto(session,nome)

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
        email = input("Email do usuário relacionado à compra: ")
        delete_compra(session,email)

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
            produto text
        )
    """)

    session.execute("""
        CREATE TABLE IF NOT EXISTS mercado_livre.favoritos (
            id UUID PRIMARY KEY,
            email text,
            produto text
        )
    """)

    session.execute("CREATE INDEX IF NOT EXISTS email_usuario ON usuarios (email);")
    session.execute("CREATE INDEX IF NOT EXISTS email_vendedor ON vendedores (email);")
    session.execute("CREATE INDEX IF NOT EXISTS nome_produto ON produtos (nome);")
    session.execute("CREATE INDEX IF NOT EXISTS email_compra ON compras (email);")
    session.execute("CREATE INDEX IF NOT EXISTS produto_compra ON compras (produto);")
    session.execute("CREATE INDEX IF NOT EXISTS email_favorito ON favoritos (email);")
    session.execute("CREATE INDEX IF NOT EXISTS produto_favorito ON favoritos (produto);")

    # get_user(session)

    # update_user(session, new_age, lastname)

    # get_user(session, lastname)

    # delete_user(session, lastname)

main()
opcoes()
