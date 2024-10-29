from datetime import datetime
import pytz
import re

DAILYWITHDRALLIMIT = 3
DAILYDEPOSITLIMIT = 2
LIMITAMOUNTWITHDRAWAL = 500
MENU = [
    {"id":1,"keyword":"ccl","text":"Criar Cliente"},
    {"id":2,"keyword":"lcl","text":"Listar Clientes"},
    {"id":3,"keyword":"cco","text":"Criar Conta"},
    {"id":4,"keyword":"lco","text":"Listar Contas"},
    {"id":5,"keyword":"dep","text":"Depósito"},
    {"id":6,"keyword":"saq","text":"Saque"},
    {"id":7,"keyword":"ext","text":"Extrato"},
    {"id":8,"keyword":"sai","text":"Sair"}
]

DATA_CLIENT = [
    {"attribute":"name","label":"Nome","value":""},
    {"attribute":"date_of_birthday","label":"Data de Nascimento","value":""},
    {"attribute":"cpf","label":"CPF","value":""},
    {"attribute":"address","label":"Endereço","children": [
            {"attribute":"publicplace","label":"Logradouro","value":""},
            {"attribute":"number","label":"Nro","value":""},
            {"attribute":"neighborhood","label":"Bairro","value":""},
            {"attribute":"city","label":"Cidade","value":""},
            {"attribute":"state_acronym","label":"Sigla do Estado","value":""}
        ]
    }
]

DATA_BANK_ACCOUNT = [
    {"attribute":"agency","label":"Agência","value":"0001"}
]

clients = []
accounts = []
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
    
    while True:

        option = input(f"\nBank Python:\n\nDigite uma das opções abaixo:\n\n{options}\n\n")

        match option:
            case "ccl":
                create_client()
            case "lcl":
                list_clients()
            case "cco":
                create_account()
            case "lco":
                list_accounts()
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
                print("\nOpção inválida. Por favor digite uma das opções disponíveis no menu!\n")

def create_client() -> None:
    print(f"\nBank Python:\n\nInforme os dados solicitados do cliente:\n\n[{MENU[7].get('keyword')}] - Voltar ao menu anterior\n")
    
    global clients
    client = {};

    breakFor = False
    for attribute in DATA_CLIENT:
        if (breakFor == True):
            break

        if ("children" not in attribute):
            while True:
                data = input(f"\nDigite o {attribute['label']}: \n").strip()

                if (data == MENU[7].get('keyword')):
                    breakFor = True
                    break;
                
                if (attribute["attribute"] == "cpf"):
                    data = re.sub('[^0-9]+', '', data)
                    lenCpf = len(data)
                    if (lenCpf < 11 or lenCpf > 11):
                        print(f"CPF inválido. Verifique os dados e tente novamente!")
                        continue
                    
                    checkExistsCpf = any(data in client.values() for client in clients)

                    if (checkExistsCpf == True):
                        print(f"\nCPF já vinculado a outro cliente. Verifique os dados e tente novamente!")
                        continue

                client[attribute['attribute']] = data
                break
        else:
            print(f"\nDados do {attribute['label']}")
            address = {}
            for children in attribute['children']:
                data = input(f"\nDigite o {children['label']}: \n").strip()

                if (data == MENU[7].get('keyword')):
                    breakFor = True
                    break;
                
                address[children['attribute']] = data
            
            client[attribute["attribute"]] = address

    client['id'] = len(clients) + 1
    
    print(f"\nBank Python:\n\nCliente [ID: {client['id']} | Nome: {client['name']}] registrado com sucesso!")

    clients.append(client)

def list_clients() -> None :
    print(f"\nBank Python:\n\nClientes:\n")

    for client in clients:
        print(f"########################## {client['id']} ##########################")
        for attribute in DATA_CLIENT:
            value = client[attribute['attribute']];
            value = ",".join(value.values()) if isinstance(value, dict) else value
            print(f"{attribute['label']}: {value}")

