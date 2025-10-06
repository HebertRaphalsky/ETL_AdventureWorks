WITH monthly AS (
  SELECT d."Ano" , d."Mes" , SUM(f."LineTotal" ) AS receita
  FROM fato_vendas f
  JOIN dim_data d ON f."DateID"  = d."DateID" 
  GROUP BY d."Ano" , d."Mes" 
)
SELECT m.*,
       (m.receita - LAG(m.receita) OVER (ORDER BY m."Ano" , m."Mes" )) / NULLIF(LAG(m.receita) OVER 
       (ORDER BY m."Ano"  , m."Mes" ),0) * 100 AS mom_change_percent
FROM monthly m
ORDER BY m."Ano" , m."Mes" ;