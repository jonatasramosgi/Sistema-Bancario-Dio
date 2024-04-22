menu = """

Selecione a operação que deseja a seguir:

[c] Consultar saldo
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)
    
    if opcao == "c":
        print(f"\nSaldo: R$ {saldo:.2f}")

    elif opcao == "d":
        while True:
            valor = float(input("\nInforme o valor do depósito: "))

            if valor > 0:
                saldo += valor
                extrato += f"Depósito: R$ {valor:.2f}\n"
                break

            else:
                print("\nOperação falhou! O valor informado é inválido.")

    elif opcao == "s":
        while True:
            valor = float(input("\nInforme o valor do saque: "))

            excedeu_saldo = valor > saldo

            excedeu_limite = valor > limite

            excedeu_saques = numero_saques >= LIMITE_SAQUES

            if excedeu_saldo:
                print("\nOperação falhou! Você não tem saldo suficiente.")
                break

            elif excedeu_limite:
                print("\nOperação falhou! O valor do saque excede o limite.")

            elif excedeu_saques:
                print("\nOperação falhou! Número máximo de saques excedido.")
                break

            elif valor > 0:
                saldo -= valor
                extrato += f"Saque: R$ {valor:.2f}\n"
                numero_saques += 1
                break

            else:
                print("\nOperação falhou! O valor informado é inválido.")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações.\n" if not extrato else extrato)
        print(f"Saldo: R$ {saldo:.2f}")
        print("=========================================")

    elif opcao == "q":
        break

    else:
        print("\nOperação inválida, por favor selecione novamente a operação desejada.")