import sys
from base import (
    Item,
    Knapsack
)

def _combinations(
    listing: list[any],
    t: int = 1,
    fixed: list[any] = ...,
    results: list[list[any]] = ...,
) -> list[list[any]]:
    """ 
    Algoritmo de combinação que gera todas as possibilidaes dentr os símbolos passados. 
    
    Args:
        results (list[list]) Lista final de combinações
        listing (list): Lista de elementos quaisquer 
        t (int): Tamanho da lista a ser produzida 
        fixed (list): Combinação mínima atual
    """

    if fixed == ...:
        fixed = []
    if results == ...:
        results = []

    # print(listing, fixed)
    for i in range(len(listing)):
        current = fixed + [listing[i]]
        results.append(current)
        results = _combinations(
            results=results,
            listing=listing[i+1:],
            fixed=current,
            t=t+1,
        )

    return results

def knapsack_combinations(items: list[Item], limit: int) -> Knapsack:
    """
    Algoritmo que realiza a combinação de todos os itens e encontra aquela com o 
    maior valor e que não ultrapasse o limite proposto.
    """    

    # Gerando combinações
    combinations = _combinations(items)

    # Escolhendo combinação com melhor custo_beneficio
    best_knapsack = Knapsack(limit=limit, items=[])
    for c in combinations:
        try:
            knapsack = Knapsack(limit=limit, items=c)
            if knapsack.value > best_knapsack.value:
                best_knapsack = knapsack
        except Knapsack.LimitExceeded:
            pass

    return best_knapsack


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "./tsp.py <n>  or <archive>"
            "<n> - quantidade de pontos na grid "
            "<archive> - arquivo de importação"
        )
    else:
        try:
            parameter = eval(sys.argv[1])
        except Exception:
            parameter = sys.argv[1]
        match parameter:
            case int():     
                limit, items = Knapsack.generate(int(sys.argv[1]))
            # case str():
                # grid = Knapsack.import_maps(parameter)[0]
        best = knapsack_combinations(items, limit)
        print(best.value)