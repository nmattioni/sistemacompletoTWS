import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ler o arquivo de análise
df = pd.read_csv('analise.csv')

# Tratar valores ausentes
df.dropna(subset=['alavancagem'], inplace=True)  # Remover linhas onde alavancagem é NaN

# Certificar que 'alavancagem' é numérica
df['alavancagem'] = pd.to_numeric(df['alavancagem'], errors='coerce')

# Ordenar por alavancagem
df_sorted = df.sort_values(by='alavancagem')

# Seaborn settings
sns.set_style("whitegrid")
plt.figure(figsize=(15, 10))

# Plotar todas as alavancagens
sns.barplot(x='codigo_conta', y='alavancagem', data=df_sorted, palette='viridis')

# Linha média de alavancagem
mean_alavancagem = df_sorted['alavancagem'].mean()
plt.axhline(mean_alavancagem, color='red', linestyle='dashed', linewidth=1, label=f'Média: {mean_alavancagem:.2f}')

# Ajustar labels e títulos
plt.xticks(rotation=90)
plt.ylabel('Alavancagem')
plt.xlabel('Código de Conta')
plt.title('Alavancagem por Código de Conta')
plt.legend()

# Mostrar o gráfico
plt.tight_layout()
plt.show()

# Identificando os top 5 mais e menos alavancados para saída no terminal
top_5 = df_sorted.tail(5)
bottom_5 = df_sorted.head(5)

print("Top 5 mais alavancados:")
print(top_5)

print("\nBottom 5 menos alavancados:")
print(bottom_5)
