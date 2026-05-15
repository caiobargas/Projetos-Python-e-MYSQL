saldo = 0.0
extrato = []


def adicionarDinheiro():
    global saldo
    valor = float(input("Digite o valor do déposito R$: "))

    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print(f"Depósito de realizado com sucesso!")
        print(f"Saldo atual: R$ {saldo:.2f}")
    else:
        print("Valor inválido. O valor do depósito deve ser positivo.")


def sacarDinheiro():
    global saldo, extrato
    valor = float(input("Digite o valor do saque R$: "))

    if valor > 0:
        if saldo >= valor:
            saldo -= valor
            extrato.append(f"Saque: R$ {valor:.2f}")
            print("Saque realizado com sucesso!")
            print(f"Saldo atual: R$ {saldo:.2f}")
        else:
            print("Saldo insuficiente para realizar o saque.")
    else:
        print("Valor inválido! O valor deve ser positivo.")


def mostrarExtrato():
    print("\n===== EXTRATO =====")
    if not extrato:
        print("Nenhuma transação realizada.")
    else:
        for operacao in extrato:
            print(operacao)
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("==================")


while True:
    print("\n==== MENU ====")
    print("1. Adicionar dinheiro")
    print("2. Sacar dinheiro")
    print("3. Mostrar extrato")
    print("4. Sair")
    print("Escolha uma opção: ", end="")

    opcao = input()

    if opcao == "1":
        adicionarDinheiro()
    elif opcao == "2":
        sacarDinheiro()
    elif opcao == "3":
        mostrarExtrato()
    elif opcao == "4":
        print("Saindo do programa. Obrigado por usar nosso serviço!")
        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
