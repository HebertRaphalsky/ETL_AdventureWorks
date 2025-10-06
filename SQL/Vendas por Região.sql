SELECT t.regiao, SUM(f."LineTotal" ) AS receita
FROM fato_vendas f
JOIN dim_territorio t ON f."TerritoryID"  = t.id_territorio 
GROUP BY t.regiao
ORDER BY receita DESC;