import pandas as pd

# Dados fornecidos

lista_clientes = [
    'U10355581', 'U10375548', 'U10393335', 'U11071406', 'U11086471', 'U11239176', 'U11424382', 'U11821945', 
    'U12156732', 'U12167071', 'U12192213', 'U12216291', 'U12236925', 'U12277193', 'U12294610', 'U12320396', 
    'U12321651', 'U12351347', 'U12471035', 'U12631300', 'U12666466', 'U12691955', 'U12843298', 'U12997920', 
    'U4031188', 'U5453084', 'U9578694', 'U9624456', 'U9665342'
]

# Lendo o CSV com o pandas

df = pd.read_csv('executions.csv', header=None, names=['codigo_conta', 'ticker', 'quantidade', 'preco', 'tipo_transacao'])

# Calculando o valor líquido por cliente

valores_liquidos = {cliente: 0 for cliente in lista_clientes}

for index, row in df.iterrows():
    if row['codigo_conta'] in valores_liquidos:
        if row['tipo_transacao'] == "BOT":
            valores_liquidos[row['codigo_conta']] += row['quantidade'] * row['preco']
        elif row['tipo_transacao'] == "SLD":
            valores_liquidos[row['codigo_conta']] -= row['quantidade'] * row['preco']

# Convertendo o dicionário em DataFrame e salvando como CSV

df_resultado = pd.DataFrame(valores_liquidos.items(), columns=['codigo_conta', 'valor_liquido'])
df_resultado.to_csv('contratosabertos.csv', index=False)

print("Os valores líquidos foram salvos em 'contratosabertos.csv'")