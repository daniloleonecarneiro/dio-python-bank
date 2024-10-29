# Sistema de Banco Simples

Desenvolvido por **Danilo Leone**

Este projeto implementa um sistema de banco simples em Python, capaz de realizar operações de depósito, saque e extrato, conforme as regras estabelecidas abaixo.

## Funcionalidades

### 1. Criar Cliente
- Permite criar um cliente

### 2. Criar Conta
- Cria uma nova conta bancária associada a um cliente.
- As contas estão vinculadas a um cliente e são identificadas por um número único de conta.

### 3. Listar Clientes
- Exibe uma lista de todos os clientes cadastrados, mostrando informações como nome e CPF.

### 4. Listar Contas
- Exibe uma lista de todas as contas criadas, mostrando o número da conta e o saldo atual.

### 5. Depósito
- Permite depositar qualquer valor sem limites.
- O valor do depósito é adicionado ao saldo da conta.
- Registra a transação no extrato com a data e hora do depósito.

### 6. Saque
- Limite de saques diários: até **3 saques por dia**.
- Limite de valor para cada saque: até **500 reais**.
- Em caso de saldo insuficiente, exibe uma mensagem informando que a operação não pode ser concluída por falta de saldo.
- Registra a transação no extrato com a data e hora do saque.

### 7. Extrato
- Lista todas as operações de depósito e saque realizadas na conta, exibindo:
  - Valor e tipo de cada operação.
  - Data e hora em que cada operação foi realizada.

## Regras do Sistema

1. **Depósitos**: Não há limite de valor para depósitos.
2. **Saques**:
   - Limite de 3 saques por dia.
   - Valor máximo de cada saque é de 500 reais.
   - Não é permitido saque com saldo insuficiente.
3. **Extrato**: Exibe o histórico completo das operações realizadas.

## Considerações

Este sistema de banco simples foi desenvolvido com foco em funcionalidades básicas para demonstrar operações bancárias essenciais. 