import random

# Parâmetros do algoritmo
TAMANHO_POPULACAO = 100
TAXA_MUTACAO = 0.01
MAX_GERACOES = 1000
META_CALORICA = 2000  # Meta calórica para opção 1 e 3
META_CALORICA_MIN = 200  # Meta calórica para opção 2
NUM_ALIMENTOS = 10  # Número de alimentos na dieta
MIN_GRAMAS = 50  # Mínimo de gramas por alimento

# Estrutura para armazenar informações sobre alimentos
class Alimento:
    def __init__(self, nome, kcal_por_100g, carboidratos_por_100g, proteinas_por_100g, gorduras_por_100g):
        self.nome = nome
        self.kcal_por_100g = kcal_por_100g
        self.carboidratos_por_100g = carboidratos_por_100g
        self.proteinas_por_100g = proteinas_por_100g
        self.gorduras_por_100g = gorduras_por_100g

# Lista de alimentos reais
alimentos = [
    Alimento("Frango grelhado", 165, 0, 31, 3.6),
    Alimento("Arroz integral", 111, 23, 2.6, 0.9),
    Alimento("Brócolis", 34, 7, 2.8, 0.4),
    Alimento("Batata doce", 86, 20.1, 1.6, 0.1),
    Alimento("Ovo", 155, 1.1, 13, 11),
    Alimento("Lentilha cozida", 116, 20.1, 9, 0.4),
    Alimento("Maçã", 52, 14, 0.3, 0.2),
    Alimento("Queijo cheddar", 402, 1.3, 25, 33),
    Alimento("Iogurte natural", 61, 4.7, 3.5, 3.3),
    Alimento("Salmão", 206, 0, 22, 13),
]

# Estrutura para armazenar a dieta
class Cromossomo:
    def __init__(self):
        # Garantindo que cada alimento tenha pelo menos 50 gramas
        self.quantidades = [random.randint(MIN_GRAMAS, 500) for _ in range(NUM_ALIMENTOS)]

# Função para calcular as calorias totais de um cromossomo
def calcular_calorias(cromossomo):
    total_calorias = sum(cromossomo.quantidades[i] * alimentos[i].kcal_por_100g / 100 for i in range(NUM_ALIMENTOS))
    return total_calorias

# Função para calcular a distribuição de macronutrientes
def calcular_macronutrientes(cromossomo):
    total_carboidratos = sum(cromossomo.quantidades[i] * alimentos[i].carboidratos_por_100g / 100 for i in range(NUM_ALIMENTOS))
    total_proteinas = sum(cromossomo.quantidades[i] * alimentos[i].proteinas_por_100g / 100 for i in range(NUM_ALIMENTOS))
    total_gorduras = sum(cromossomo.quantidades[i] * alimentos[i].gorduras_por_100g / 100 for i in range(NUM_ALIMENTOS))
    return total_carboidratos, total_proteinas, total_gorduras

# Função para calcular a função de fitness de um cromossomo
def calcular_fitness(cromossomo, opcao):
    total_calorias = calcular_calorias(cromossomo)
    carboidratos, proteinas, gorduras = calcular_macronutrientes(cromossomo)

    # Calcular a porcentagem de cada macronutriente
    total_macronutrientes = carboidratos + proteinas + gorduras
    if total_macronutrientes == 0:  # Evitar divisão por zero
        return float('inf')  # Penalizar soluções sem macronutrientes

    carboidratos_percent = (carboidratos * 4 / total_macronutrientes) * 100
    proteinas_percent = (proteinas * 4 / total_macronutrientes) * 100
    gorduras_percent = (gorduras * 9 / total_macronutrientes) * 100

    # Calcular penalidades
    penalidade_calorias = 0
    if opcao == 1:  # Maximizar gramas para 2000 kcal
        if total_calorias < META_CALORICA:
            penalidade_calorias = META_CALORICA - total_calorias
    elif opcao == 2:  # Minimizar gramas para 200 kcal
        if total_calorias > META_CALORICA_MIN:
            penalidade_calorias = total_calorias - META_CALORICA_MIN

    penalidade_macronutrientes = abs(30 - carboidratos_percent) + abs(30 - proteinas_percent) + abs(30 - gorduras_percent)

    # Fitness total (quanto menor, melhor)
    fitness = penalidade_calorias + penalidade_macronutrientes
    return fitness

# Função para gerar a população inicial
def gerar_populacao_inicial():
    populacao = [Cromossomo() for _ in range(TAMANHO_POPULACAO)]
    return populacao

# Função para selecionar os melhores cromossomos
def selecionar(populacao, opcao):
    # Ordena a população com base na fitness (menor é melhor)
    populacao.sort(key=lambda cromossomo: calcular_fitness(cromossomo, opcao))
    return populacao[:TAMANHO_POPULACAO // 2]  # Retorna os melhores 50%

# Função para cruzar dois cromossomos
def crossover(pai1, pai2):
    filho = Cromossomo()
    for i in range(NUM_ALIMENTOS):
        filho.quantidades[i] = pai1.quantidades[i] if random.random() > 0.5 else pai2.quantidades[i]
    return filho

# Função para mutação
def mutacao(cromossomo):
    for i in range(NUM_ALIMENTOS):
        if random.random() < TAXA_MUTACAO:
            # Altera a quantidade aleatoriamente, garantindo que a quantidade mínima ainda seja respeitada
            nova_quantidade = random.randint(0, 500)
            cromossomo.quantidades[i] = max(nova_quantidade, MIN_GRAMAS)  

# Função principal do algoritmo genético
def algoritmo_genetico(opcao):
    populacao = gerar_populacao_inicial()
    
    for geracao in range(MAX_GERACOES):
        nova_populacao = selecionar(populacao, opcao)
        
        # Cruzamento e geração da nova população
        while len(nova_populacao) < TAMANHO_POPULACAO:
            pai1, pai2 = random.sample(nova_populacao, 2)  # Seleciona dois pais aleatoriamente
            filho = crossover(pai1, pai2)
            mutacao(filho)
            nova_populacao.append(filho)

        populacao = nova_populacao  # Atualiza a população para a próxima geração

    # Retorna o melhor cromossomo encontrado
    melhor_cromossomo = min(populacao, key=lambda cromossomo: calcular_fitness(cromossomo, opcao))
    return melhor_cromossomo

# Função para imprimir os resultados
def imprimir_resultados(cromossomo, opcao):
    print(f"\nMelhor dieta para opção {opcao}:")

    for i in range(NUM_ALIMENTOS):
        if cromossomo.quantidades[i] > 0:
            alimento = alimentos[i]
            print(f"{alimento.nome}: {cromossomo.quantidades[i]} gramas")

# Execução do algoritmo para as três opções
for opcao in range(1, 4):
    melhor_dieta = algoritmo_genetico(opcao)
    imprimir_resultados(melhor_dieta, opcao)
