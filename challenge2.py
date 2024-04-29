import textwrap
import re


def menu():
    menu = """\n
    Selecione a operação que deseja a seguir:
    [c]\tConsultar saldo
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo usuário
    [nc]\tNova conta
    [lc]\tListar contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def consultar(saldo):
    return print(f"Saldo: R$ {saldo:.2f}")


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n=== Operação falhou! O valor informado é inválido. ===")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n=== Operação falhou! Você não tem saldo suficiente. ===")

    elif excedeu_limite:
        print("\n=== Operação falhou! O valor do saque excede o limite. ===")

    elif excedeu_saques:
        print("\n=== Operação falhou! Número máximo de saques excedido. ===")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n=== Operação falhou! O valor informado é inválido. ===")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf_padrao = re.compile(r"^([0-9]{3}[.]?[0-9]{3}[.]?[0-9]{3}[-]?[0-9]{2})$")
    cpf = input("Informe o CPF (somente número): ")
    
    if re.match(cpf_padrao, cpf):
        usuario = filtrar_usuario(cpf, usuarios)
    else:
        print("\n=== CPF inválido! ===")
        return

    if usuario:
        print("\n=== Já existe usuário com esse CPF! ===")
        return

    nome = input("Informe o nome completo: ")
    data_padrao = re.compile(r"(^(((0[1-9]|1[0-9]|2[0-8])[\/](0[1-9]|1[012]))|((29|30|31)[\/](0[13578]|1[02]))|((29|30)[\/](0[4,6,9]|11)))[\/](19|[2-9][0-9])\d\d$)|(^29[\/]02[\/](19|[2-9][0-9])(00|04|08|12|16|20|24|28|32|36|40|44|48|52|56|60|64|68|72|76|80|84|88|92|96)$)")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    
    if re.match(data_padrao, data_nascimento):
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
        print("\n=== Usuário criado com sucesso! ===")
    else:
        print("\n=== Data de nascimento inválida! ===")
        return
    

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n=== Usuário não encontrado, fluxo de criação de conta encerrado! ===")


def listar_contas(contas):
    if contas:
        for conta in contas:
            linha = f"""\
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))
    else:
        print("\n=== Não existem contas cadastradas! ===")

    
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        
        if opcao == "c":
            consultar(saldo)

        elif opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
    