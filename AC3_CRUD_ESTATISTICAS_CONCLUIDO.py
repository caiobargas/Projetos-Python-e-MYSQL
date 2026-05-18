# Avaliação Continuada 3 - 1 ponto
# PROJETO DE VENDAS - parte 1
# Exercicios de estatisticas de vendas.
# Entrega - dia 17/05/2026

import mysql.connector
from mysql.connector import Error
from datetime import datetime


def conectar():
    try:
        conexao = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='310805Cv@',
            database='projeto_vendas_eletronicos_unifecaf',
            auth_plugin='mysql_native_password'
        )

        if conexao.is_connected():
            print("Conectado ao MySQL com sucesso!")
            return conexao

    except Error as e:
        print(f"Erro ao conectar: {e}")
        return None


def fechar_conexao(conexao):
    if conexao and conexao.is_connected():
        conexao.close()
        print("Conexão encerrada.")


def total_vendas_periodo():

    while True:
        data_inicial = input("Digite a data inicial (YYYY-MM-DD): ")
        try:
            datetime.strptime(data_inicial, "%Y-%m-%d")
            break
        except:
            print("Data inválida, tente uma data valida")

    while True:
        data_final = input("Digite a data final (YYYY-MM-DD): ")
        try:
            datetime.strptime(data_final, "%Y-%m-%d")
            break
        except:
            print("Data inválida, tente uma data valida")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT
            SUM(valor_final) valor_total
        FROM vendas
         WHERE data_e_hora BETWEEN %s AND %s
        """, (data_inicial, data_final))

    valor_total = cursor.fetchone()

    print("\n=== VALOR TOTAL DE VENDAS ===")
    print(f"VALOR TOTAL: {valor_total[0]}")

    cursor.close()
    fechar_conexao(conexao)


def qtd_vendas_por_vendedor():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT
            vendedores.nome vendedor,
            COUNT(*) qtd_vendas
        FROM vendas
        INNER JOIN vendedores
            ON vendas.id_vendedor = vendedores.id
        GROUP BY vendedores.id
    """)

    vendedores = cursor.fetchall()

    print("\n=== QUANTIDADE DE VENDAS POR VENDEDOR ===")
    for vendedor in vendedores:
        print(f"VENDEDOR: {vendedor[0]} - QTD VENDAS: {vendedor[1]}")

    cursor.close()
    fechar_conexao(conexao)


def ticket_medio_geral():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT
        AVG(valor_final) ticket_medio
        FROM vendas
    """)

    resultado = cursor.fetchone()

    print("\n=== TICKET MÉDIO GERAL ===")
    print(f"TICKET MÉDIO: R$ {resultado[0]:.2f}")

    cursor.close()
    fechar_conexao(conexao)


def ticket_medio_por_vendedor():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT
            vendedores.nome vendedor,
            AVG(vendas.valor_final) ticket_medio
        FROM vendas
        INNER JOIN vendedores
            ON vendas.id_vendedor = vendedores.id
        GROUP BY vendedores.nome
    """)

    vendedores = cursor.fetchall()

    print("\n=== TICKET MÉDIO POR VENDEDOR ===")

    for vendedor in vendedores:
        print(f"VENDEDOR: {vendedor[0]} - TICKET MÉDIO: R$ {vendedor[1]:.2f}")

    cursor.close()
    fechar_conexao(conexao)


