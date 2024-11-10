# # Importações necessárias para o funcionamento do algoritmo
# import sys  # Usado para saída de dados no console
# import numpy as np  # Biblioteca para manipulação de arrays e números
# from numpy import random  # Funções aleatórias da biblioteca numpy
# from typing import Final  # Para definir constantes no código
# import matplotlib.pyplot as plt  # Biblioteca para plotar gráficos

# # Constantes do algoritmo genético
# FRASE: Final[str] = 'EuAdoroInteligenciaArtificialPorqueTemMuitaMatematica'  # Frase alvo do algoritmo
# TAM_CROMO: Final[int] = len(FRASE)  # Tamanho do cromossomo, igual ao número de caracteres da frase
# TAM_POP: Final[int] = TAM_CROMO * 2  # Tamanho da população, definido como o dobro do tamanho da frase

# # Matrizes para armazenar população e novos indivíduos
# pop = np.zeros((TAM_POP, TAM_CROMO))  # População inicial de indivíduos
# nova_pop = np.zeros((TAM_POP, TAM_CROMO))  # Nova população após reprodução
# pais = np.zeros((2, TAM_CROMO))  # Pais selecionados para cruzamento
# filhos = np.zeros((2, TAM_CROMO))  # Filhos gerados após cruzamento
# nota_pop = np.zeros((TAM_POP, 3))  # Matriz de notas dos indivíduos (índice, aptidão, probabilidade)

# def init_pop():
#     """
#     Inicializa a população com valores aleatórios, correspondendo a caracteres ASCII entre 65 e 122.
#     """
#     global pop  # Utiliza a variável global pop para armazenar a população
#     pop = random.randint(low=65, high=122, size=(TAM_POP, TAM_CROMO))  # Gera caracteres aleatórios para cada indivíduo

# def avalia_pop():
#     """
#     Avalia a aptidão de cada indivíduo da população comparando com a frase-alvo.
#     Calcula a aptidão como a soma das diferenças ao quadrado entre os caracteres do indivíduo e da frase-alvo.
#     Ordena os indivíduos pela aptidão e calcula as probabilidades de seleção para reprodução.
#     """
#     global nota_pop  # Utiliza a variável global nota_pop para armazenar as notas
#     soma_apt = 0  # Variável para armazenar a soma das aptidões de toda a população

#     # Avaliação da aptidão de cada indivíduo
#     for i in range(TAM_POP):
#         apt = 0  # Inicializa a aptidão do indivíduo i
#         for j in range(TAM_CROMO):
#             apt += (ord(FRASE[j]) - pop[i][j]) ** 2  # Diferença ao quadrado entre a letra da frase e do indivíduo

#         nota_pop[i][0] = i  # Armazena o índice do indivíduo
#         nota_pop[i][1] = apt  # Armazena a aptidão calculada
#         nota_pop[i][2] = -1  # Inicializa a probabilidade como -1 (será calculada depois)
#         soma_apt += apt  # Soma a aptidão deste indivíduo à soma total

#     # Ordena os indivíduos pela aptidão (quanto menor, melhor)
#     nota_pop = nota_pop[nota_pop[:, 1].argsort()]

#     # Calcula a probabilidade de seleção com base na aptidão inversa
#     minsum = 0  # Soma das probabilidades
#     for i in range(TAM_POP):
#         if soma_apt > 0 and nota_pop[i][1] > 0:  # Apenas calcula se a soma e aptidão são válidas
#             nota_pop[i][2] = ((1 / nota_pop[i][1]) / soma_apt) * 100  # Inverso da aptidão
#         else:
#             nota_pop[i][2] = 0  # Evita divisão por zero
#         minsum += nota_pop[i][2]

#     # Normaliza as probabilidades para que a soma seja 100%
#     for i in range(TAM_POP):
#         if minsum > 0:
#             nota_pop[i][2] /= minsum
#         else:
#             nota_pop[i][2] = 0  # Se a soma for zero, define probabilidade como 0

# def seleciona_pais():
#     """
#     Seleciona dois pais com base na roleta viciada, onde a probabilidade de ser selecionado
#     depende da aptidão do indivíduo.
#     """
#     global pais  # Utiliza a variável global pais para armazenar os pais selecionados

