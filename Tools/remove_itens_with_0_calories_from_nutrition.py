import pandas as pd

# Caminho do arquivo CSV
file_path = '/Users/kadishsilva/Downloads/nutrition.csv'

# Carregar o arquivo CSV
nutrition_data = pd.read_csv(file_path, delimiter=';')

# Filtrar linhas onde as calorias são diferentes de 0 e resetar o índice
filtered_data = nutrition_data[nutrition_data['calories'] != 0].reset_index(drop=True)

# Exibir as primeiras linhas do DataFrame resultante para verificar
print(filtered_data.head())

# Salva o DataFrame filtrado, sobrescrevendo o arquivo original
filtered_data.to_csv(file_path, index=False)

print("Arquivo salvo com sucesso!")
