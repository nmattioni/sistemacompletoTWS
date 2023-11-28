import pandas as pd
import matplotlib.pyplot as plt

# Lendo os CSVs
df1 = pd.read_csv('contratosabertos.csv')
df2 = pd.read_csv('netliquidation.csv')

# Realizando a junção dos dados
merged_df = df1.merge(df2, left_on='codigo_conta', right_on='Account', how='left')
merged_df = merged_df.drop(columns='Account')

# Convertendo a coluna 'NetLiquidation' para float (removendo vírgulas e convertendo)
merged_df['NetLiquidation'] = merged_df['NetLiquidation'].str.replace(',', '').astype(float)

# Calculando a alavancagem e tratando divisões por zero
merged_df['alavancagem'] = merged_df.apply(lambda row: row['valor_liquido'] / row['NetLiquidation'] if row['NetLiquidation'] != 0 else 0, axis=1)

# Análise gráfica

# Gráfico de barras para os 5 maiores valores de alavancagem
top_5 = merged_df.nlargest(5, 'alavancagem')
top_5.plot(x='codigo_conta', y='alavancagem', kind='bar', title='Top 5 maiores alavancagens')
plt.ylabel('Alavancagem')
plt.show()

# Gráfico de barras para os 5 menores valores de alavancagem (excluindo zeros)
bottom_5 = merged_df[merged_df['alavancagem'] > 0].nsmallest(5, 'alavancagem')
bottom_5.plot(x='codigo_conta', y='alavancagem', kind='bar', title='Top 5 menores alavancagens')
plt.ylabel('Alavancagem')
plt.show()

# Linha horizontal mostrando a média de alavancagem
avg_leverage = merged_df['alavancagem'].mean()
plt.axhline(y=avg_leverage, color='r', linestyle='-')
plt.title(f'Média de alavancagem: {avg_leverage:.2f}')
plt.show()

print("Análise gráfica concluída!")
