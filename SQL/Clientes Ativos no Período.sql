SELECT COUNT(DISTINCT f."CustomerID" ) AS clientes_ativos
FROM fato_vendas f
JOIN dim_data d ON f."DateID"  = d."DateID" 
WHERE d."OrderDate"  between  '2014-01-01' AND '2014-12-31';