#     # Gera dois números aleatórios para selecionar os pais
#     r_pai1 = random.random_sample(size=None)
#     r_pai2 = random.random_sample(size=None)

#     # Seleciona o primeiro pai
#     acum = 0  # Acumulador para verificar a soma das probabilidades
#     for i in range(TAM_POP):
#         acum += nota_pop[i][2]
#         if acum >= r_pai1:  # Se o acumulador ultrapassar o valor aleatório, seleciona este indivíduo
#             pais[0] = pop[nota_pop[i][0].astype(int)]
#             break

#     # Seleciona o segundo pai da mesma forma
#     acum = 0
#     for i in range(TAM_POP):
#         acum += nota_pop[i][2]
#         if acum >= r_pai2:
#             pais[1] = pop[nota_pop[i][0].astype(int)]
#             break

# def cruza_pais():
#     """
#     Realiza o cruzamento entre os dois pais para gerar dois filhos.
#     Utiliza uma taxa de cruzamento de 80%, e em caso de cruzamento, faz um corte aleatório no cromossomo.
#     """
#     global filhos  # Utiliza a variável global filhos para armazenar os filhos gerados

#     r_cruza = random.random_sample(size=None)  # Probabilidade de ocorrer cruzamento
#     if r_cruza < 0.80:
#         corte = random.randint(low=0, high=TAM_CROMO-1)  # Escolhe um ponto de corte aleatório no cromossomo
#         # Gera os filhos com base no ponto de corte
#         filhos[0][:corte] = pais[0][:corte]
#         filhos[0][corte:] = pais[1][corte:]
#         filhos[1][corte:] = pais[0][corte:]
#         filhos[1][:corte] = pais[1][:corte]
#     else:
#         filhos[0] = pais[0]  # Sem cruzamento, os filhos são cópias dos pais
#         filhos[1] = pais[1]

# def muta_filhos():
#     """
#     Aplica mutação nos filhos, alterando aleatoriamente um caractere com uma chance de 3%.
#     """
#     global filhos  # Utiliza a variável global filhos para aplicar as mutações

#     # Aplica mutação no primeiro filho
#     for i in range(TAM_CROMO):
#         r_muta = random.random_sample(size=None)  # Gera um valor aleatório
#         if r_muta < 0.03:  # Se o valor for menor que 3%, ocorre a mutação
#             filhos[0][i] = random.randint(low=65, high=122)  # Novo valor aleatório para o gene

#     # Aplica mutação no segundo filho da mesma forma
#     for i in range(TAM_CROMO):
#         r_muta = random.random_sample(size=None)
#         if r_muta < 0.03:
#             filhos[1][i] = random.randint(low=65, high=122)

# def elitismo(qtde):
#     """
#     Copia os melhores 'qtde' indivíduos da população atual para a nova população sem modificações.
#     """
#     global nova_pop  # Utiliza a variável global nova_pop para armazenar a nova geração
#     for i in range(qtde):
#         nova_pop[i] = pop[nota_pop[i][0].astype(int)]  # Copia os melhores indivíduos diretamente

# def imprime_pop():
#     """
#     Imprime a população atual em formato de caracteres (convertendo os valores ASCII para letras).
#     """
#     for i in range(len(FRASE)*2):
#         for j in range(len(FRASE)):
#             sys.stdout.write(chr(pop[i][j]))  # Converte o valor ASCII para caractere
#         print("")  # Pula linha após imprimir cada indivíduo

# def imprime_nota_pop():
#     """
#     Imprime as notas de todos os indivíduos da população, incluindo aptidão e probabilidade.
#     """
#     acum = 0  # Variável para armazenar a soma acumulada das probabilidades
#     for i in range(TAM_POP):
#         acum += nota_pop[i][2]  # Acumula as probabilidades
#         print('Individuo: ', nota_pop[i][0], '- Nota: ', nota_pop[i][1], '- (%): ', nota_pop[i][2], ' - Acum: ', acum)

# def imprime_melhor():
#     """
#     Imprime o melhor indivíduo da população atual.
#     """
#     sys.stdout.write('>> Melhor: ')
#     for i in range(len(FRASE)):
#         sys.stdout.write(chr(pop[nota_pop[0][0].astype(int)][i].astype(int)))  # Imprime o melhor indivíduo
#     print(' - Nota: ', nota_pop[0][1], ' - (%): ', nota_pop[0][2])

