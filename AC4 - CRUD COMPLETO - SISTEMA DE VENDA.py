# AC4 - CRUD COMPLETO - PROJETO DE VENDAS
# PROJETO DE VENDAS - parte 2
# Exercicios de CRUD completo (Produtos, Vendedores e Vendas)
# Entrega - dia 24/05/2026


# PRODUTOS


import mysql.connector
from mysql.connector import Error
from datetime import datetime
from decimal import Decimal


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


def criar_produto():
    """Exercicio 1: cadastrar um novo produto na tabela produtos (descricao, preco)."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, descricao, preco FROM produtos
    """)
    produtos = cursor.fetchall()
    print("\n=== PRODUTOS CADASTRADOS ===")
    for produto in produtos:
        print(
            f"ID: {produto[0]} | Descrição: {produto[1]} | Preço: R$ {produto[2]:.2f}")

    descricao = input("Digite a descrição do produto: ").strip()

    while True:
        try:
            preco = float(
                input("Digite o preço do produto (maior que zero): ").replace(',', '.'))
            if preco > 0:
                break
        except ValueError:
            pass
        print("Preço inválido! Digite um valor maior que zero.")

    cursor.execute(
        """
        INSERT INTO produtos (descricao, preco)
        VALUES (%s, %s)
        """,
        (descricao, preco),
    )

    conexao.commit()
    print("Produto cadastrado com sucesso!")

    cursor.execute("""
        SELECT id, descricao, preco FROM produtos
        """)
    produtos = cursor.fetchall()
    print("\n=== LISTA DE PRODUTOS ATUALIZADA ===")
    for produto in produtos:
        print(
            f"ID: {produto[0]} | Descrição: {produto[1]} | Preço: R$ {produto[2]:.2f}")

    cursor.close()
    fechar_conexao(conexao)


def listar_produtos():
    # Exercicio 2: listar todos os produtos cadastrados com id, descricao e preco.
    conexao = conectar()
    if not conexao:
        return
    cursor = conexao.cursor()
    cursor.execute("SELECT id, descricao, preco FROM produtos")
    produtos = cursor.fetchall()
    for produto in produtos:
        print(
            f"ID: {produto[0]}, Descrição: {produto[1]}, Preço: {produto[2]}")

    cursor.close()
    fechar_conexao(conexao)


def atualizar_produto():
    # Exercicio 3: atualizar descricao e/ou preco de um produto existente por id.

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, descricao
        FROM produtos
    """)

    produtos = cursor.fetchall()

    print("\n=== PRODUTOS CADASTRADOS ===")

    for produto in produtos:
        print(f"ID: {produto[0]} | Descrição: {produto[1]}")

    print()

    while True:
        id_produto = input("Digite o ID do produto a ser atualizado: ").strip()

        if id_produto.isdigit():
            id_produto = int(id_produto)
            break

        print("ID inválido! Digite apenas números.")

    cursor.execute("""
        SELECT id, descricao, preco
        FROM produtos
        WHERE id = %s
    """, (id_produto,))

    produto = cursor.fetchone()

    if produto is None:
        print("Produto não encontrado.")

        cursor.close()
        fechar_conexao(conexao)
        return

    print("\n=== PRODUTO ATUAL ===")
    print(f"ID: {produto[0]}")
    print(f"Descrição: {produto[1]}")
    print(f"Preço: R$ {produto[2]:.2f}")

    nova_descricao = input("\nDigite a nova descrição: ").strip()

    while True:
        try:
            novo_preco = float(
                input("Digite o novo preço: ").replace(',', '.')
            )

            if novo_preco > 0:
                break

            print("O preço deve ser maior que zero.")

        except ValueError:
            print("Preço inválido! Digite um valor numérico válido.")

    cursor.execute("""
        UPDATE produtos
        SET descricao = %s,
            preco = %s
        WHERE id = %s
    """, (nova_descricao, novo_preco, id_produto))

    conexao.commit()
    print("\nProduto atualizado com sucesso!")

    cursor.execute("""
    SELECT id, descricao, preco
    FROM produtos
