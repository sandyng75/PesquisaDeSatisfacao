#%% Aplicação em Análise Fatorial PCA

#%% Importando pacotes

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
import pingouin as pg
import plotly.express as px
import plotly.io as pio
import random


#%% Importando o banco de dados

# Fonte: Fávero & Belfiore (2017, Capítulo 10) 

df = pd.read_excel('C:/Users/sandy/OneDrive/Documentos/GitHub/PesquisaDeSatisfacao/Codigo4.xlsx')

print(df)

#%% Matriz de correlaçãoes entre as variáveis

matriz_corr = pg.rcorr(df, method = 'pearson', upper = 'pval', decimals = 4, pval_stars = {0.01: '***', 0.05: '**', 0.10: '*'})
print(matriz_corr)


#%% Gráfico com a matriz de correlações

fig = plt.figure(figsize=(9,7), facecolor='white')
sns.heatmap(df.corr(), vmin = -1, annot=True,linewidth=0.5,  annot_kws={"fontsize":10, 'rotation':0} ,fmt = '.2f', cmap = 'coolwarm')

# Pela matriz é possível observar que:
# Preço e Desconto tem correlação altíssica: 0,9
# Sortimento tem correlação com reposição, layout, conforto e limpeza
# Atendimento não tem correlação significativa com nenhuma das outras variáveis

#%% Teste de Bartlett - compara a matriz de correlações com a matriz identidade de mesma dimensão 
# e espera-se que tais matrizes sejam diferentes para que a análise seja aplicável

# H0: As matrizes não são diferentes (p > 0.05)
# H1: As matrizes são diferentes (p < 0.05)

bartlett, p_value = calculate_bartlett_sphericity(df)
print(f'Bartlett statistic: {bartlett}')
print(f'p-value : {p_value}')


#%% Definindo a PCA (inicial)

fa = FactorAnalyzer()
fa.fit(df)

#%% Obtendo os Eigenvalues (autovalores)
# O critério de Kaiser (ou critério da raiz latente) indica que sejam considerados apenas
# fatores correspondentes a autovalores > 1

ev, v = fa.get_eigenvalues()
print(ev)
print([item for item in ev if item > 1])

# Temos 2 autovalores maiores que 1 e outro próximo de 1. 
# Escolho selecionar 3 fatores para perder menos variância dos dados.

#%% Parametrizando a PCA para 2 fatores (autovalores > 1)

fa.set_params(n_factors = 3, method = 'principal', rotation = None)
fa.fit(df)

#%% Eigenvalues, variâncias e variâncias acumulada

eigen_fatores = fa.get_factor_variance()
eigen_fatores

tabela_eigen = pd.DataFrame(eigen_fatores)
tabela_eigen.columns = [f"Fator {i+1}" for i, v in enumerate(tabela_eigen.columns)]
tabela_eigen.index = ['Autovalor','Variância', 'Variância Acumulada']
tabela_eigen = tabela_eigen.T

print(tabela_eigen)

# Variância acumulada com 3 fatores de 87,7%

#%% Determinando as cargas fatoriais

cargas_fatores = fa.loadings_

tabela_cargas = pd.DataFrame(cargas_fatores)
tabela_cargas.columns = [f"Fator {i+1}" for i, v in enumerate(tabela_cargas.columns)]
tabela_cargas.index = df.columns
tabela_cargas

print(tabela_cargas)

# Fator 1 tem correlação alta com sortimento, layout, conforto, limpeza e reposição.
# Fator 2 tem correlação alta com preco e desconto.
# Fator 3 tem correlação alta com atendimento.

#%% Determinando as comunalidades

comunalidades = fa.get_communalities()

tabela_comunalidades = pd.DataFrame(comunalidades)
tabela_comunalidades.columns = ['Comunalidades']
tabela_comunalidades.index = df.columns
tabela_comunalidades

print(tabela_comunalidades)