# def imprime_pior():
#     """
#     Imprime o pior indivíduo da população atual.
#     """
#     sys.stdout.write('>> Pior:   ')
#     for i in range(len(FRASE)):
#         sys.stdout.write(chr(pop[nota_pop[TAM_POP-1][0].astype(int)][i].astype(int)))  # Imprime o pior indivíduo
#     print(' - Nota: ', nota_pop[TAM_POP-1][1], ' - (%): ', nota_pop[TAM_POP-1][2])

# def imprime_medio():
#     """
#     Imprime o indivíduo mediano da população atual, ou seja, aquele que está no meio da classificação.
#     """
#     sys.stdout.write('>> Medio:  ')
#     meio = (TAM_POP - 1) // 2  # Calcula o índice do indivíduo mediano
#     for i in range(len(FRASE)):
#         sys.stdout.write(chr(pop[nota_pop[meio][0].astype(int)][i].astype(int)))  # Imprime o indivíduo mediano
#     print(' - Nota: ', nota_pop[meio][1], ' - (%): ', nota_pop[meio][2])

# # Código principal que executa o algoritmo genético
# if __name__ == '__main__':
#     # Listas para armazenar dados para gráficos de convergência
#     geracao = []  # Armazena o número da geração
#     melhor = []   # Armazena a aptidão do melhor indivíduo em cada geração
#     pior = []     # Armazena a aptidão do pior indivíduo em cada geração
#     medio = []    # Armazena a aptidão do indivíduo mediano em cada geração

#     # Exibe a frase-alvo
#     print(FRASE)

#     # Inicializa a população com indivíduos aleatórios
#     init_pop()

#     # Imprime a população inicial
#     imprime_pop()

#     # Executa o algoritmo genético por até 2000 gerações
#     for i in range(2000):
#         print('GERACAO: ', i)

#         # Avalia a população atual
#         avalia_pop()

#         # Imprime o melhor, o pior e o mediano da geração atual
#         imprime_melhor()
#         imprime_pior()
#         imprime_medio()

#         # Critério de parada: se o melhor indivíduo tiver aptidão próxima de zero (solução encontrada)
#         if nota_pop[0][1] < 1:
#             break

#         # Armazena dados para os gráficos de convergência
#         geracao.append(i)
#         melhor.append(nota_pop[0][1])
#         pior.append(nota_pop[TAM_POP-1][1])
#         medio.append(nota_pop[(TAM_POP-1) // 2][1])

#         # Preserva os 'n' melhores indivíduos (elitismo)
#         j = 4  # Quantidade de indivíduos preservados
#         elitismo(j)

#         # Gera a nova população até atingir o tamanho total
#         while j < TAM_POP:
#             # Seleciona pais com base nas probabilidades calculadas
#             seleciona_pais()

#             # Realiza o cruzamento entre os pais
#             cruza_pais()

#             # Aplica mutações nos filhos
#             muta_filhos()

#             # Adiciona os filhos à nova população
#             nova_pop[j] = filhos[0]
#             nova_pop[j+1] = filhos[1]
#             j += 2

#         # Substitui a população antiga pela nova
#         pop = nova_pop.copy()
#         nova_pop = np.zeros((TAM_POP, TAM_CROMO))  # Limpa a nova população para a próxima geração

#     # Gera e exibe o gráfico de convergência do algoritmo
#     plt.title("CONVERGENCIA AG")
#     plt.plot(geracao, melhor, label="Melhor")
#     plt.plot(geracao, pior, label="Pior")
#     plt.plot(geracao, medio, label="Medio")
#     plt.legend()
#     plt.show()

#     # Exibe os indivíduos finalistas (melhor, pior e mediano)
#     imprime_melhor()
#     imprime_pior()
#     imprime_medio()
#--------------------------------------------------
# import sys
# import numpy as np
# from numpy import random
# import pandas as pd
# import matplotlib.pyplot as plt
# from typing import Final

# # Constantes para o problema da dieta
# OBJETIVO_CALORIAS: Final[int] = 2000
# TAM_POP: Final[int] = 20  # Número de indivíduos na população
# TAM_CROMO: Final[int] = 10  # Número de alimentos selecionados por indivíduo

