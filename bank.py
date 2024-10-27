import datetime

DAILYWITHDRALLIMIT = 3
LIMITAMOUNTWITHDRAWAL = 500
MENU = [[0,"Sair"],[1,"Depósito"],[2,"Saque"],[3,"Extrato"]]

bankTransactions = []
totalAmount = 0
processDailyWithdralLimit = DAILYWITHDRALLIMIT;

def init() -> None :
    menu()

def menu() -> None :
    menu = f"""\nBank Python:\n\nDigite uma das opções abaixo:\n\n{MENU[1][0]} - {MENU[1][1]}\n{MENU[2][0]} - {MENU[2][1]}\n{MENU[3][0]} - {MENU[3][1]}\n{MENU[0][0]} - {MENU[0][1]}\n\n"""

    while True:

        option = input(menu)

        match option:
            case "1":
                deposit()
            case "2":
                withdraw()
            case "3":
                extract()
            case "0":
                logoff()
                break;
            case _:
                print("""\nOpção inválida. Por favor digite uma das opções disponíveis no menu!\n""")

def deposit() -> None :
    global totalAmount
    global bankTransactions

    while True:
        menu = f"""\nBank Python:\n\nInforme o valor que deseja depositar:\n\n[{MENU[0][0]}] - Voltar ao menu anterior\n\n"""
        deposit = parseInput(input(menu))

        if (deposit == 0):
            break;

        if (deposit > 0):
            bankTransactions.append([MENU[1][1], deposit,  getDatetime()])
            totalAmount += deposit

            print(f"""\nBank Python:\n\nDepósito realizado com sucesso!""")
            continue

        print("""\nOpção inválida. Por favor digite uma das opções disponíveis no menu!\n""")

def withdraw() -> None :
    global totalAmount
    global processDailyWithdralLimit
    global bankTransactions

    while True:    
        menu = f"""\nBank Python:\n\nInforme o valor que deseja sacar:\n\n[{MENU[0][0]}] - Voltar ao menu anterior\n\n"""
        withdraw = parseInput(input(menu))

        if (withdraw == 0):
            break;

        if (withdraw > 0):
            if (processDailyWithdralLimit == 0):
                print(f"""\nBank Python:\n\nLimite diário de saque excedido. Verifique suas condições em seu extrato e tente novamente!""")
                continue

            if (withdraw > LIMITAMOUNTWITHDRAWAL):
                print(f"""\nBank Python:\n\nValor acima do limite permitido de {getFormatCurrency(LIMITAMOUNTWITHDRAWAL)}. Verifique suas condições em seu extrato e tente novamente!""")
                continue

            if (withdraw > totalAmount):
                print(f"""\nBank Python:\n\nValor indisponível para saque. Verifique o seu extrato e tente novamente!""")
                continue

            bankTransactions.append([MENU[2][1], withdraw, getDatetime()])
            processDailyWithdralLimit -= 1
            totalAmount -= withdraw

            print(f"""\nBank Python:\n\nSaque realizado com sucesso!""")
            continue

        print("""\nOpção inválida. Por favor digite uma das opções disponíveis no menu!\n""")

def extract() -> None :
    global bankTransactions

    print(f"""\nBank Python:\n\nSaldo: {getFormatCurrency(totalAmount)}\nLimite de quantidade diário de saque: Total {DAILYWITHDRALLIMIT} | Utilizado {DAILYWITHDRALLIMIT-processDailyWithdralLimit}\nValor de saque por transação: {getFormatCurrency(LIMITAMOUNTWITHDRAWAL)}""")

    bankTransactionsHistory = "\n".join([
        f"{element[2]}: {element[0]} de {getFormatCurrency(element[1])}" for element in bankTransactions
    ])

    print(f"""\nHistórico de transações:\n\n{bankTransactionsHistory}""")

    while True:
        menu = f"""\nBank Python:\n\n[{MENU[0][0]}] - Voltar ao menu anterior\n\n"""
        extract = parseInput(input(menu))

        if (extract == 0):
            break;    

        print("""\nOpção inválida. Por favor digite uma das opções disponíveis no menu!\n""")
        
def parseInput(input: str) -> float | int :
    value = 0
    try:
        value = float(input)
    except ValueError :
        value = -1

    return value

def getDatetime() -> str:
    actualDatetime = datetime.datetime.now()

    return actualDatetime.strftime("%Y-%m-%d %H-%M-%S")

def getFormatCurrency(value) -> str:
    return "R$ {:.2f}".format(value)

def logoff() -> None :
    print("\nObrigado e volte sempre que precisar!\n\n")

if __name__ == '__main__':
    init()
