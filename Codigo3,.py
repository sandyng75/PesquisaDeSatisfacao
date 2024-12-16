#%% Código 3 > A VARIÁVEL QUE MAIS INTERFERE NA PSAT DOS ATENDIMENTOS AUTOMATIZADOS

# O código 3 mostra a relação direta entre o percentual de retenção dos clientes nos 
# canais digitais e a nota PSAT. É uma regressão linear simples. 
# Daria também para fazer com as retenções de todas as automações (regressão linear múltipla).
# Da vivência analisando PSAT de URA e WPP, percebi que a quantidade de saídas para o 
# atendimento humano é a variável que mais interfere na nota. Algumas empresas acreditam tanto 
# nos seus robôs que passam a automatizar todos os processos, sem deixar brecha para o cliente 
# explicar todo o perrengue que está passando. Difícil o equilíbrio entre automação e satisfação! 
# Buscar excelência em cada automação é a solução.

#%% Importando pacotes

import pandas as pd 
import statsmodels.api as sm 
import plotly.io as pio 
pio.renderers.default = 'browser' 
import seaborn as sns
import matplotlib.pyplot as plt


#%% Importando arquivo excel. lembre-se que o endereço é com barra à direita "/"

df = pd.read_excel('C:/Users/sandy/OneDrive/Documentos/GitHub/PesquisaDeSatisfacao/Codigo3.xlsx')

#%% Analisando o dataframe importado 

print(df.info())
df.describe()

#%% Analisando gráfico do comportamento de Retenção e Notas por dia

plt.figure(figsize=(30,10))
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Data')
ax1.set_ylabel('Nota', color=color)
ax1.plot(df['Data'], df['Nota_Media'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  
color = 'tab:blue'
ax2.set_ylabel('Retencao', color=color)  
ax2.plot(df['Data'], df['Retenção_Media'], color=color)
ax2.tick_params(axis='y',  labelcolor=color)

fig.tight_layout() 
plt.show()

# Veja que quando retenção sobe a nota cai, inversamente proporcional

#%% Analisando a correlação entre Retenção e Nota PSAT

# Correlação de Pearson
df[['Nota_Media','Retenção_Media']].corr()

# R² (cálculo pelo quadrado da correlação de Pearson)
((df[['Nota_Media','Retenção_Media']].corr())**2).iloc[0,1]

# -0,78 é um valor alto de correlação negativa. 

#%% Analisar as informações no gráfico de dispersão

plt.figure(figsize=(20,10))
sns.regplot(data=df, x='Retenção_Media', y='Nota_Media', ci=False, color='grey')
plt.xlabel('Retenção', fontsize=15)
plt.ylabel('Nota', fontsize=15)
plt.legend(['Valores Reais', 'Valores Preditos'], fontsize=12)
plt.show

#%% Estimação do modelo de regressão linear

modelo = sm.OLS.from_formula("Nota_Media ~ Retenção_Media", df).fit()
modelo.summary()

#%% Inserção dos valores predictos e resíduos

df['Valor_Predito'] = modelo.fittedvalues
df['Residuo'] = modelo.resid
df


#%% Gráfico com o intervalo de confiança de 95%

plt.figure(figsize=(20,10))
sns.regplot(data=df, x='Retenção_Media', y='Nota_Media', ci=95, color='purple')
plt.xlabel('Retenção)', fontsize=20)
plt.ylabel('Nota', fontsize=20)
plt.legend(['Valores Reais', 'Valores Preditos'], fontsize=24)
plt.show

#%% Elaboração de previsões:
# Qual a previsão de nota para 55% de retenção?

modelo.predict(pd.DataFrame({'Retenção_Media':[55]}))

#%% Equação da Reta (Nota = 21.4841 - 0.2815 * Retencao)

# Ou seja, para cada ponto de retenção adicional, há uma redução de 0.2815 da nota.

#%% FIM 

#%% Caso queira analisar correlação somente nos dias úteis (sem sábado e domingo)

df['Dia_semana'] = df['Data'].dt.dayofweek

df_dia_util = df[(df['Dia_semana'] == 0 ) |
                 (df['Dia_semana'] == 1 ) |
                 (df['Dia_semana'] == 2 ) |
                 (df['Dia_semana'] == 3 ) |
                 (df['Dia_semana'] == 4 ) ]

df_dia_util[['Nota_Media','Retenção_Media']].corr()


