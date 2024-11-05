import csv
import random

def criar_csv_reduzido(arquivo_entrada, arquivo_saida, num_linhas):
    with open(arquivo_entrada, mode='r', newline='', encoding='utf-8') as csv_in:
        reader = list(csv.reader(csv_in, delimiter=';'))
        
        cabecalho = reader[0]
        dados = reader[1:] 
        
        linhas_aleatorias = random.sample(dados, min(num_linhas, len(dados)))
        
    with open(arquivo_saida, mode='w', newline='', encoding='utf-8') as csv_out:
        writer = csv.writer(csv_out, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        writer.writerow(cabecalho)
        writer.writerows(linhas_aleatorias)

if __name__ == '__main__':
    criar_csv_reduzido('data/nutrition_macro_fixed.csv', 'data/sample_nutrition_data.csv', 100)
