import pandas as pd

# Lendo os CSVs
df_contratos = pd.read_csv('contratosabertos.csv')
df_patrimonio = pd.read_csv('netliquidation.csv')

# Realizando o merge
merged_df = df_contratos.merge(df_patrimonio, left_on='codigo_conta', right_on='Account', how='left').drop(columns='Account')

# Salvando o resultado em um novo arquivo CSV
merged_df.to_csv('consolidado.csv', index=False)