# # Matrizes para armazenar a população e os resultados
# pop = np.zeros((TAM_POP, TAM_CROMO))
# nova_pop = np.zeros((TAM_POP, TAM_CROMO))
# pais = np.zeros((2, TAM_CROMO))
# filhos = np.zeros((2, TAM_CROMO))
# nota_pop = np.zeros((TAM_POP, 3))

# # Carregar os dados do CSV
# alimentos_df = pd.read_csv('/Users/kadishsilva/Library/Mobile Documents/com~apple~CloudDocs/MyProfessionalCarrier/MyProjects/GitHub/diet-combinatorial-optimization-exercise/data/alimentos_nutricionais_10.csv', delimiter=';')


# def init_pop():
#     """
#     Inicializa a população com alimentos aleatórios.
#     """
#     global pop
#     for i in range(TAM_POP):
#         pop[i] = random.choice(alimentos_df['id'], TAM_CROMO)

# def avalia_pop():
#     """
#     Avalia a população com base na soma das calorias.
#     O objetivo é chegar o mais próximo de 2000 kcal.
#     """
#     global nota_pop
#     soma_apt = 0

#     for i in range(TAM_POP):
#         apt = 0
#         total_calorias = 0
#         for j in range(TAM_CROMO):
#             alimento_id = int(pop[i][j])
#             calorias = alimentos_df[alimentos_df['id'] == alimento_id]['calories'].values[0]
#             total_calorias += calorias

#         apt = abs(OBJETIVO_CALORIAS - total_calorias)  # Quanto mais próximo de 2000, menor a aptidão
#         nota_pop[i][0] = i
#         nota_pop[i][1] = apt
#         nota_pop[i][2] = -1
#         soma_apt += apt

#     # Ordenar pela aptidão (menor é melhor)
#     nota_pop = nota_pop[nota_pop[:, 1].argsort()]

#     # Calcular a probabilidade inversamente proporcional à aptidão
#     minsum = 0
#     for i in range(TAM_POP):
#         if soma_apt > 0 and nota_pop[i][1] > 0:
#             nota_pop[i][2] = ((1 / nota_pop[i][1]) / soma_apt) * 100
#         else:
#             nota_pop[i][2] = 0
#         minsum += nota_pop[i][2]

#     # Normalizar para que a soma seja 100%
#     for i in range(TAM_POP):
#         if minsum > 0:
#             nota_pop[i][2] /= minsum
#         else:
#             nota_pop[i][2] = 0

# def seleciona_pais():
#     global pais

#     r_pai1 = random.random_sample(size=None)
#     r_pai2 = random.random_sample(size=None)

#     acum = 0
#     for i in range(TAM_POP):
#         acum += nota_pop[i][2]
#         if acum >= r_pai1:
#             pais[0] = pop[nota_pop[i][0].astype(int)]
#             break

#     acum = 0
#     for i in range(TAM_POP):
#         acum += nota_pop[i][2]
#         if acum >= r_pai2:
#             pais[1] = pop[nota_pop[i][0].astype(int)]
#             break

# def cruza_pais():
#     global filhos

#     r_cruza = random.random_sample(size=None)
#     if r_cruza < 0.80:
#         corte = random.randint(low=0, high=TAM_CROMO-1)
#         filhos[0][:corte] = pais[0][:corte]
#         filhos[0][corte:] = pais[1][corte:]
#         filhos[1][corte:] = pais[0][corte:]
#         filhos[1][:corte] = pais[1][:corte]
#     else:
#         filhos[0] = pais[0]
#         filhos[1] = pais[1]

# def muta_filhos():
#     global filhos

#     for i in range(TAM_CROMO):
#         r_muta = random.random_sample(size=None)
#         if r_muta < 0.03:
#             filhos[0][i] = random.choice(alimentos_df['id'])
#         r_muta = random.random_sample(size=None)
#         if r_muta < 0.03:
#             filhos[1][i] = random.choice(alimentos_df['id'])

# def elitismo(qtde):
#     global nova_pop
#     for i in range(qtde):
#         nova_pop[i] = pop[nota_pop[i][0].astype(int)]