def create_account() -> None:
    print(f"\nBank Python:\n\nInforme os dados solicitados da conta bancária:\n\n[{MENU[7].get('keyword')}] - Voltar ao menu anterior\n")

    global accounts
    global clients

    newAccount = {}

    for attribute in DATA_BANK_ACCOUNT:
        if (len(attribute['value']) > 0):
            newAccount[attribute['attribute']] = attribute['value']
            continue

        data = input(f"\nDigite o {attribute['label']}: \n").strip()

        if (data == MENU[7].get('keyword')):
            break
    
    while True:
        search = input(f"\nNome e/ou parte do nome do cliente ou CPF do cliente:\n").strip().lower()

        if (search == MENU[7].get('keyword')):
            break
        
        filteredClients = [
            client
            for client in clients
            if search in client["name"] or search in client["cpf"]
        ]

        if (len(filteredClients) == 0):
            print(f"\nClient não localizado. Tente novamente")
            continue

        print(f"\nVeja a lista de clientes encontrados com base na busca: {search}\n")
        listClients = "\n".join([
            f"ID: {client.get('id')} | CPF: {client.get('cpf')} | Nome: {client.get('name')}\n" for client in filteredClients
        ])
        print(listClients)

        idClient = input(f"\nDigite o ID do cliente para vincular a conta:\n\n[{MENU[7].get('keyword')}] - Voltar ao menu anterior\n").strip()

        if (idClient == MENU[7].get('keyword')):
            break

        filteredClient = [
            client
            for client in filteredClients
            if int(idClient) == client["id"]
        ]

        if (len(filteredClient) == 0):
            print(f"\nClient não localizado. Tente novamente")
            continue

        client = filteredClient[0]

        countAccounts = sum(len(account['accounts']) for account in accounts)
        newAccount['account_number'] = countAccounts + 1

        created = False
        for account in accounts:
            if account["cpf"] == client['cpf']:
                account["accounts"].append(newAccount)
                created = True
                break

        if (created == False):
            accounts.append({"cpf": client['cpf'], "accounts": [newAccount]})     

        print(f"\nBank Python:\n\nConta cadastrada e vinculada com sucesso [Cliente: {client['cpf']} | Agência: {newAccount['agency']} | Conta: {newAccount['account_number']}] registrado com sucesso!")
        break

def list_accounts() -> None:
    print(f"\nBank Python:\n\Contas:\n")

    for account in accounts:
        print(f"########################## {account['cpf']} ##########################")
        for item in account['accounts']:
            print(f"Agência: {item['agency']}")
            print(f"Número da Conta: {item['account_number']}")
            print("\n")

def deposit() -> None :
    global totalAmount
    global bankTransactions

    while True:
        deposit = input(f"\nBank Python:\n\nInforme o valor que deseja depositar:\n\n[{MENU[7].get('keyword')}] - Voltar ao menu anterior\n\n").strip()

        if (deposit == MENU[7].get('keyword')):
            break;
        
        deposit = parse_input(deposit);

        if (deposit == 0):
            break
        
        if (get_transaction_limit_per_day() == True):
            print(f"\nBank Python:\n\nLimite de transações excedido limitado a {DAILYDEPOSITLIMIT} por dia. Verifique suas condições em seu extrato e tente novamente!")
            continue

        if (deposit > 0):
            bankTransactions.append({"type":MENU[1].get('text'),"value":deposit,"date_created":get_date_time()})
            totalAmount += deposit

            print(f"\nBank Python:\n\nDepósito realizado com sucesso!")
            continue

        print("\nOpção inválida. Por favor digite uma das opções disponíveis no menu!\n")

def withdraw() -> None :
    global totalAmount
    global processDailyWithdralLimit
    global bankTransactions

    while True:    
        withdraw = input(f"\nBank Python:\n\nInforme o valor que deseja sacar:\n\n[{MENU[6].get('keyword')}] - Voltar ao menu anterior\n\n").strip()

        if (withdraw == MENU[7].get('keyword')):
            break;
        
        withdraw = parse_input(withdraw)

        if (withdraw > 0):
            if (processDailyWithdralLimit == 0):
                print(f"\nBank Python:\n\nLimite diário de saque excedido. Verifique suas condições em seu extrato e tente novamente!")
                continue

            if (withdraw > LIMITAMOUNTWITHDRAWAL):
                print(f"\nBank Python:\n\nValor acima do limite permitido de {get_format_currency(LIMITAMOUNTWITHDRAWAL)}. Verifique suas condições em seu extrato e tente novamente!")
                continue

            if (withdraw > totalAmount):
                print(f"\nBank Python:\n\nValor indisponível para saque. Verifique o seu extrato e tente novamente!")
                continue

            bankTransactions.append({"type":MENU[2].get('text'),"value":withdraw,"date_created":get_date_time()})
            processDailyWithdralLimit -= 1
            totalAmount -= withdraw

            print(f"\nBank Python:\n\nSaque realizado com sucesso!")
            continue

        print("\nOpção inválida. Por favor digite uma das opções disponíveis no menu!\n")

def extract() -> None :
    global bankTransactions

    print(f"\nBank Python:\n\nSaldo: {get_format_currency(totalAmount)}\nQuantidade de transações por dia: Total {DAILYDEPOSITLIMIT} | Disponível {processDailyDeposityLimit}\nQuantidade diária de saque: Total {DAILYWITHDRALLIMIT} | Disponível {processDailyWithdralLimit}\nValor de saque por transação: {get_format_currency(LIMITAMOUNTWITHDRAWAL)}")

    bankTransactionsHistory = "\n".join([
        f"{element['date_created']}: {element['type']} de {get_format_currency(element['value'])}" for element in bankTransactions
    ])

    print(f"\nHistórico de transações:\n\n{bankTransactionsHistory}")

    while True:
        extract = parse_input(input(f"\nBank Python:\n\n[{MENU[7].get('keyword')}] - Voltar ao menu anterior\n\n"))

        if (extract == 0):
            break

        print("\nOpção inválida. Por favor digite uma das opções disponíveis no menu!\n")
        
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

def get_transaction_limit_per_day() -> list:
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