# limpeza foi a variável que mais perdeu variância. Os demais ficaram acima de 80%

#%% Resultado do fator para as observações do dataset

predict_fatores= pd.DataFrame(fa.transform(df))
predict_fatores.columns =  [f"Fator {i+1}" for i, v in enumerate(predict_fatores.columns)]

# Adicionando ao banco de dados

df = pd.concat([df.reset_index(drop=True), predict_fatores], axis=1)

print(df)

#%% Identificando os scores fatoriais

scores = fa.weights_

tabela_scores = pd.DataFrame(scores)
tabela_scores.columns = [f"Fator {i+1}" for i, v in enumerate(tabela_scores.columns)]
tabela_scores.index = tabela_cargas.index

print(tabela_scores)

#Equações

#F1 = Zsort*0.23 + Zrepo*0.18 + Zlay*0.22 + Zconf*0.23 + Zlimp*0.22 + Zatend*0.08 + Zpre*0.07 + Zdesc*0.06
#F2 = Zsort*(-0.07) + Zrepo*(-0.29) + Zlay*0.08 + Zconf*(-0.01) + Zlimp*(-0.04) + Zatend*0.02 + Zpre*0.42 + Zdesc*0.40
#F3 = Zsort*(-0.12) + Zrepo*(0.05) + Zlay*(-0.20) + Zconf*(-0.02) + Zlimp*(-0.03) + Zatend*0.99 + Zpre*(-0.01) + Zdesc*(-0.03)

#%% Criando um ranking

df['Ranking'] = 0

for index, item in enumerate(list(tabela_eigen.index)):
    variancia = tabela_eigen.loc[item]['Variância']

    df['Ranking'] = df['Ranking'] + df[tabela_eigen.index[index]]*variancia


#%% Gráfico da variância acumulada dos componentes principais

plt.figure(figsize=(12,8))

plt.title(f"{tabela_eigen.shape[0]} componentes principais que explicam {round(tabela_eigen['Variância'].sum()*100,2)}% da variância", fontsize=14)
ax = sns.barplot(x=tabela_eigen.index, y=tabela_eigen['Variância'], data=tabela_eigen, color='green')

ax.bar_label(ax.containers[0])
plt.xlabel("Componentes principais", fontsize=14)
plt.ylabel("Porcentagem de variância explicada (%)", fontsize=14)
plt.show()


#%% Obtendo o índice da tabela de cargas fatoriais

tabela_cargas = tabela_cargas.reset_index()

#%% Plotando no gráfico 2D com 2 fatores

plt.figure(figsize=(16,10))
plt.scatter(tabela_cargas["Fator 1"], tabela_cargas["Fator 2"])

def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val':val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']))

label_point(x = tabela_cargas["Fator 1"],
            y = tabela_cargas["Fator 2"],
            val=tabela_cargas["index"],
            ax = plt.gca()) 

plt.xlabel("PC 1", fontsize=14)
plt.ylabel("PC 2", fontsize=14)

plt.axhline(y = 0, color = 'gray', linestyle = '--')
plt.axvline(x = 0, color = 'gray', linestyle = '--')
plt.xlim([-1, 1])
plt.ylim([-1, 1])
plt.show()

#%% Podemos observar o ranking formado

print(df.sort_values(by=["Ranking"],ascending=True))

#%% Gráfico 3D

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')

ax.set_xlabel('Fator 1')
ax.set_ylabel('Fator 2')
ax.set_zlabel('Fator 3')

sequence_containing_x_vals = tabela_cargas['Fator 1']
sequence_containing_y_vals = tabela_cargas['Fator 2']
sequence_containing_z_vals = tabela_cargas['Fator 3']

random.shuffle(sequence_containing_x_vals)
random.shuffle(sequence_containing_y_vals)
random.shuffle(sequence_containing_z_vals)

ax.scatter(sequence_containing_x_vals, sequence_containing_y_vals, sequence_containing_z_vals)
plt.show()

#%% Fim