#%%Código 2 > QUEM NUNCA FEZ MÉDIA COM LIKERT QUE ATIRE A PRIMEIRA PEDRA

# Escala Likert, muito usada no final do atendimento de SAC, não é uma variável quantitativa. 
# A atribuição de um número para cada item, como no exemplo abaixo, não significa que todos 
# os clientes possuem na mente uma escala métrica de um ponto para cada nível de satisfação. 
# Cada cliente possui a sua escala abstrata do que é "muito bom" ou "muito ruim". 
# Dessa maneira, avaliar se a média da Likert subiu ou desceu não faz sentido, 
# melhor seria pedir uma nota de 0 a 10. Seguem dois código para analisar variável qualitativa:
# Contagem de Frequência e Análise de Correspondência Múlpila com mapa perceptual.

#%% Importando pacotes

import pandas as pd #manipulação de dados em formato de dataframe
from scipy.stats import chi2_contingency #estatística qui-quadrado e teste
import prince #biblioteca para Análise de Correspondência Simples e Múlpila 

#%% Importando arquivo excel. lembre-se que o endereço é com barra à direita "/"

base_original = pd.read_excel('C:/Users/sandy/OneDrive/Documentos/GitHub/PesquisaDeSatisfacao/Codigo2.xlsx')

#%% Analisando o dataframe importado 

print(base_original.info())

#%% Ajustando as variáveis para type = 'category' no dataframe 'df'

base = base_original[['Regiao','Tier','PSAT']] 
base = base.astype('category')
base.info()

#%% Criando tabelas de contingências

tabela_mca_1 = pd.crosstab(base["PSAT"], base["Regiao"])
tabela_mca_2 = pd.crosstab(base["PSAT"], base["Tier"])

print(tabela_mca_1.sort_values(by = 'PSAT', ascending = True ))
print(tabela_mca_2)

#%% Analisando a significância estatística das associações (teste qui²)
# Hipótese 0: a associação se dá de forma proporcional (p > 0.05)
# Hipótese 1: as associação não é proporcional (p < 0.05)

chi2, pvalor, df, freq_esp = chi2_contingency(tabela_mca_1)
print("Associação 1")
print(f"estatística qui²: {chi2}") # estatística qui²
print(f"p-valor da estatística: {pvalor}") # p-valor da estatística
print(f"graus de liberdade: {df} \n") # graus de liberdade


chi2, pvalor, df, freq_esp = chi2_contingency(tabela_mca_2)
print("Associação 2")
print(f"estatística qui²: {chi2}") # estatística qui²
print(f"p-valor da estatística: {pvalor}") # p-valor da estatística
print(f"graus de liberdade: {df} \n") # graus de liberdade

# Como os p-values estão abaixo de 0.05, rejeitamos H0 e podemos fazer a MCA

#%% Elaboração da MCA propriamente dita (função 'MCA' do pacote 'prince')

mca = prince.MCA()
mca = mca.fit(base)


#%%Coordenadas das categorias das variáveis e das observações

# Coordenadas das abcissas e ordenadas das categorias das variáveis
mca.column_coordinates(base)

# Coordenadas das abcissas e ordenadas das observações (estudantes)
mca.row_coordinates(base)


#%% Mapa perceptual 

mca.plot_coordinates(X=base,
                     figsize=(10,8),
                     show_row_points = False,
                     show_column_points = True,
                     show_row_labels=False,
                     show_column_labels = True,
                     column_points_size = 100)

#%%  Observa-se no mapa perceptual em relação as regiões:
     
# Região SUL está altamente associada com MUITO INSATISFEITO
# Região CENTRO-OESTE está associada com INSATISFEITO e INDIFERENTE
# Região SUDESTE e NORTE estão associados com SATISFEITO
# Região NORDESTE está altamente associada com MUITO SATISFEITO

# Já em relação aos Tiers: 

# Tier 1 está associada com MUITO INSATISFEITO e INDIFERENTE (o que é péssimo para os negócios)
# Tier 2 está altamente associada com SATISFEITO
# Tier 3 está altamente associada com MUITO SATISFEITO

# Próxima pesquisa, entender porquê o Tier 1 possui tantos clientes insatisfeitos.    

#%% FIM