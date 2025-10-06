-- Quantidade Vendida por Produto - Top 10 Produtos

SELECT p.nome_produto, SUM(f."OrderQty" ) AS total_qtd
FROM fato_vendas f
JOIN dim_produto p ON f."ProductID"  = p.id_produto 
GROUP BY p.nome_produto
ORDER BY total_qtd DESC
LIMIT 10;