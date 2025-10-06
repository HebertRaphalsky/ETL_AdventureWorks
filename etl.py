import pandas as pd
from sqlalchemy import create_engine
import urllib
import config

# --- ETAPA 1: Conectar ao SQL Server ---
def get_sqlserver_engine():
    params = urllib.parse.quote_plus(
        f"DRIVER={{{config.SQLSERVER['driver']}}};"
        f"SERVER={config.SQLSERVER['server']},1433;"
        f"DATABASE={config.SQLSERVER['database']};" 
        f"UID={config.SQLSERVER['username']};"
        f"PWD={config.SQLSERVER['password']};"
        f"TrustServerCertificate=yes;"
    )
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    return engine

# --- ETAPA 2: Conectar ao PostgreSQL ---
def get_postgres_engine():
    conn_str = (
        f"postgresql+psycopg2://{config.POSTGRES['user']}:"
        f"{config.POSTGRES['password']}@{config.POSTGRES['host']}/"
        f"{config.POSTGRES['database']}"
    )
    engine = create_engine(conn_str)
    return engine

# -----------------------------
# --- ETAPA 3: Extrair dados ---
# -----------------------------

# Pessoas

def extract_person(engine):
    query = """
        SELECT BusinessEntityID, FirstName, LastName, ModifiedDate
        FROM Person.Person
    """
    return pd.read_sql(query, engine)

# Clientes Pessoa Física

def extract_customer_individual(engine):
    query = """
        SELECT c.CustomerID, c.PersonID, p.Title, p.FirstName, p.MiddleName, p.LastName, 
           a.AddressLine1, a.AddressLine2, a.City,  sp.StateProvinceCode, sp.name as StateProvinceName, sp.CountryRegionCode, cr.Name as CountryName,  a.PostalCode
        FROM Sales.Customer c
        LEFT JOIN person.Person p  ON c.PersonID = p.BusinessEntityID
        LEFT JOIN Person.BusinessEntityAddress ba  ON c.PersonID = ba.BusinessEntityID
        LEFT JOIN person.Address a ON ba.AddressID = a.AddressID 
        LEFT JOIN person.StateProvince sp ON a.StateProvinceID = sp.StateProvinceID
        LEFT JOIN person.CountryRegion cr ON sp.CountryRegionCode = cr.CountryRegionCode 
        WHERE c.PersonID is not null  
    """
    return pd.read_sql(query, engine)

# Clientes Pessoa Jurídica

def extract_customer_legalentity(engine):
    query = """
        SELECT c.CustomerID, c.PersonID, a.City, a.StateProvinceID, a.CountryRegionCode
        FROM Sales.Customer c
        LEFT JOIN Sales.CustomerAddress ca ON c.CustomerID = ca.CustomerID
        LEFT JOIN Person.Address a ON ca.AddressID = a.AddressID
    """
    return pd.read_sql(query, engine)



def extract_product(engine):
    query = """
        SELECT p.ProductID, p.Name AS ProductName, sc.Name AS SubcategoryName, c.Name AS CategoryName
        FROM Production.Product p
        JOIN Production.ProductSubcategory sc ON p.ProductSubcategoryID = sc.ProductSubcategoryID
        JOIN Production.ProductCategory c ON sc.ProductCategoryID = c.ProductCategoryID
    """
    return pd.read_sql(query, engine)

def extract_territory(engine):
    query = "SELECT t.TerritoryID, t.Name AS TerritoryName, t.CountryRegionCode AS Country, t.[Group] AS Region FROM Sales.SalesTerritory t"
    return pd.read_sql(query, engine)

def extract_orders(engine):
    query = """
        SELECT s.SalesOrderID, s.OrderDate, s.CustomerID, s.TerritoryID,
               sd.ProductID, sd.OrderQty, sd.UnitPrice, sd.LineTotal, s.Status
        FROM Sales.SalesOrderHeader s
        JOIN Sales.SalesOrderDetail sd ON s.SalesOrderID = sd.SalesOrderID

    """
    return pd.read_sql(query, engine)

# -----------------------------
# --- ETAPA 4: Transformar dados ---
# -----------------------------