""")

    produtos = cursor.fetchall()

    print("\n=== LISTA DE PRODUTOS ATUALIZADA ===")

    for produto in produtos:
        print(
            f"ID: {produto[0]} | "
            f"Descrição: {produto[1]} | "
            f"Preço: R$ {produto[2]:.2f}"
        )

    cursor.close()
    fechar_conexao(conexao)


def excluir_produto():
    # Exercicio 4: excluir um produto por id, tratando dependencias em vendas_produtos.
    conexao = conectar()
    cursor = conexao.cursor()

    try:

        # =========================
        # LISTAR PRODUTOS
        # =========================
        print("\n=== PRODUTOS CADASTRADOS ===")

        cursor.execute("""
            SELECT
                id,
                descricao,
                preco
            FROM produtos
        """)

        produtos = cursor.fetchall()

        if not produtos:
            print("Nenhum produto cadastrado.")

        else:

            for produto in produtos:

                id_produto, descricao, preco = produto

                print(
                    f"ID: {id_produto} | "
                    f"PRODUTO: {descricao} | "
                    f"PREÇO: R$ {preco:.2f}"
                )

        # =========================
        # ESCOLHER PRODUTO
        # =========================
        id_produto = int(
            input("\nDigite o ID do produto a ser excluído: ")
        )

        # =========================
        # VERIFICAR EXISTÊNCIA
        # =========================
        cursor.execute("""
            SELECT id
            FROM produtos
            WHERE id = %s
        """, (id_produto,))

        produto = cursor.fetchone()

        if produto is None:

            print("Produto não encontrado.")

        else:

            # =========================
            # EXCLUIR ITENS RELACIONADOS
            # =========================
            cursor.execute("""
                DELETE FROM vendas_produtos
                WHERE id_produto = %s
            """, (id_produto,))

            # =========================
            # EXCLUIR PRODUTO
            # =========================
            cursor.execute("""
                DELETE FROM produtos
                WHERE id = %s
            """, (id_produto,))

            conexao.commit()

            print(
                "\nProduto excluído com sucesso "
                "(e itens relacionados removidos)."
            )

        # =========================
        # LISTAR PRODUTOS APÓS EXCLUSÃO
        # =========================
        print("\n=== PRODUTOS ATUALIZADOS ===")

        cursor.execute("""
            SELECT
                id,
                descricao,
                preco
            FROM produtos
        """)

        produtos_atualizados = cursor.fetchall()

        if not produtos_atualizados:

            print("Nenhum produto cadastrado.")

        else:

            for produto in produtos_atualizados:

                id_produto, descricao, preco = produto

                print(
                    f"ID: {id_produto} | "
                    f"PRODUTO: {descricao} | "
                    f"PREÇO: R$ {preco:.2f}"
                )

    except ValueError:
        print("Digite um ID válido.")

    except Exception as erro:
        print(f"Erro ao excluir produto: {erro}")

    finally:
        cursor.close()
        conexao.close()
        print("Conexão encerrada.")


# VENDEDORES

def criar_vendedor():
    # Exercicio 5: cadastrar um novo vendedor na tabela vendedores.
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome FROM vendedores
    """)
    vendedores = cursor.fetchall()
    print("\n=== VENDEDORES CADASTRADOS ===")
    for vendedor in vendedores:
        print(
            f"ID: {vendedor[0]} | Nome: {vendedor[1]}")

    nome = input("Digite o nome do vendedor á ser cadastrado: ").strip()
    cursor.execute("""
            INSERT INTO vendedores (nome)
            VALUES (%s)
        """, (nome,))

    conexao.commit()
    print("Vendedor cadastrado com sucesso!")

    cursor.execute("""
        SELECT id, nome
        FROM vendedores
        """)
    vendedores = cursor.fetchall()
    print("\n=== LISTA DE VENDEDORES ATUALIZADA ===")
    for vendedor in vendedores:
        print(f"ID: {vendedor[0]} | Nome: {vendedor[1]}")

    cursor.close()
    fechar_conexao(conexao)


