import sys
from base import (
    Item,
    Knapsack
)

from kp_brute import knapsack_combinations

def _update_tabu_list(
    tabu_list: dict[tuple[int, str, str], int],
    tabu_time: int,
    new_movement: tuple[int, int] | None,
):
    remove_list = []
    for tabu_movement, time in tabu_list.items():
        tabu_list[tabu_movement] = time - 1
        if tabu_list[tabu_movement] <= 0:
            remove_list.append(tabu_movement)
    
    for movement in remove_list:
        tabu_list.pop(movement)

    if new_movement != None:
        tabu_list[new_movement] = tabu_time

def select_best_solution_kp(
    best_solution: Knapsack,
    solution: Knapsack
) -> Knapsack:
    if best_solution.value < solution.value:
        return solution
    return best_solution

def player_substitution(
    solution: Knapsack,
    items: list[Item],
    starting_index: int,
) -> tuple[Knapsack, tuple[int, str, str] | None]:
    new_solution = Knapsack(limit=solution.limit, items=solution.items.copy())
    l_remaining = new_solution.limit - new_solution.weight
    for i_item in range(starting_index, len(new_solution.items)):
        old_item = new_solution.items[i_item]
        for item in items:
            if (
                item not in new_solution.items
                and item.weight - l_remaining <= old_item.weight
                and item.value > old_item.value
            ):
                new_solution.weight += item.weight - old_item.weight
                new_solution.value += item.value - old_item.value
                new_solution.items[i_item] = item
                return new_solution, (i_item, old_item.name, item.name)
    return new_solution, None

def generate_candidates(
    solution: Knapsack,
    best_solution: Knapsack,
    items: list[Item],
    tabu_list: dict[tuple[int, int], int],
) -> tuple[Knapsack | None, int | None]:
    best_candidate = None
    best_movement = None
    best_cost = 0
    
    for i in range(10):
        current_solution, movement = player_substitution(solution, items, i)
        if movement is None:
            continue
        current_cost = current_solution.value

        is_not_tabu = tabu_list.get(movement, 0) <= 0
        is_aspiration = current_cost >= best_solution.value
        
        if (
            (is_not_tabu or is_aspiration)
            and current_cost > best_cost
        ):
            best_cost = current_cost
            best_candidate = current_solution
            best_movement = movement
    if best_candidate is None:
        return solution, None
    return best_candidate, best_movement


def tabu_search_kp(
    limit: int,
    items: list[Item],
    max_retry: int = 10,
    tabu_time: int = 10,
):
    solution = Knapsack(limit=limit)
    for item in items:
        try:
            solution.add(item)
        except Knapsack.LimitExceeded:
            break
    best_solution = solution
    tabu_list = {}

    while max_retry > 0:
        solution, movement = generate_candidates(solution, best_solution, items, tabu_list)
        _update_tabu_list(tabu_list, tabu_time, movement)
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
        best = tabu_search_kp(limit, items)
        print(best.value)