# Controle de Despesas Pessoais

Aplicação de linha de comando para registro e análise de despesas pessoais, feita em Python com persistência em SQLite.

## Funcionalidades

- Cadastro, edição, remoção e consulta de despesas
- Filtros por categoria e por período
- Relatórios agregados:
  - Total gasto por categoria
  - Total gasto por mês
  - Resumo geral (soma, média, maior e menor despesa)
  - Ranking das maiores despesas
- Categorias pré-cadastradas (Alimentação, Transporte, Moradia, Saúde, Lazer, Educação, Outros)

## Estrutura do projeto

```
finance_tracker/
├── main.py                 # ponto de entrada
├── src/
│   ├── database.py         # conexão e criação do schema (SQLite)
│   ├── models.py           # entidades e validações
│   ├── repository.py       # operações de acesso a dados (CRUD)
│   ├── services.py         # regras de negócio e agregações
│   └── cli.py               # interface de linha de comando
├── tests/
│   └── test_despesas.py
├── requirements.txt
└── README.md
```

A separação segue o padrão repository/service: `repository.py` lida apenas com SQL, `services.py` concentra validações e regras de negócio, e `cli.py` cuida só da interação com o usuário. O banco (`data/finance.db`) é criado automaticamente na primeira execução.

## Como rodar

```bash
python3 main.py
```

Não há dependências externas — o projeto usa apenas a biblioteca padrão do Python (`sqlite3`, `dataclasses`, `pathlib`).

## Rodando os testes

```bash
python3 -m unittest tests/test_despesas.py -v
```

## Banco de dados

O schema tem duas tabelas principais:

- `categorias (id, nome)`
- `despesas (id, descricao, valor, data, categoria_id)` com chave estrangeira para `categorias`

Índices em `data` e `categoria_id` para acelerar consultas e relatórios.

## Possíveis melhorias futuras

- Exportação de relatórios para CSV/PDF
- Suporte a receitas além de despesas (fluxo de caixa completo)
- Interface web (Flask/FastAPI) reaproveitando a camada `services`
- Metas de gastos mensais por categoria
