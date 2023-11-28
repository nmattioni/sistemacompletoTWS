import pandas as pd

# Lendo o CSV consolidado
df_consolidado = pd.read_csv('consolidado.csv')

# Convertendo os valores de NetLiquidation para float
df_consolidado['NetLiquidation'] = df_consolidado['NetLiquidation'].astype(float)

# Calculando a alavancagem
df_consolidado['alavancagem'] = df_consolidado['valor_liquido'] / df_consolidado['NetLiquidation']

# Salvando o resultado em um novo arquivo CSV
df_consolidado.to_csv('analise.csv', index=False)