# def imprime_melhor():
#     melhor_indice = int(nota_pop[0][0])
#     melhor_calorias = 0
#     sys.stdout.write('Melhor plano de dieta: ')
#     for i in range(TAM_CROMO):
#         alimento_id = int(pop[melhor_indice][i])
#         alimento = alimentos_df[alimentos_df['id'] == alimento_id]['name'].values[0]
#         calorias = alimentos_df[alimentos_df['id'] == alimento_id]['calories'].values[0]
#         melhor_calorias += calorias
#         sys.stdout.write(f'{alimento} ({calorias} kcal), ')
#     print(f'\nTotal de calorias: {melhor_calorias}, Aptidão: {nota_pop[0][1]}')

# # Código principal
# if __name__ == '__main__':
#     init_pop()

#     for geracao in range(2000):
#         avalia_pop()

#         if nota_pop[0][1] == 0:
#             break

#         j = 4
#         elitismo(j)

#         while j < TAM_POP:
#             seleciona_pais()
#             cruza_pais()
#             muta_filhos()

#             nova_pop[j] = filhos[0]
#             nova_pop[j + 1] = filhos[1]
#             j += 2

#         pop = nova_pop.copy()

#     imprime_melhor()
#----------------------------------------------------------------------
# import random
# import numpy as np
# import pandas as pd

# # Carregar os dados dos alimentos
# alimentos_df = pd.read_csv('/Users/kadishsilva/Library/Mobile Documents/com~apple~CloudDocs/MyProfessionalCarrier/MyProjects/GitHub/diet-combinatorial-optimization-exercise/data/alimentos_nutricionais_10.csv', delimiter=';')
# print("Dados dos alimentos carregados:")
# print(alimentos_df)

# # Parâmetros do algoritmo genético
# TAM_POP = 50  # Tamanho da população
# N_GERACOES = 100  # Número de gerações
# TAM_CROMO = 10  # Número de alimentos no plano alimentar (cromossomo)

# # Função de cálculo de fitness (aptidão)
# def calcula_fitness(plano):
#     """
#     Calcula a aptidão de um plano alimentar com base nas calorias.
#     A aptidão será maior quanto mais próximo de 2000 kcal for o plano.
#     """
#     total_calorias = sum(alimentos_df.iloc[plano, 2])  # Acessa a coluna de calorias (índice 2)
#     return abs(2000 - total_calorias)  # Quanto menor a diferença de calorias, melhor

# # Seleção por torneio
# def seleciona_pais(populacao, aptidoes):
#     """
#     Seleção por torneio. Escolhe aleatoriamente dois indivíduos da população e seleciona o mais apto.
#     """
#     pais = []
#     for _ in range(2):  # Seleciona dois pais
#         torneio = random.sample(range(len(populacao)), 3)  # Seleciona 3 indivíduos aleatórios
#         melhores = sorted(torneio, key=lambda i: aptidoes[i])[:2]  # Seleciona os dois melhores
#         pais.append(populacao[melhores[0]])
#     return pais

# # Função de cruzamento (crossover)
# def cruza_pais(pais):
#     """
#     Realiza o cruzamento entre dois pais para gerar dois filhos.
#     O corte é feito de forma aleatória no cromossomo.
#     """
#     corte = random.randint(1, len(pais[0]) - 1)
#     filho1 = np.concatenate((pais[0][:corte], pais[1][corte:]))
#     filho2 = np.concatenate((pais[1][:corte], pais[0][corte:]))
#     return [filho1, filho2]

# # Função de mutação
# def muta_plano(plano):
#     """
#     Aplica mutação no plano alimentar com 3% de chance para cada alimento.
#     """
#     for i in range(len(plano)):
#         if random.random() < 0.03:  # 3% de chance de mutação
#             plano[i] = random.randint(0, len(alimentos_df) - 1)
#     return plano

# # Função principal do algoritmo genético
# def main():
#     # Gerando população inicial
#     populacao = []
#     planos_testados = set()  # Conjunto para armazenar planos já testados (evitar repetição)
    
#     for _ in range(TAM_POP):
#         plano = np.random.randint(0, len(alimentos_df), TAM_CROMO)
#         while tuple(plano) in planos_testados:  # Se o plano já foi testado, gera um novo
#             plano = np.random.randint(0, len(alimentos_df), TAM_CROMO)
#         populacao.append(plano)
#         planos_testados.add(tuple(plano))  # Adiciona o plano ao conjunto de planos testados
    
