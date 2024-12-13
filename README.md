# PesquisaDeSatisfacao

Repositório com análises de dados em Python com base em Pesquisas de Satisfação.


Código 1 > A NOTA AUMENTOU 0.50, TÁ VALENDO?

Empresa boa é aquela que olha constantemente para a satisfação do cliente, não é mesmo?! Possui vários profissionais para melhorar o layout do app, jornada de pesquisa de produtos, de pagamento, de pós-venda, etc. E frequentemente, queremos mostrar à diretoria que aquela melhoria (que demorou 3 meses para ser implantada) aumentou a PSAT e gritar (silenciosamente): "NÃO FALEI QUE IRIA DAR CERTO?!". Massss, será que o aumento foi realmente significativo ou ficou dentro da margem de confiança? Segue código para ver se aquele 0.5 é estatisticamente relevante.



Código 2 > QUEM NUNCA FEZ MÉDIA COM LIKERT QUE ATIRE A PRIMEIRA PEDRA

Escala Likert, muito usada no final do atendimento de SAC, NÃO é uma variável quantitativa e sim qualitativa ordinal (assim como escolaridade). A atribuição de um número para cada item, como no exemplo abaixo, não significa que todos os clientes possuem na mente uma escala métrica de um ponto para cada nível de satisfação. Cada cliente possui a sua escala abstrata do que é "muito bom" ou "muito ruim". Dessa maneira, avaliar se a MÉDIA da Likert subiu ou desceu não faz sentido, melhor seria pedir uma nota de 0 a 10. Seguem dois códigoS para analisar variável qualitativa: Tabela de Contingência (cross tabulation) e Análise de Correspondência com Mapa Perceptual.

Exemplo: Avalie o nosso atendimento em relação a sua satisfação:

- 5 Muito satisfeito
- 4 Satisfeito
- 3 Indiferente
- 2 Insatisfeito 
- 1 Muito Insatisfeito


Código 3 > A VARIÁVEL QUE MAIS INTERFERE NA PSAT DOS ATENDIMENTOS AUTOMATIZADOS

O código 3 mostra a relação direta entre o percentual de retenção dos clientes nos canais digitais e a nota PSAT. É uma regressão linear simples. Daria também para fazer com as retenções de todas as automações (regressão linear múltipla).

Da vivência analisando PSAT de URA e WPP, percebi que a quantidade de saídas para o atendimento humano é a variável que mais interefere na nota. Algumas empresas acreditam tanto nos seus robôs que passam a automatizar todos os processos, sem deixar brechas para o cliente explicar todo o perrengue. Difícil equilíbrio entre custos e satisfação! Buscar excelência em cada automação é a solução.