def produto_mais_vendido_qtd():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT
            produtos.descricao,
            SUM(vendas_produtos.quantidade) qtd_vendida
        FROM vendas_produtos
        INNER JOIN produtos
            ON vendas_produtos.id_produto = produtos.id
        GROUP BY produtos.id
        ORDER BY SUM(vendas_produtos.quantidade) DESC 
        LIMIT 1
    """)

    produto = cursor.fetchone()

    print("\n=== PRODUTO MAIS VENDIDO ===")
    print(f"PRODUTO: {produto[0]} - QUANTIDADE VENDIDA: {produto[1]}")

    cursor.close()
    fechar_conexao(conexao)


def produto_mais_rentavel_valor():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT
            produtos.descricao,
            SUM(vendas_produtos.valor_total) 
        FROM vendas_produtos
        INNER JOIN produtos
            ON vendas_produtos.id_produto = produtos.id
        GROUP BY produtos.id, produtos.descricao
        ORDER BY SUM(vendas_produtos.valor_total) DESC
        LIMIT 1
    """)

    produto = cursor.fetchone()

    print("\n=== PRODUTO MAIS RENTÁVEL ===")
    print(f"PRODUTO: {produto[0]} - FATURAMENTO: R$ {produto[1]:.2f}")

    cursor.close()
    fechar_conexao(conexao)


def total_descontos_aplicados():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT SUM(vendas.desconto)
        FROM vendas
    """)

    resultado = cursor.fetchone()

    print("\n=== TOTAL DE DESCONTOS APLICADOS ===")
    print(f"TOTAL DE DESCONTOS: R$ {resultado[0]:.2f}")

    cursor.close()
    fechar_conexao(conexao)


def percentual_desconto_medio():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT
            AVG(vendas.desconto / (valor_final + vendas.desconto)) * 100
        FROM vendas
    """)

    resultado = cursor.fetchone()

    print("\n=== PERCENTUAL MÉDIO DE DESCONTO ===")
    print(f"PERCENTUAL MÉDIO: {resultado[0]:.2f}%")


    cursor.close()
    fechar_conexao(conexao)


def faturamento_por_dia():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT
           DATE(data_e_hora),
            SUM(valor_final)
        FROM vendas
        GROUP BY DATE(data_e_hora)
        ORDER BY DATE(data_e_hora)
    """)

    resultados = cursor.fetchall()

    print("\n=== FATURAMENTO POR DIA ===")

    for resultado in resultados:
        print(f"DATA: {resultado[0]} - FATURAMENTO: R$ {resultado[1]:.2f}")
    else:
        print("Nenhuma venda encontrada.")
    

    cursor.close()
    fechar_conexao(conexao)


def top_3_vendedores_faturamento():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT 
            vendedores.nome,
            SUM(vendas.valor_final)
        FROM vendas
        INNER JOIN vendedores
            ON vendas.id_vendedor = vendedores.id
        GROUP BY vendedores.id, vendedores.nome
        ORDER BY SUM(vendas.valor_final) DESC
        LIMIT 3
    """)

    vendedores = cursor.fetchall()

    print("\n=== TOP 3 VENDEDORES POR FATURAMENTO ===")

    for vendedor in vendedores:
        print(f"VENDEDOR: {vendedor[0]} - FATURAMENTO: R$ {vendedor[1]:.2f}")

    cursor.close()
    fechar_conexao(conexao)


def menu_relatorios():
    opcoes = {
        "1": ("Total de vendas por periodo", total_vendas_periodo),
        "2": ("Quantidade de vendas por vendedor", qtd_vendas_por_vendedor),
        "3": ("Ticket medio geral", ticket_medio_geral),
        "4": ("Ticket medio por vendedor", ticket_medio_por_vendedor),
        "5": ("Produto mais vendido por quantidade", produto_mais_vendido_qtd),
        "6": ("Produto mais rentavel por faturamento", produto_mais_rentavel_valor),
        "7": ("Total de descontos aplicados", total_descontos_aplicados),
        "8": ("Percentual medio de desconto", percentual_desconto_medio),
        "9": ("Faturamento por dia", faturamento_por_dia),
        "10": ("Top 3 vendedores por faturamento", top_3_vendedores_faturamento),
    }

    while True:
        print("\n=== MENU AC3 - RELATORIOS ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Voltar")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Voltando ao menu principal.")
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\nGerando relatorio: {descricao}")
            funcao()
        else:
            print("Opcao invalida. Tente novamente.")


menu_relatorios()