#     for geracao in range(N_GERACOES):
#         print(f"Geração {geracao + 1} - Avaliando população...")
        
#         # Avalia a aptidão de cada plano alimentar
#         aptidoes = [calcula_fitness(plano) for plano in populacao]
        
#         # Encontra e imprime todos os planos que atingem 2000 kcal
#         planos_2000kcal = []
#         for i in range(len(populacao)):
#             if aptidoes[i] == 0:  # Plano com 2000 kcal
#                 planos_2000kcal.append(populacao[i])
        
#         if planos_2000kcal:
#             print(f"Planos alimentares com 2000 kcal na geração {geracao + 1}:")
#             for plano in planos_2000kcal:
#                 print(f"Plano: {plano} | Calorias: 2000")
        
#         # Criação da nova população
#         nova_populacao = []
#         for _ in range(TAM_POP // 2):  # Para cada par de pais
#             pais = seleciona_pais(populacao, aptidoes)  # Seleção dos pais
#             filhos = cruza_pais(pais)  # Cruzamento para gerar filhos
#             filhos = [muta_plano(filho) for filho in filhos]  # Aplica mutação nos filhos
            
#             # Verifica se os filhos gerados já foram testados e os gera novamente caso necessário
#             for filho in filhos:
#                 while tuple(filho) in planos_testados:  # Se o filho já foi testado, gera um novo
#                     filho = np.random.randint(0, len(alimentos_df), TAM_CROMO)
#                 nova_populacao.append(filho)
#                 planos_testados.add(tuple(filho))  # Adiciona o filho ao conjunto de planos testados
        
#         populacao = nova_populacao  # Substitui a população atual pela nova
    
#     print("\nFim das gerações!")

# # Rodar a função principal
# main()

#########################################
import random
import numpy as np
import pandas as pd

# Carregar os dados dos alimentos
alimentos_df = pd.read_csv('/Users/kadishsilva/Library/Mobile Documents/com~apple~CloudDocs/MyProfessionalCarrier/MyProjects/GitHub/diet-combinatorial-optimization-exercise/data/alimentos_nutricionais_10.csv', delimiter=';')
print("Dados dos alimentos carregados:")
print(alimentos_df)

# Parâmetros do algoritmo genético
TAM_POP = 50  # Tamanho da população
N_GERACOES = 100  # Número de gerações
TAM_CROMO = 10  # Número de alimentos no plano alimentar (cromossomo)

# Função de cálculo de fitness (aptidão)
def calcula_fitness(plano):
    """
    Calcula a aptidão de um plano alimentar com base nas calorias.
    A aptidão será maior quanto mais próximo de 2000 kcal for o plano.
    """
    total_calorias = sum(alimentos_df.iloc[plano, 2])  # Acessa a coluna de calorias (índice 2)
    return abs(2000 - total_calorias)  # Quanto menor a diferença de calorias, melhor

# Seleção por torneio
def seleciona_pais(populacao, aptidoes):
    """
    Seleção por torneio. Escolhe aleatoriamente dois indivíduos da população e seleciona o mais apto.
    """
    pais = []
    for _ in range(2):  # Seleciona dois pais
        torneio = random.sample(range(len(populacao)), 3)  # Seleciona 3 indivíduos aleatórios
        melhores = sorted(torneio, key=lambda i: aptidoes[i])[:2]  # Seleciona os dois melhores
        pais.append(populacao[melhores[0]])
    return pais

# Função de cruzamento (crossover)
def cruza_pais(pais):
    """
    Realiza o cruzamento entre dois pais para gerar dois filhos.
    O corte é feito de forma aleatória no cromossomo.
    """
    corte = random.randint(1, len(pais[0]) - 1)
    filho1 = np.concatenate((pais[0][:corte], pais[1][corte:]))
    filho2 = np.concatenate((pais[1][:corte], pais[0][corte:]))
    return [filho1, filho2]

