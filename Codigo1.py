#%% Código 1 >>> Análise de duas médias de amostras independentes
# Nível de significância = 5%

# Importando pacotes
import pandas as pd #manipulação de dados em formato de dataframe
from scipy import stats #biblioteca de operações estatísticas
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu

#%% Importando arquivo excel. lembre-se que o endereço é com barra à direita "/"

df = pd.read_excel('C:/Users/sandy/OneDrive/Documentos/GitHub/PesquisaDeSatisfacao/Codigo1.xlsx')

#%% Analisando o dataframe importado 

print(df.describe())
print(df.info())

#%% Adicionando a coluna mês na tabela. 
#Supondo que houve uma implatanção de melhoria no dia 01/04/2024 

df['Mes'] = df['Data'].map(lambda x: 100*x.year + x.month)

#%% Verificando a média das notas de cada mes
#Houve um acréscimo de 0.50 na nota em abril (pós-implantação)

Nota = df[['Mes', 'Nota']]
Media_nota = Nota.groupby(by =['Mes']).mean() 

print(Media_nota)

#%% Histograma com as médias

sns.barplot(x="Mes", y="Nota", data=Media_nota)
plt.title("Média das Notas de PSAT")
plt.xlabel('Mês',fontsize=12)
plt.ylabel('Nota',fontsize=12)
plt.show()

#%% Criando duas amostras somente com as notas, uma para cada mês

antes = df.loc[df['Mes']== 202403, 'Nota']
depois = df.loc[df['Mes']== 202404, 'Nota'].reset_index(drop=True)

print(antes)      
print(depois)
                  
#%% Verificando se a distribuição dos resíduos é normal para usar T de Student.
#Teste de Shapiro Wilk é o mais usado
#H0: a amostra possui distribuição normal (p > 0.05)
#H1:a amostra não possui distribuição normal (p < 0.05)

TNormal_antes = stats.shapiro(antes)
print('Estatística:', TNormal_antes.statistic)
print('P-value:', TNormal_antes.pvalue)

TNormal_depois = stats.shapiro(depois)
print('Estatística:', TNormal_depois.statistic)
print('P-value:', TNormal_depois.pvalue) 

#%% O teste de Shapiro resultou em os p-values < 0,05. 
# Ou seja, rejeitamos H0 (as amostras não possuem distribuição normal)
# Ao inves de rodar o Teste t, iremos rodar o Teste U de Mann-Whitney
# H0 : Não existe diferença significativa entre as médias (p > 0.05)
# H1 : Existe diferença significativa entre as médias (p < 0.05)   

U1, p = mannwhitneyu(antes, depois, method="exact")
print('Estatística:', U1)
print('P-value:', p) 


#%% Para amostras com distribuição normal, segue código para Teste T
# H0 : Não existe diferença significativa entre as médias (p > 0.05)
# H1 : Existe diferença significativa entre as médias (p < 0.05)
   
t_stat, p_value = ttest_ind(antes, depois)
print('Estatística:', t_stat)
print('P-value:', p_value) 

# Os resultados dos testes (tanto Mann Whitney como T de Student) mostram que não 
# existe diferença significativa entre as médias de março e abril

#%% FIM
