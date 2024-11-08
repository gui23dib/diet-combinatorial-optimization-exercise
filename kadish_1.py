import random

# Definição dos alimentos e suas calorias por 100 gramas
alimentos = {
    'ovo': 20,
    'frango': 200,
    'leite': 500,
    'arroz': 1000,
    'banana': 10
}

meta_calorias = 2000
tamanho_populacao = 100
taxa_mutacao = 0.1

# Função de avaliação (fitness) - Quanto mais perto de 2000 kcal, melhor
def calcular_calorias(dieta):
    total_calorias = sum([alimentos[alimento] * quantidade / 100 for alimento, quantidade in dieta.items()])
    return abs(meta_calorias - total_calorias), total_calorias

# Inicialização da população - cada indivíduo é uma dieta com quantidades aleatórias de cada alimento
def criar_populacao():
    populacao = []
    for _ in range(tamanho_populacao):
        dieta = {alimento: random.randint(0, 20) * 100 for alimento in alimentos}
        populacao.append(dieta)
    return populacao

# Seleção - Seleciona as dietas com menor valor de fitness
def selecionar(populacao):
    populacao_classificada = sorted(populacao, key=lambda dieta: calcular_calorias(dieta)[0])
    return populacao_classificada[:tamanho_populacao//2]  # Mantém as melhores 50%

# Crossover - Combina dietas para criar novas
def cruzar(pai, mae):
    filho = {}
    for alimento in alimentos:
        filho[alimento] = pai[alimento] if random.random() > 0.5 else mae[alimento]
    return filho

# Mutação - Aleatoriamente altera as quantidades de algum alimento
def mutacao(dieta):
    if random.random() < taxa_mutacao:
        alimento_aleatorio = random.choice(list(alimentos.keys()))
        dieta[alimento_aleatorio] = random.randint(0, 20) * 100
    return dieta

# Algoritmo genético
def algoritmo_genetico():
    populacao = criar_populacao()
    geracao = 0

    while True:
        # Avaliar e selecionar os melhores
        populacao = selecionar(populacao)

        # Imprimir a geração e a melhor dieta
        melhor_dieta = populacao[0]
        diferenca_calorias, total_calorias = calcular_calorias(melhor_dieta)
        print(f"Geração {geracao}: Dieta {melhor_dieta}, Calorias: {total_calorias} kcal, Diferença: {diferenca_calorias} kcal")

        # Se encontrar uma dieta com exatamente 2000 kcal, encerra o algoritmo
        if total_calorias == 2000:
            print(f"\nDieta perfeita encontrada na geração {geracao}: {melhor_dieta}, Calorias: {total_calorias} kcal")
            break

        # Gerar novos indivíduos por crossover
        novos_individuos = []
        while len(novos_individuos) < tamanho_populacao - len(populacao):
            pai, mae = random.sample(populacao, 2)
            filho = cruzar(pai, mae)
            filho = mutacao(filho)
            novos_individuos.append(filho)

        # Atualizar a população com os novos indivíduos
        populacao.extend(novos_individuos)
        geracao += 1

# Rodar o algoritmo genético
algoritmo_genetico()
