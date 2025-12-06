import sys
import random
from base import (
    Item,
    Knapsack
)

from kp_brute import knapsack_combinations

def select_best_solution_kp(
    best_solution: Knapsack,
    solution: Knapsack
) -> Knapsack:
    if solution.value > best_solution.value:
        return solution
    return best_solution

def _make_rcl(
    solution: Knapsack,
    random_factor: float,
    items: list[Item],
) -> list[Item]:
    
    # Construção de possibilidades 
    possibilities = []
    for i in items:
        if solution.weight + i.weight <= solution.limit:
            ratio = i.value/i.weight
            possibilities.append((i, ratio))
    
    if not possibilities:
        return []

    possibilities.sort(key= lambda c: c[1], reverse=True)

    # Calculando limite RCL
    min_ratio = possibilities[0][1]
    max_ratio = possibilities[-1][1]
    rcl_limit = min_ratio + random_factor * (max_ratio - min_ratio)

    # Criando lista RCL
    candidates = [
        item 
        for item, ratio in possibilities
        if ratio >= rcl_limit
    ]

    # Lista final apenas com os melhores candidatos
    return candidates

def _select_random_element(
    candidates: list[Item],
) -> Item:
    return random.choice(candidates)

def _adapt_greedy_solution(
    selected: Item,
    items: list[Item]
) -> None:
    items.remove(selected)

def construct_solution(
    limit: int,
    items: list[Item],
    random_factor: float,
) -> Knapsack:
    solution = Knapsack(limit=limit)
    while items:
        candidates = _make_rcl(solution, random_factor, items)
        if candidates:
            selected = _select_random_element(candidates)
            solution.add(selected)
            _adapt_greedy_solution(selected, items)
        else:
            break
    return solution

def player_substitution(
    solution: Knapsack,
    items: list[Item]
) -> Knapsack:
    new_solution = Knapsack(limit=solution.limit, items=solution.items.copy())
    for i_item in range(len(new_solution.items)):
        l_remaining = new_solution.limit - new_solution.weight
        if not items:
            break
        removed_item = None
        for item in items:
            if (
                item not in new_solution.items
                and item.weight - l_remaining <= new_solution.items[i_item].weight
                and item.value > new_solution.items[i_item].value
            ):
                new_solution.weight += item.weight - new_solution.items[i_item].weight
                new_solution.value += item.value - new_solution.items[i_item].value
                new_solution.items[i_item] = item
                l_remaining = new_solution.limit - new_solution.weight
                removed_item = item 
        if removed_item:
            items.remove(removed_item)
    return new_solution


def local_search(
    solution: Knapsack, items: list[Item]    
) -> Knapsack:
    improved = True
    while improved:
        improved = False
        new_solution = player_substitution(solution, items=items.copy())
        if new_solution.value > solution.value:
            solution = new_solution
            improved = True
    return solution

def grasp_kp(
    limit: int,
    items: list[Item],
    max_retry: int = 10,
    random_factor: float = 0.2,
) -> Knapsack:
    best_solution = Knapsack(limit=limit)
    while max_retry > 0:
        solution = construct_solution(limit, items.copy(), random_factor)
        solution = local_search(solution, items.copy())
        best_solution = select_best_solution_kp(best_solution, solution)
        max_retry = max_retry - 1
    return best_solution

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "./grid.py <n> or <archive>\n"
            "<n> - quantidade de pontos na grid "
            "<archive> - arquivo de importação"
        )
    else:
        parameter = eval(sys.argv[1])
        match parameter:
            case int():     
                limit, items = Knapsack.generate(int(sys.argv[1]))
            # case str():
                # grid = Knapsack.import_maps(parameter)[0]
        best = grasp_kp(limit, items)
        print(best.value)