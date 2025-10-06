SELECT SUM(CASE WHEN  f.status = 'Canceled' THEN 1 ELSE 0 END) AS qtd_cancelada,
       SUM(f."LineTotal" ) FILTER (WHERE f.status = 'Canceled') AS valor_cancelado
FROM fato_vendas f;