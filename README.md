# 📋 Gerenciador de Tarefas

## 📝 Descrição

Este projeto implementa um sistema completo de gerenciamento de tarefas em Python, desenvolvido como exercício integrador de Programação Orientada a Objetos. O sistema utiliza conceitos avançados de Python como Enums, descritores, dataclasses, polimorfismo e persistência de dados.

## ✨ Funcionalidades

- ✅ **Gerenciamento Completo de Tarefas**: Adicione, liste, marque como concluída ou reabra tarefas
- 🎯 **Sistema de Prioridades**: Organize tarefas por prioridade (BAIXA, MÉDIA, ALTA)
- 📅 **Validação de Datas**: Impede a criação de tarefas com datas no passado
- 🔍 **Múltiplos Filtros**: Liste tarefas por prioridade, prazo, status de conclusão
- 💾 **Persistência de Dados**: Salve e carregue dados em formatos CSV e JSON
- 🖥️ **Interface CLI Intuitiva**: Menu interativo para facilitar o uso
- ✏️ **Validação Robusta**: Sistema de validação para nomes e datas

## 🛠️ Tecnologias e Conceitos Utilizados

### Conceitos de POO Implementados:
- **Enum com Propriedades**: Sistema de prioridades com pesos para ordenação
- **Descritores**: Validação automática de dados (strings não vazias, datas não passadas)
- **Dataclasses com InitVar**: Estrutura de dados eficiente com validação integrada
- **Polimorfismo**: Representações customizadas com `__str__`
- **Type Hints**: Código mais legível e menos propenso a erros

### Bibliotecas Utilizadas:
```python
import enum
import datetime
from dataclasses import dataclass, InitVar
from typing import ClassVar
import json
import csv
import sys
import os
import time
```

## 📁 Estrutura do Projeto

```
gerenciador_tarefas/
├── gerenciador_tarefas.py      # Código principal do sistema
├── tarefas.csv                 # Arquivo de dados CSV
├── tarefas.json                # Arquivo de dados JSON
├── README.md                   # Documentação do projeto
└── Exercício Integrador — Gerenciador de Tarefas.txt  # Especificações do exercício
```

## 🚀 Como Usar

### Pré-requisitos
- Python 3.7+ instalado no sistema

### Executando o Sistema

1. **Clone ou baixe o projeto**
2. **Navegue até o diretório do projeto**
3. **Execute o programa:**
   ```bash
   python gerenciador_tarefas.py
   ```

### Menu Principal

```
-----------------------------------------------------------------------------------------------
                           GERENCIADOR DE TAREFAS
-----------------------------------------------------------------------------------------------
MENU PRINCIPAL:

1  - Carregar CSV
2  - Carregar JSON
3  - Salvar CSV
4  - Salvar JSON
5  - Adicionar tarefa
6  - Listar tarefas concluídas
7  - Listar tarefas não concluídas
8  - Listar por prioridade
9  - Listar por prazo
10 - Marcar tarefa como concluída
11 - Reabrir tarefa
0  - Sair
```

### Exemplo de Uso

```
Escolha uma opção: 5
Nome da tarefa: Preparar slides
Prazo (YYYY-MM-DD ou DD/MM/YYYY): 25/09/2025
Prioridade (ALTA/MEDIA/BAIXA) [padrão MEDIA]: ALTA
Já concluída? (s/N): n
Tarefa adicionada com sucesso!
Ordenado por prioridade:
 1. [ALTA] 2025-09-25  Preparar slides  (concluída: ✗)
```

## 🎯 Funcionalidades Detalhadas

### 1. Adicionar Tarefas
- **Nome**: String obrigatória (não pode ser vazia)
- **Prazo**: Data no formato YYYY-MM-DD ou DD/MM/YYYY (não pode ser no passado)
- **Prioridade**: BAIXA, MÉDIA ou ALTA (padrão: MÉDIA)
- **Status**: Concluída ou não (padrão: não concluída)

### 2. Listagem de Tarefas
- **Por Prioridade**: Ordena por peso da prioridade (ALTA → MÉDIA → BAIXA)
- **Por Prazo**: Ordena por data de vencimento
- **Filtros**: Incluir/excluir tarefas concluídas
- **Numeração**: Opção de enumerar tarefas para facilitar operações

### 3. Gerenciamento de Status
- **Marcar como Concluída**: Alterar status de uma tarefa específica
- **Reabrir Tarefa**: Marcar tarefa concluída como pendente novamente

### 4. Persistência de Dados
- **Formato CSV**: Compatível com planilhas (Excel, Calc, etc.)
- **Formato JSON**: Estruturado e legível para humanos
- **Auto-detecção**: Sistema detecta e carrega dados existentes

## 🔧 Arquitetura do Sistema

### Classes Principais

#### `Prioridade` (Enum)
```python
class Prioridade(Enum):
    BAIXA = auto()    # peso: 1
    MEDIA = auto()    # peso: 2
    ALTA = auto()     # peso: 3
```

#### `Tarefa` (Dataclass)
- Utiliza descritores para validação automática
- InitVar para processamento no `__post_init__`
- Representação formatada com `__str__`

#### `GerenciadorTarefas`
- Gerencia coleção de tarefas
- Métodos para CRUD completo
- Sistema de persistência integrado

### Descritores de Validação

#### `NaoVazio`
- Valida strings obrigatórias
- Rejeita strings vazias ou apenas espaços

#### `DataNaoPassada`
- Valida objetos `datetime.date`
- Impede datas no passado (aceita hoje)

## 📊 Formatos de Dados

### CSV
```csv
nome,prazo,prioridade,concluida
Preparar slides,2025-09-25,ALTA,False
Revisar código,2025-09-30,MEDIA,True
```

### JSON
```json
[
    {
        "nome": "Preparar slides",
        "prazo": "2025-09-25",
        "prioridade": "ALTA",
        "concluida": false
    }
]
```

## 🎨 Representação Visual

As tarefas são exibidas no formato:
```
[PRIORIDADE] YYYY-MM-DD  Nome da tarefa  (concluída: ✓/✗)
```

Exemplos:
- `[ALTA] 2025-09-25  Preparar slides  (concluída: ✗)`
- `[MÉDIA] 2025-09-30  Revisar código  (concluída: ✓)`

## ⚠️ Tratamento de Erros

O sistema inclui tratamento robusto para:
- Datas em formato inválido
- Prioridades não reconhecidas
- Índices de tarefas inválidos
- Arquivos corrompidos ou inexistentes
- Entradas vazias ou inválidas

## 🔄 Formatos de Data Aceitos

- **ISO 8601**: `YYYY-MM-DD` (ex: 2025-09-25)
- **Brasileiro**: `DD/MM/YYYY` (ex: 25/09/2025)

## 📈 Possíveis Melhorias

- [ ] Interface gráfica (GUI)
- [ ] Busca e filtros avançados
- [ ] Categorias/tags para tarefas
- [ ] Notificações de prazo
- [ ] Backup automático
- [ ] Integração com APIs externas
- [ ] Relatórios e estatísticas

## 👨‍💻 Desenvolvimento

Este projeto foi desenvolvido como exercício integrador para demonstrar conhecimentos em:
- Programação Orientada a Objetos
- Design Patterns (Descriptor Pattern)
- Manipulação de arquivos
- Validação de dados
- Interface de usuário em terminal

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte do curso de Residência em Robótica e IA - CIn/Softex.

---

**Desenvolvido com ❤️ usando Python**