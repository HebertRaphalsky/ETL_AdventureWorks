SELECT SUM("LineTotal") / NULLIF(COUNT(DISTINCT "SalesOrderID"),0) 
AS ticket_medio FROM fato_vendas;