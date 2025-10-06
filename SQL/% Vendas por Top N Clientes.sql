WITH client_sales AS (
  SELECT f."CustomerID" , SUM(f."LineTotal" ) AS receita
  FROM fato_vendas f
  GROUP BY f."CustomerID" 
)
SELECT SUM(receita) FILTER (WHERE r <= 10) 
/ SUM(receita) * 100 AS pct_top10
FROM (
  SELECT cs.*, ROW_NUMBER() OVER (ORDER BY receita DESC) AS r
  FROM client_sales cs
) t;
