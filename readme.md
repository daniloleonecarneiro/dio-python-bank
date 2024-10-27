# Sistema de Banco Simples

Desenvolvido por **Danilo Leone**

Este projeto implementa um sistema de banco simples em Python, capaz de realizar operações de depósito, saque e extrato, conforme as regras estabelecidas abaixo.

## Funcionalidades

### 1. Depósito
- Permite depositar qualquer valor sem limites.
- O valor do depósito é adicionado ao saldo da conta.

### 2. Saque
- Limite de saques diários: até **3 saques por dia**.
- Limite de valor para cada saque: até **500 reais**.
- Em caso de saldo insuficiente, exibe uma mensagem informando que a operação não pode ser concluída por falta de saldo.

### 3. Extrato
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