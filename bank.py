from datetime import datetime
import pytz

DAILYWITHDRALLIMIT = 3
DAILYDEPOSITLIMIT = 2
LIMITAMOUNTWITHDRAWAL = 500
MENU = [
    {"id":1,"keyword":"ccl","text":"Criar Cliente"},
    {"id":2,"keyword":"cco","text":"Criar Conta"},
    {"id":3,"keyword":"dep","text":"Depósito"},
    {"id":4,"keyword":"saq","text":"Saque"},
    {"id":5,"keyword":"ext","text":"Extrato"},
    {"id":6,"keyword":"sai","text":"Sair"}
]

bankTransactions = []
totalAmount = 0
processDailyWithdralLimit = DAILYWITHDRALLIMIT
processDailyDeposityLimit = DAILYDEPOSITLIMIT

def init() -> None :
    menu()

def menu() -> None :
    options = "\n".join([
        f"{option.get('keyword')} - {option.get('text')}" for option in MENU
    ])
    menu = f"""\nBank Python:\n\nDigite uma das opções abaixo:\n\n{options}\n\n"""

    while True:

        option = input(menu)

        match option:
            case "dep":
                deposit()
            case "saq":
                withdraw()
            case "ext":
                extract()
            case "sai":
                logoff()
                break
            case _:
                print("""\nOpção inválida. Por favor digite uma das opções disponíveis no menu!\n""")

def deposit() -> None :
    global totalAmount
    global bankTransactions

    while True:
        menu = f"""\nBank Python:\n\nInforme o valor que deseja depositar:\n\n[{MENU[5].get('keyword')}] - Voltar ao menu anterior\n\n"""
        deposit = parse_input(input(menu))

        if (deposit == 0):
            break
        
        if (get_transaction_limit_per_day() == True):
            print(f"""\nBank Python:\n\nLimite de transações excedido limitado a {DAILYDEPOSITLIMIT} por dia. Verifique suas condições em seu extrato e tente novamente!""")
            continue

        if (deposit > 0):
            bankTransactions.append({"type":MENU[1].get('text'),"value":deposit,"date_created":get_date_time()})
            totalAmount += deposit

            print(f"""\nBank Python:\n\nDepósito realizado com sucesso!""")
            continue

        print("""\nOpção inválida. Por favor digite uma das opções disponíveis no menu!\n""")

def withdraw() -> None :
    global totalAmount
    global processDailyWithdralLimit
    global bankTransactions

    while True:    
        menu = f"""\nBank Python:\n\nInforme o valor que deseja sacar:\n\n[{MENU[6].get('keyword')}] - Voltar ao menu anterior\n\n"""
        withdraw = parse_input(input(menu))

        if (withdraw == 0):
            break

        if (withdraw > 0):
            if (processDailyWithdralLimit == 0):
                print(f"""\nBank Python:\n\nLimite diário de saque excedido. Verifique suas condições em seu extrato e tente novamente!""")
                continue

            if (withdraw > LIMITAMOUNTWITHDRAWAL):
                print(f"""\nBank Python:\n\nValor acima do limite permitido de {get_format_currency(LIMITAMOUNTWITHDRAWAL)}. Verifique suas condições em seu extrato e tente novamente!""")
                continue

            if (withdraw > totalAmount):
                print(f"""\nBank Python:\n\nValor indisponível para saque. Verifique o seu extrato e tente novamente!""")
                continue

            bankTransactions.append({"type":MENU[2].get('text'),"value":withdraw,"date_created":get_date_time()})
            processDailyWithdralLimit -= 1
            totalAmount -= withdraw

            print(f"""\nBank Python:\n\nSaque realizado com sucesso!""")
            continue

        print("""\nOpção inválida. Por favor digite uma das opções disponíveis no menu!\n""")

def extract() -> None :
    global bankTransactions

    print(f"""\nBank Python:\n\nSaldo: {get_format_currency(totalAmount)}\nQuantidade de transações por dia: Total {DAILYDEPOSITLIMIT} | Disponível {processDailyDeposityLimit}\nQuantidade diária de saque: Total {DAILYWITHDRALLIMIT} | Disponível {processDailyWithdralLimit}\nValor de saque por transação: {get_format_currency(LIMITAMOUNTWITHDRAWAL)}""")

    bankTransactionsHistory = "\n".join([
        f"{element['date_created']}: {element['type']} de {get_format_currency(element['value'])}" for element in bankTransactions
    ])

    print(f"""\nHistórico de transações:\n\n{bankTransactionsHistory}""")

    while True:
        menu = f"""\nBank Python:\n\n[{MENU[5].get('keyword')}] - Voltar ao menu anterior\n\n"""
        extract = parse_input(input(menu))

        if (extract == 0):
            break

        print("""\nOpção inválida. Por favor digite uma das opções disponíveis no menu!\n""")
        
def parse_input(input: str) -> float | int :
    value = 0
    try:
        value = float(input)
    except ValueError :
        value = -1

    return value

def get_date_time() -> str:
    return datetime.now(pytz.timezone("UTC")).strftime("%Y-%m-%d %H:%M:%S")

def get_format_currency(value) -> str:
    return "R$ {:.2f}".format(value)

def get_transaction_limit_per_day() -> bool:
    global processDailyDeposityLimit
    localProcessDailyDeposityLimit = DAILYDEPOSITLIMIT
    optionDeposity = {}

    for optionsMenu in MENU:
        if (optionsMenu.get('text', '').lower() == "depósito"):
            optionDeposity.update({'type': optionsMenu.get('text', '')})

    actualDatetime = get_date_time()

    for transaction in bankTransactions:
        
        if (transaction.get('type') != optionDeposity.get('type')):
            continue
        
        if (datetime.strptime(actualDatetime, "%Y-%m-%d %H:%M:%S") - datetime.strptime(transaction.get('date_created'), "%Y-%m-%d %H:%M:%S")).days == 0:
            localProcessDailyDeposityLimit -= 1

    processDailyDeposityLimit = localProcessDailyDeposityLimit
    return True if processDailyDeposityLimit < 1 else False
            
def logoff() -> None :
    print("\nObrigado e volte sempre que precisar!\n\n")

if __name__ == '__main__':
    init()
