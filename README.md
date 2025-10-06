# 🏗️ Projeto de Data Warehouse AdventureWorks

Este projeto tem como objetivo construir um **Data Warehouse (DW)** baseado no conjunto de dados do **AdventureWorks**, aplicando conceitos de **modelagem multidimensional**, **ETL em Python** e **análise de indicadores (KPIs)**.

---

## 🧩 Estrutura do Projeto

```
📂 adventureworks_dw_etl/
│
├── etl.py                         # Script principal da ETL
├── config.py                      # Configuração de conexões (SQL Server e PostgreSQL)
├── requirements.txt               # Dependências do projeto
├── dashboard.ipynb                # (Opcional) Notebook com análise dos indicadores
├── modelo_multidimensional.png    # Diagrama estrela do modelo do DW
├── README.md                      # Documentação do projeto
└── /data                          # (opcional) Dados intermediários/exportados
```

---

## ⚙️ Tecnologias Utilizadas

- **Python 3.10+**  
- **Pandas**  
- **SQLAlchemy**  
- **PyODBC**  
- **Psycopg2**  
- **PostgreSQL 15**  
- **SQL Server 2022 (AdventureWorks2022)**  

---

## 🧱 Modelo Multidimensional

O modelo segue um **esquema estrela**, com a tabela fato principal `fato_vendas` conectada às dimensões:

**Fato Principal**
- `fato_vendas`

**Dimensões**
- `dim_cliente`
- `dim_produto`
- `dim_pessoa`
- `dim_territorio`
- `dim_data`

![Modelo Multidimensional](modelo_multidimensional.png)

---

## 📊 Indicadores (KPIs)

| # | Indicador | Descrição |
|---|------------|-----------|
| 1 | Total de Vendas | Soma total de vendas realizadas |
| 2 | Quantidade de Pedidos | Número de pedidos efetuados |
| 3 | Lucro Total | Receita líquida após custos |
| 4 | Ticket Médio | Valor médio por pedido |
| 5 | Quantidade de Itens Vendidos | Total de produtos vendidos |
| 6 | Vendas por Categoria | Faturamento agrupado por categoria |
| 7 | Vendas por Território | Análise de vendas por região |
| 8 | Cancelamentos | Quantidade e valor de pedidos cancelados |
| 9 | Crescimento Mensal | Evolução percentual de vendas mês a mês |
| 10 | Lucro por Região | Margem de lucro média por território |

---

## 🚀 Execução da ETL

### 1️⃣ Criar o banco de dados PostgreSQL
Crie um banco no PostgreSQL chamado, por exemplo, `dw_adventureworks`.

### 2️⃣ Configurar o arquivo `config.py`
```python
SQLSERVER = {
    "driver": "ODBC Driver 17 for SQL Server",
    "server": "localhost",
    "database": "AdventureWorks2022",
    "username": "sa",
    "password": "sua_senha"
}

POSTGRES = {
    "host": "localhost",
    "database": "dw_adventureworks",
    "user": "postgres",
    "password": "sua_senha"
}
```

### 3️⃣ Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Executar o script ETL
```bash
python etl.py
```

O script irá:

✅ Extrair dados do SQL Server (AdventureWorks)  
✅ Transformar e padronizar os dados  
✅ Carregar as tabelas no PostgreSQL  

As tabelas criadas serão:
- `dim_pessoa`
- `dim_cliente`
- `dim_produto`
- `dim_territorio`
- `dim_data`
- `fato_vendas`

---

## 📈 Exemplo de Consulta (KPI de Cancelamentos)

```sql
SELECT 
    SUM(CASE WHEN f.status = 'Canceled' THEN 1 ELSE 0 END) AS qtd_cancelada,
    SUM(line_total) FILTER (WHERE f.status = 'Canceled') AS valor_cancelado
FROM dw.fato_vendas f;
```

---

## 📚 Autor

**Carlos Eduardo Pereira Dutra**  
**Hebert Souza Raphalsky do Nascimento **
**Luiz Eduardo de Pádua Oliveira**
---


