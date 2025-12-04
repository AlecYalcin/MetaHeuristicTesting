import sys
from tsp import (
    Grid,
    Point,
    total_distance,
)

def _update_tabu_list(
    tabu_list: dict[tuple[int, int], int],
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

def select_best_solution_tsp(
    best_solution: list[Point],
    solution: list[Point]
) -> list[Point]:
    if total_distance(best_solution) > total_distance(solution):
        return solution
    return best_solution

def _2opt_invert(
    points: list[Point],
    i: int,
    j: int,
) -> list[Point]:
    return points[:i] + list(reversed(points[i:j+1])) + points[j+1:]

def generate_candidates(
    solution: list[Point],
    best_solution: list[Point],
    tabu_list: dict[tuple[int, int], int],
) -> tuple[list[Point] | None, int | None]:
    best_candidate = None
    best_movement = None
    best_cost = float('inf')

    for i in range(0, len(solution)-2):
        for j in range(i+2, len(solution)):
            current_solution = _2opt_invert(solution.copy(), i, j)
            current_cost = total_distance(current_solution)

            is_not_tabu = tabu_list.get((i, j), 0) <= 0
            is_aspiration = current_cost <= total_distance(best_solution)
            
            if (
                (is_not_tabu or is_aspiration)
                and current_cost < best_cost
            ):
                best_cost = current_cost
                best_candidate = current_solution
                best_movement = (i, j)
    if best_candidate is None:
        return solution, None
    return best_candidate, best_movement


def tabu_search_tsp(
    points: list[Point],
    max_retry: int = 10,
    tabu_time: int = 10,
):
    solution = points.copy()
    best_solution = solution
    tabu_list = {}

    while max_retry > 0:
        solution, movement = generate_candidates(solution, best_solution, tabu_list)
        _update_tabu_list(tabu_list, tabu_time, movement)
        best_solution = select_best_solution_tsp(best_solution, solution)
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
                grid = Grid.generate(int(sys.argv[1]))
            case str():
                grid = Grid.import_maps(parameter)[0]
        best = tabu_search_tsp(grid.points)
        print(total_distance(best))