def listar_vendedores():
    # Exercicio 6: listar todos os vendedores cadastrados.
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome FROM vendedores")
    vendedores = cursor.fetchall()
    print("\n=== VENDEDORES CADASTRADOS ===")
    for vendedor in vendedores:
        print(f"ID: {vendedor[0]}, Nome: {vendedor[1]}")

    cursor.close()
    fechar_conexao(conexao)


def atualizar_vendedor():
    # Exercicio 7: atualizar o nome de um vendedor existente por id.
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome
        FROM vendedores
    """)

    vendedores = cursor.fetchall()

    print("\n=== VENDEDORES CADASTRADOS ===")

    for vendedor in vendedores:
        print(f"ID: {vendedor[0]} | Nome: {vendedor[1]}")

    print()

    while True:
        id_vendedor = input(
            "Digite o ID do vendedor a ser atualizado: ").strip()

        if id_vendedor.isdigit():
            id_vendedor = int(id_vendedor)
            break

        print("ID inválido! Digite apenas números.")

    cursor.execute("""
        SELECT id, nome FROM vendedores
        WHERE id = %s
    """, (id_vendedor,))

    vendedores = cursor.fetchone()
    if vendedores is None:
        print("Vendedor não encontrado.")
        cursor.close()
        fechar_conexao(conexao)
        return

    print("\n=== VENDEDOR ATUAL ===")
    print(f"ID: {vendedores[0]}")
    print(f"Nome: {vendedores[1]}")
    novo_nome = input("\nDigite o novo nome do vendedor: ").strip()
    cursor.execute("""
        UPDATE vendedores
        SET nome = %s
        WHERE id = %s
    """, (novo_nome, id_vendedor))
    conexao.commit()
    print("\nVendedor atualizado com sucesso!")

    cursor.execute("""
    SELECT id, nome
    FROM vendedores
    """)

    vendedores = cursor.fetchall()

    print("\n=== LISTA DE VENDEDORES ATUALIZADA ===")

    for vendedor in vendedores:
        print(
            f"ID: {vendedor[0]} | "
            f"Nome: {vendedor[1]}"
        )
    cursor.close()
    fechar_conexao(conexao)


def excluir_vendedor():
    # Exercicio 8: excluir vendedor por id, validando se possui vendas vinculadas.
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome
        FROM vendedores
    """)
    vendedores = cursor.fetchall()
    print("\n=== VENDEDORES CADASTRADOS ===")
    for vendedor in vendedores:
        print(f"ID: {vendedor[0]} | Nome: {vendedor[1]}")

    id_vendedores = input("Digite o ID do vendedor a ser excluído: ").strip()
    cursor.execute("""
        SELECT COUNT(*) FROM vendas
        WHERE id_vendedor = %s
    """, (id_vendedores,))
    id_vendedor = cursor.fetchone()[0]
    if id_vendedor > 0:
        print("Não é possível excluir o vendedor, existem vendas vinculadas.")
    else:
        cursor.execute("""
            DELETE FROM vendedores
            WHERE id = %s
        """, (id_vendedores,))
        conexao.commit()
        if cursor.rowcount > 0:
            print("Vendedor excluído com sucesso.")
        else:
            print("Nenhum vendedor encontrado com esse ID.")

    conexao.commit()

    cursor.execute("""
    SELECT id, nome
    FROM vendedores
    """)

    vendedores = cursor.fetchall()

    print("\n=== LISTA DE VENDEDORES ATUALIZADA ===")

    for vendedor in vendedores:
        print(
            f"ID: {vendedor[0]} | "
            f"Nome: {vendedor[1]}"
        )

    cursor.close()
    fechar_conexao(conexao)

# VENDAS