def transform_person(df):
    df.rename(columns={
        "BusinessEntityID": "id_pessoa",
        "FirstName": "primeiro_nome",
        "LastName": "sobrenome",
        "ModifiedDate": "data_modificacao"
    }, inplace=True)
    df["nome_completo"] = df["primeiro_nome"] + " " + df["sobrenome"]
    return df

def transform_customer_individual(df):
    df.rename(columns={
        "CustomerID": "id_cliente",
        "PersonID": "id_pessoa",
        "Title": "titulo", 
        "FirstName" : "primeiro_nome", 
        "MiddleName" : "nome_meio", 
        "LastName" : "sobrenome",
        "AddressLine1" : "endereco_linha1", 
        "AddressLine2" : "endereco_linha2", 
        "City" : "cidade",  
        "StateProvinceCode" : "estado_provincia_codigo",
        "StateProvinceName": "estado_provincia_nome",
        "CountryRegionCode" : "pais_codigo",
        "CountryName" : "pais_nome",
        "a.PostalCode": "cep"
    }, inplace=True)
    return df

def transform_product(df):
    df.rename(columns={
        "ProductID": "id_produto",
        "ProductName": "nome_produto",
        "SubcategoryName": "subcategoria",
        "CategoryName": "categoria"
    }, inplace=True)
    return df

def transform_territory(df):
    df.rename(columns={
        "TerritoryID": "id_territorio",
        "TerritoryName": "nome_territorio",
        "Country": "pais",
        "Region": "regiao"
    }, inplace=True)
    return df

def transform_orders(df):
    # Criar DateID para ligação com dimensão tempo
    df['DateID'] = df['OrderDate'].dt.strftime('%Y%m%d').astype(int)
    
    # Calcular lucro aproximado (custo = 70% do unit price)
    df['Profit'] = df['LineTotal'] - (df['OrderQty'] * df['UnitPrice'] * 0.7)
    
    # Traduzir Status numérico para texto
    status_map = {
        1: 'In Process',
        2: 'Approved',
        3: 'Backordered',
        4: 'Rejected',
        5: 'Shipped',
        6: 'Canceled'
    }
    df['status'] = df['Status'].map(status_map)
    
    return df

def create_dim_data(df_orders):
    df_data = df_orders[['OrderDate']].drop_duplicates().copy()
    df_data['DateID'] = df_data['OrderDate'].dt.strftime('%Y%m%d').astype(int)
    df_data['Ano'] = df_data['OrderDate'].dt.year
    df_data['Mes'] = df_data['OrderDate'].dt.month
    df_data['Dia'] = df_data['OrderDate'].dt.day
    df_data['Trimestre'] = df_data['OrderDate'].dt.quarter
    df_data['Semana'] = df_data['OrderDate'].dt.isocalendar().week
    return df_data

# -----------------------------
# --- ETAPA 5: Carregar no PostgreSQL ---
# -----------------------------

def load_table(df, table_name, engine):
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"✅ Tabela {table_name} carregada no PostgreSQL ({len(df)} registros).")

# -----------------------------
# --- MAIN ---
# -----------------------------
if __name__ == "__main__":
    sql_engine = get_sqlserver_engine()
    pg_engine = get_postgres_engine()

    # Pessoas
    df_person = transform_person(extract_person(sql_engine))
    load_table(df_person, "dim_pessoa", pg_engine)

    # Clientes
    df_customer = transform_customer_individual(extract_customer_individual(sql_engine))
    load_table(df_customer, "dim_cliente", pg_engine)

    # Produtos
    df_product = transform_product(extract_product(sql_engine))
    load_table(df_product, "dim_produto", pg_engine)

    # Território
    df_territory = transform_territory(extract_territory(sql_engine))
    load_table(df_territory, "dim_territorio", pg_engine)

    # Pedidos / Fato Vendas
    df_orders = transform_orders(extract_orders(sql_engine))
    load_table(df_orders, "fato_vendas", pg_engine)

    # Dimensão Data
    df_dim_data = create_dim_data(df_orders)
    load_table(df_dim_data, "dim_data", pg_engine)

    print("✅ ETL completo finalizado!")
