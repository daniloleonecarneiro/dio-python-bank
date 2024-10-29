from datetime import datetime
import pytz
import re
from abc import ABC, abstractmethod

class Pessoa():
    def __init_(self, nome) -> None:
        self._nome = nome

class Conta():
    def __init_(self, numero, cliente) -> None:
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self) -> float:
        return self._saldo;
    
    @property
    def numero(self) -> str:
        return self._numero;

    @property
    def agencia(self) -> str:
        return self._agencia;

    @property
    def cliente(self) -> str:
        return self._cliente;

    @property
    def historico(self) -> list:
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: str) -> Conta:
        return cls(cliente, numero)
    
    def sacar(self, valor: float) -> bool:
        if (valor > self.saldo):
            print(f"\nBank Python:\n\nValor indisponível para saque. Verifique o seu extrato e Tente novamente!")
            return False

        if (valor <= 0):
            print(f"\nBank Python:\n\nValor não é válido para saque. Tente novamente!")
            return False

        self.saldo -= valor
        print(f"\nBank Python:\n\nSaque realizado com sucesso!")

        return True

    def depositar(self, valor: float) -> bool:
        if (valor <= 0):
            print(f"\nBank Python:\n\nValor não é válido para depósito. Tente novamente!")
            return False
        
        self.saldo += valor

        print(f"\nBank Python:\n\nDepósito realizado com sucesso!")
        
class Cliente(Pessoa):
    def __init_(self, nome, endereco) -> None:
        self._endereco = endereco
        self._contas = []
        super().__init__(nome)

    @property
    def endereco(self) -> dict:
        return self._endereco
    
    def adcicionar_conta(self, conta: Conta) -> None:
        self.contas.append(conta)
    
    def realizar_transacao(self, conta: Conta, transacao: Transacao) -> None:
        transacao.registrar(conta)
     
class ContaCorrent(Conta):
    def __init_(self, numero, cliente, limite=500, limite_saques=3) -> None:
        self._limite = limite
        self._limite_saques = limite_saques
        super().__init__(numero, cliente)
    
    @property
    def limite(self) -> int:
        return self._limit

    @property
    def limite_saques(self) -> int:
        return self._limit_saques
    
    def sacar(self, valor: float) -> bool:
        saques = len(
            [
                transacao for transacao in self.historico.transacao
                if transacao.get("tipo") == Saque.__name__
            ]
        )

        if (saques == self.limite_saques):
            print(f"\nBank Python:\n\nLimite diário de saque excedido. Verifique as condições em sua conta e tente novamente!")
            return False

        if (valor > self.limite):
            print(f"\nBank Python:\n\nValor acima do limite permitido de {self.limite}. Verifique as condições em sua conta e tente novamente!")
            return False

        super().sacar(valor)

        return True
    
    def depositar(self, valor: float) -> bool:
        if (valor <= 0):
            print(f"\nBank Python:\n\nValor não é válido para depósito. Tente novamente!")
            return False
        
        self.saldo += valor

        print(f"\nBank Python:\n\nDepósito realizado com sucesso!")

class Historico():
    def __init__(self):
        self._transacao = []

    @property
    def transacao(self) -> list:
        return self._transacao
    
    def adiciona_transacao(self, instanciaTransacao: Transacao) -> None:
        self.transacao.append(
            {
                "tipo": instanciaTransacao.__class__.__name__,
                "valor": instanciaTransacao.valor,
                "data": instanciaTransacao.now().strftime("%Y-m-d %H:%M:%s")
            }
        )
    
class PessoaFisica(Cliente):
    def __init(self, nome, cpf, data_nascimento, endereco):
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        super().__init__(nome=nome, endereco=endereco)

    @property
    def cpf(self) -> int:
        return self._cpf;
    
    @property
    def data_nascimento(self) -> str:
        return self._data_nascimento;

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta: Conta) -> Saque | Deposito:
        pass

    @property
    def valor(self) -> float:
        pass

class Saque(Transacao):
    def __init__(self, valor=None):
        self._valor = valor

    @property
    def valor(self):
        return self.valor;

    def registrar(self, conta: Conta) -> None:
        transacao = conta.sacar(self.valor)

        if (transacao):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor=None):
        self._valor = valor

    @property
    def valor(self):
        return self.valor;

    def registrar(self, conta: Conta) -> None:
        transacao = conta.depositar(self.valor)

        if (transacao):
            conta.historico.adicionar_transacao(self)