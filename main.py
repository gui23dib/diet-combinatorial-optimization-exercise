from fetcher import fetch_food_data

def get_user_input() -> int:
    print("ESCOLHA SEU PLANO:")
    print("1 - perder peso\n2 - manutenção de peso\n3 - ganhar peso")
    choice = int(input("Digite a opção desejada: "))
    return 1200 + 400 * choice

if __name__ == '__main__':
    data = fetch_food_data(True)

    obj_kcal = get_user_input()
    carb, prot, fat = (0.5, 0.2, 0.3) # melhorar isso aq por input

    refeicoes = [(None, 0.3), (None, 0.5), (None, 0.2)] # 3 refeicoes

    for refeicao, distribucao in refeicoes:
        pass