def criar_venda_com_itens():
    # Exercicio 9: criar uma venda e inserir itens na tabela vendas_produtos com quantidade e valores.
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        # =========================
        # LISTAR VENDEDORES
        # =========================
        print("\n=== VENDEDORES DISPONÍVEIS ===")

        cursor.execute("""
            SELECT id, nome
            FROM vendedores
        """)

        vendedores = cursor.fetchall()

        for vendedor in vendedores:
            print(f"ID: {vendedor[0]} | Nome: {vendedor[1]}")

        id_vendedor = int(input("\nDigite o ID do vendedor: "))
        desconto_percentual = Decimal(input("Digite o desconto em %(Digite apenas o numero, ex: 10% para 10: ")
                                      )

        # =========================
        # CRIAR VENDA
        # =========================
        cursor.execute("""
            INSERT INTO vendas (
                id_vendedor,
                data_e_hora,
                desconto,
                valor_final
            )
            VALUES (%s, NOW(), %s, %s)
        """, (id_vendedor, 0, 0))

        conexao.commit()

        # PEGAR ID DA VENDA CRIADA
        id_venda = cursor.lastrowid

        print(f"\nVenda criada com sucesso! ID DA VENDA: {id_venda}")

        total_venda = Decimal("0")

        # =========================
        # INSERIR PRODUTOS
        # =========================
        while True:

            print("\n=== PRODUTOS DISPONÍVEIS ===")

            cursor.execute("""
                SELECT id, descricao, preco
                FROM produtos
            """)

            produtos = cursor.fetchall()

            for produto in produtos:
                print(
                    f"ID: {produto[0]} | "
                    f"Produto: {produto[1]} | "
                    f"Preço: R$ {produto[2]:.2f}"
                )

            id_produto = int(input("\nDigite o ID do produto: "))
            quantidade = int(input("Digite a quantidade: "))

            # BUSCAR PREÇO DO PRODUTO
            cursor.execute("""
                SELECT preco
                FROM produtos
                WHERE id = %s
            """, (id_produto,))

            resultado = cursor.fetchone()

            if resultado is None:
                print("Produto não encontrado.")
                continue

            valor_unitario = resultado[0]
            valor_total = valor_unitario * quantidade

            # INSERIR ITEM DA VENDA
            cursor.execute("""
                INSERT INTO vendas_produtos (
                    id_venda,
                    id_produto,
                    quantidade,
                    valor_unitario,
                    valor_total
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                id_venda,
                id_produto,
                quantidade,
                valor_unitario,
                valor_total
            ))

            conexao.commit()

            total_venda += valor_total

            print("Produto adicionado à venda com sucesso!")

            continuar = input(
                "\nDeseja adicionar outro produto? (s/n): ").lower()

            if continuar != "s":
                break

        # =========================
        # CALCULAR VALOR FINAL
        # =========================
        valor_desconto = (total_venda * desconto_percentual) / Decimal("100")
        valor_final = total_venda - valor_desconto

        if valor_final < 0:
            valor_final = 0

        # ATUALIZAR VALOR FINAL DA VENDA
        cursor.execute("""
            UPDATE vendas
            SET valor_final = %s
            WHERE id = %s
        """, (valor_final, id_venda))

        conexao.commit()

        # =========================
        # RESUMO DA VENDA
        # =========================
        print("\n=== RESUMO DA VENDA ===")

        cursor.execute("""
            SELECT
                p.descricao,
                vp.quantidade,
                vp.valor_unitario,
                vp.valor_total
            FROM vendas_produtos vp
            JOIN produtos p
                ON vp.id_produto = p.id
            WHERE vp.id_venda = %s
        """, (id_venda,))

        itens = cursor.fetchall()

        for item in itens:
            descricao, quantidade, valor_unitario, valor_total = item

            print(
                f"Produto: {descricao} | "
                f"Quantidade: {quantidade} | "
                f"Valor Unitário: R$ {valor_unitario:.2f} | "
                f"Valor Total: R$ {valor_total:.2f}"
            )

        print(f"\nTOTAL DA VENDA: R$ {total_venda:.2f}")
        print(f"DESCONTO (%): {desconto_percentual}%")
        print(f"VALOR DO DESCONTO: R$ {valor_desconto:.2f}")
        print(f"VALOR FINAL: R$ {valor_final:.2f}")

    except ValueError:
        print("Erro: digite valores numéricos válidos.")

    except Exception as erro:
        print(f"Erro ao criar venda: {erro}")

    finally:
        cursor.close()
        conexao.close()
        print("\nConexão encerrada.")


def listar_vendas_completas():
    # Exercicio 10: listar vendas com vendedor e itens (produto, quantidade, valor_unitario, valor_total).
    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("""
            SELECT
                ve.id,
                ve.nome,
                p.descricao,
                vp.quantidade,
                vp.valor_unitario,
                v.desconto
            FROM vendas_produtos vp

            JOIN vendas v
                ON vp.id_venda = v.id

            JOIN vendedores ve
                ON v.id_vendedor = ve.id

            JOIN produtos p
                ON vp.id_produto = p.id
        """)

        vendas = cursor.fetchall()

        if not vendas:
            print("Nenhuma venda encontrada.")
            return

        print("\n=== LISTA DE VENDAS ===")

        for venda in vendas:

            (
                id_vendedor,
                vendedor,
                produto,
                quantidade,
                valor_unitario,
                desconto_percentual
            ) = venda

            # =========================
            # SUBTOTAL
            # =========================
            subtotal = valor_unitario * quantidade

            # =========================
            # CALCULAR VALOR REAL DESCONTO
            # =========================
            valor_desconto = (
                subtotal * desconto_percentual
            ) / 100

            # =========================
            # TOTAL FINAL
            # =========================
            valor_total = subtotal - valor_desconto

            print(
                f"\nID VENDEDOR: {id_vendedor} | "
                f"VENDEDOR: {vendedor}"
            )

            print(
                f"PRODUTO: {produto} | "
                f"QUANTIDADE: {quantidade} | "
                f"VALOR UNITÁRIO: R$ {valor_unitario:.2f} | "
                f"DESCONTO: {desconto_percentual:.0f}% | "
                f"VALOR DESCONTO: R$ {valor_desconto:.2f} | "
                f"VALOR TOTAL: R$ {valor_total:.2f}"
            )

    except Exception as erro:

        print(f"Erro ao listar vendas: {erro}")

    finally:

        cursor.close()
        conexao.close()

        print("\nConexão encerrada.")


def atualizar_venda_e_itens():
    # Exercicio 11: atualizar dados da venda (desconto/valor_final) e seus itens.
    conexao = conectar()
    cursor = conexao.cursor()

    try:

        # =========================
        # LISTAR VENDAS
        # =========================
        print("\n=== VENDAS CADASTRADAS ===")

        cursor.execute("""
            SELECT
                v.id,
                ve.nome,
                v.valor_final
            FROM vendas v

            JOIN vendedores ve
                ON v.id_vendedor = ve.id
        """)

        vendas = cursor.fetchall()

        if not vendas:
            print("Nenhuma venda encontrada.")
            return

        for venda in vendas:

            id_venda, vendedor, valor_final = venda

            print(
                f"ID VENDA: {id_venda} | "
                f"VENDEDOR: {vendedor} | "
                f"VALOR FINAL: R$ {valor_final:.2f}"
            )

        # =========================
        # ESCOLHER VENDA
        # =========================
        id_venda = int(
            input("\nDigite o ID da venda que deseja atualizar: ")
        )

        # =========================
        # VERIFICAR EXISTÊNCIA
        # =========================
        cursor.execute("""
            SELECT id
            FROM vendas
            WHERE id = %s
        """, (id_venda,))

        venda = cursor.fetchone()

        if venda is None:
            print("Venda não encontrada.")
            return

        # =========================
        # LISTAR ITENS DA VENDA
        # =========================
        print("\n=== ITENS DA VENDA ===")

        cursor.execute("""
            SELECT
                vp.id_produto,
                p.descricao,
                vp.quantidade,
                vp.valor_unitario,
                vp.valor_total
            FROM vendas_produtos vp

            JOIN produtos p
                ON vp.id_produto = p.id

            WHERE vp.id_venda = %s
        """, (id_venda,))

        itens = cursor.fetchall()

        if not itens:
            print("Nenhum item encontrado.")
            return

        for item in itens:

            (
                id_produto,
                produto,
                quantidade,
                valor_unitario,
                valor_total
            ) = item

            print(
                f"\nID PRODUTO: {id_produto} | "
                f"PRODUTO: {produto} | "
                f"QTD: {quantidade} | "
                f"UNITÁRIO: R$ {valor_unitario:.2f} | "
                f"TOTAL: R$ {valor_total:.2f}"
            )

        # =========================
        # ESCOLHER PRODUTO
        # =========================
        id_produto = int(
            input("\nDigite o ID do produto que deseja atualizar: ")
        )

        nova_quantidade = int(
            input("Digite a nova quantidade: ")
        )

        # =========================
        # BUSCAR VALOR UNITÁRIO
        # =========================
        cursor.execute("""
            SELECT valor_unitario
            FROM vendas_produtos
            WHERE id_produto = %s
            AND id_venda = %s
        """, (
            id_produto,
            id_venda
        ))

        resultado = cursor.fetchone()

        if resultado is None:
            print("Produto não encontrado na venda.")
            return

        valor_unitario = resultado[0]

        # =========================
        # NOVO TOTAL DO ITEM
        # =========================
        novo_valor_total = (
            valor_unitario * nova_quantidade
        )

        # =========================
        # ATUALIZAR ITEM
        # =========================
        cursor.execute("""
            UPDATE vendas_produtos
            SET quantidade = %s,
                valor_total = %s
            WHERE id_produto = %s
            AND id_venda = %s
        """, (
            nova_quantidade,
            novo_valor_total,
            id_produto,
            id_venda
        ))

        conexao.commit()

        # =========================
        # RECALCULAR TOTAL DA VENDA
        # =========================
        cursor.execute("""
            SELECT SUM(valor_total)
            FROM vendas_produtos
            WHERE id_venda = %s
        """, (id_venda,))

        soma_total = cursor.fetchone()[0]

        if soma_total is None:
            soma_total = Decimal("0")

        # =========================
        # NOVO DESCONTO %
        # =========================
        desconto_percentual = Decimal(
            input("\nDigite o novo desconto (%): ")
        )

        # =========================
        # CALCULAR DESCONTO
        # =========================
        valor_desconto = (
            soma_total * desconto_percentual
        ) / Decimal("100")

        # =========================
        # CALCULAR VALOR FINAL
        # =========================
        valor_final = soma_total - valor_desconto

        # =========================
        # EVITAR NEGATIVO
        # =========================
        if valor_final < 0:
            valor_final = Decimal("0")

        # =========================
        # ATUALIZAR VENDA
        # SALVANDO A PORCENTAGEM
        # =========================
        cursor.execute("""
            UPDATE vendas
            SET desconto = %s,
                valor_final = %s
            WHERE id = %s
        """, (
            desconto_percentual,
            valor_final,
            id_venda
        ))

        conexao.commit()

        print("\nVenda atualizada com sucesso!")

        # =========================
        # MOSTRAR VENDA ATUALIZADA
        # =========================
        print("\n=== VENDA ATUALIZADA ===")

        cursor.execute("""
            SELECT
                p.descricao,
                vp.quantidade,
                vp.valor_unitario,
                v.desconto
            FROM vendas_produtos vp

            JOIN produtos p
                ON vp.id_produto = p.id

            JOIN vendas v
                ON vp.id_venda = v.id

            WHERE vp.id_venda = %s
        """, (id_venda,))

        itens_atualizados = cursor.fetchall()

        for item in itens_atualizados:

            (
                produto,
                quantidade,
                valor_unitario,
                desconto_percentual
            ) = item

            subtotal = valor_unitario * quantidade

            valor_desconto = (
                subtotal * desconto_percentual
            ) / Decimal("100")

            valor_total = subtotal - valor_desconto

            print(
                f"\nPRODUTO: {produto} | "
                f"QTD: {quantidade} | "
                f"UNITÁRIO: R$ {valor_unitario:.2f} | "
                f"DESCONTO: {desconto_percentual:.0f}% | "
                f"VALOR DESCONTO: R$ {valor_desconto:.2f} | "
                f"VALOR TOTAL: R$ {valor_total:.2f}"
            )

        print(f"\nVALOR FINAL DA VENDA: R$ {valor_final:.2f}")

    except ValueError:
        print("Digite valores válidos.")

    except Exception as erro:
        print(f"Erro ao atualizar venda: {erro}")

    finally:
        cursor.close()
        conexao.close()
        print("\nConexão encerrada.")


def excluir_venda():
    # Exercicio 12: excluir uma venda por id removendo primeiro os itens de vendas_produtos.
    conexao = conectar()
    cursor = conexao.cursor()

    try:

        print("\n=== VENDAS CADASTRADAS ===")

        cursor.execute("""
            SELECT
                v.id,
                ve.nome,
                v.valor_final
            FROM vendas v
            JOIN vendedores ve
                ON v.id_vendedor = ve.id
        """)

        vendas = cursor.fetchall()

        if not vendas:
            print("Nenhuma venda encontrada.")
        else:

            for venda in vendas:

                id_venda, vendedor, valor_final = venda

                print(
                    f"ID VENDA: {id_venda} | "
                    f"VENDEDOR: {vendedor} | "
                    f"VALOR FINAL: R$ {valor_final:.2f}"
                )

        id_venda = int(
            input("\nDigite o ID da venda que deseja excluir: ")
        )

        # VERIFICAR EXISTÊNCIA
        cursor.execute("""
            SELECT id
            FROM vendas
            WHERE id = %s
        """, (id_venda,))

        venda = cursor.fetchone()

        if venda is None:
            print("Venda não encontrada.")

        else:

            # EXCLUIR ITENS
            cursor.execute("""
                DELETE FROM vendas_produtos
                WHERE id_venda = %s
            """, (id_venda,))

            # EXCLUIR VENDA
            cursor.execute("""
                DELETE FROM vendas
                WHERE id = %s
            """, (id_venda,))

            conexao.commit()

            print("\nVenda excluída com sucesso!")

        # =========================
        # LISTAR VENDAS ATUALIZADAS
        # =========================
        print("\n=== VENDAS APÓS EXCLUSÃO ===")

        cursor.execute("""
            SELECT
                v.id,
                ve.nome,
                v.valor_final
            FROM vendas v
            JOIN vendedores ve
                ON v.id_vendedor = ve.id
        """)

        vendas_atualizadas = cursor.fetchall()

        if not vendas_atualizadas:
            print("Nenhuma venda cadastrada.")

        else:

            for venda in vendas_atualizadas:

                id_venda, vendedor, valor_final = venda

                print(
                    f"ID VENDA: {id_venda} | "
                    f"VENDEDOR: {vendedor} | "
                    f"VALOR FINAL: R$ {valor_final:.2f}"
                )

    except ValueError:
        print("Digite um ID válido.")

    except Exception as erro:
        print(f"Erro ao excluir venda: {erro}")

    finally:
        cursor.close()
        conexao.close()
        print("\nConexão encerrada.")


def menu():
    opcoes = {
        "1": ("Criar produto", criar_produto),
        "2": ("Listar produtos", listar_produtos),
        "3": ("Atualizar produto", atualizar_produto),
        "4": ("Excluir produto", excluir_produto),
        "5": ("Criar vendedor", criar_vendedor),
        "6": ("Listar vendedores", listar_vendedores),
        "7": ("Atualizar vendedor", atualizar_vendedor),
        "8": ("Excluir vendedor", excluir_vendedor),
        "9": ("Criar venda com itens", criar_venda_com_itens),
        "10": ("Listar vendas completas", listar_vendas_completas),
        "11": ("Atualizar venda e itens", atualizar_venda_e_itens),
        "12": ("Excluir venda", excluir_venda),
    }

    while True:
        print("\n=== MENU AC4 - CRUD COMPLETO ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Voltar")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Voltando ao menu principal.")
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\nSelecionado: {descricao}")
            funcao()
        else:
            print("Opcao invalida. Tente novamente.")


menu()