# Função de mutação
def muta_plano(plano):
    """
    Aplica mutação no plano alimentar com 3% de chance para cada alimento.
    """
    for i in range(len(plano)):
        if random.random() < 0.03:  # 3% de chance de mutação
            plano[i] = random.randint(0, len(alimentos_df) - 1)
    return plano

# Função para converter os índices de um plano em nomes de alimentos
def converte_para_nomes(plano):
    return [alimentos_df.iloc[i]['name'] for i in plano]

# Função para calcular a quantidade de gramas necessária de cada alimento para atingir 2000 kcal
def calcula_quantidade_gramas(plano):
    quantidades = []
    total_calorias = sum(alimentos_df.iloc[plano, 2])  # Calorias totais do plano
    fator_calorias = 2000 / total_calorias  # Fator para ajustar as calorias para 2000 kcal
    
    for i in plano:
        quantidade_gramas = alimentos_df.iloc[i]['calories'] * fator_calorias  # Ajuste por grama
        quantidades.append((alimentos_df.iloc[i]['name'], quantidade_gramas))
    
    return quantidades, total_calorias  # Retorna também o total de calorias do plano

# Função principal do algoritmo genético
def main():
    # Gerando população inicial
    populacao = []
    planos_testados = set()  # Conjunto para armazenar planos já testados (evitar repetição)
    
    for _ in range(TAM_POP):
        plano = np.random.randint(0, len(alimentos_df), TAM_CROMO)
        while tuple(plano) in planos_testados:  # Se o plano já foi testado, gera um novo
            plano = np.random.randint(0, len(alimentos_df), TAM_CROMO)
        populacao.append(plano)
        planos_testados.add(tuple(plano))  # Adiciona o plano ao conjunto de planos testados
    
    planos_2000kcal_geracoes = []  # Lista para armazenar os planos com 2000 kcal em cada geração
    
    for geracao in range(N_GERACOES):
        print(f"Geração {geracao + 1} - Avaliando população...")
        
        # Avalia a aptidão de cada plano alimentar
        aptidoes = [calcula_fitness(plano) for plano in populacao]
        
        # Encontra e armazena todos os planos que atingem 2000 kcal
        planos_2000kcal = []
        for i in range(len(populacao)):
            if aptidoes[i] == 0:  # Plano com 2000 kcal
                planos_2000kcal.append(populacao[i])
        
        if planos_2000kcal:
            print(f"Planos alimentares com 2000 kcal na geração {geracao + 1}:")
            for plano in planos_2000kcal:
                nomes_alimentos = converte_para_nomes(plano)  # Converte os índices para nomes
                quantidades, total_calorias = calcula_quantidade_gramas(plano)  # Calcula as quantidades de gramas e total de calorias
                print(f"Plano: {nomes_alimentos} | Total Calorias: {total_calorias}")
                planos_2000kcal_geracoes.append((geracao + 1, nomes_alimentos, quantidades, total_calorias))
        
        # Criação da nova população
        nova_populacao = []
        for _ in range(TAM_POP // 2):  # Para cada par de pais
            pais = seleciona_pais(populacao, aptidoes)  # Seleção dos pais
            filhos = cruza_pais(pais)  # Cruzamento para gerar filhos
            filhos = [muta_plano(filho) for filho in filhos]  # Aplica mutação nos filhos
            
            # Verifica se os filhos gerados já foram testados e os gera novamente caso necessário
            for filho in filhos:
                while tuple(filho) in planos_testados:  # Se o filho já foi testado, gera um novo
                    filho = np.random.randint(0, len(alimentos_df), TAM_CROMO)
                nova_populacao.append(filho)
                planos_testados.add(tuple(filho))  # Adiciona o filho ao conjunto de planos testados
        
        populacao = nova_populacao  # Substitui a população atual pela nova
    
    # Após todas as gerações, imprime todos os planos alimentares encontrados
    print("\nPlanos alimentares com 2000 kcal em todas as gerações:")
    for geracao, nomes, quantidades, total_calorias in planos_2000kcal_geracoes:
        print('')
        print(f"-------------- Geração {geracao} --------------")
        print(f"Plano: {nomes} | Total Calorias: {total_calorias}")
        print(f"-------------- Gramas / Alimentos --------------")
        for nome, quantidade in quantidades:
            print(f"{nome}: {quantidade:.2f} g")

# Rodar a função principal
main()














