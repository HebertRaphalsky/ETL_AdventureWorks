SELECT SUM("Profit") AS lucro_total, SUM("LineTotal") AS receita_total,
       (SUM("Profit") / NULLIF(SUM("LineTotal"),0)) * 100 AS margem_percent
FROM fato_vendas;