import sys
import random
from tsp import (
    Grid,
    Point,
    total_distance,
    euclidean_distance,
)

def select_best_solution_tsp(
    best_solution: list[Point],
    solution: list[Point]
) -> list[Point]:
    if total_distance(best_solution) > total_distance(solution):
        return solution
    return best_solution

def _make_rcl(
    random_factor: float,
    points: list[Point],
    current: Point,
) -> list[Point]:
    
    # Construção de possibilidades 
    possibilities = []
    for p in points:
        d = euclidean_distance(current, p)
        possibilities.append((p, d))
    possibilities.sort(key= lambda c: c[1])

    # Calculando limite RCL
    min_distance = possibilities[0][1]
    max_distance = possibilities[-1][1]
    rcl_limit = min_distance + random_factor * (max_distance - min_distance)

    # Criando lista RCL
    candidates = [
        point 
        for point, distance in possibilities
        if distance <= rcl_limit
    ]

    # Lista final apenas com os melhores candidatos
    return candidates

def _select_random_element(
    candidates: list[Point],
) -> Point:
    return random.choice(candidates)

def _adapt_greedy_solution(
    selected: Point,
    points: list[Point]
) -> None:
    points.remove(selected)

def construct_solution(
    points: list[Point],
    random_factor: float,
) -> list[Point]:
    current = points.pop(random.randint(0, len(points)-1))
    solution = [current]
    while points:
        candidates = _make_rcl(random_factor, points, current)
        selected = _select_random_element(candidates)
        solution.append(selected)
        _adapt_greedy_solution(selected, points)
        current = selected
    return solution

def _2opt_invert(
    points: list[Point],
    i: int,
    j: int,
) -> list[Point]:
    return points[:i] + list(reversed(points[i:j+1])) + points[j+1:]

def local_search(
    solution: list[Point]      
):
    improved = True
    while improved:
        improved = False
        for i in range(0, len(solution)-2):
            for j in range(i+2, len(solution)):
                new_route = _2opt_invert(solution.copy(), i, j)
                if total_distance(new_route) < total_distance(solution):
                    solution = new_route
                    improved = True
    return solution

def grasp_tsp(
    points: list[Point],
    max_retry: int = 10,
    random_factor: float = 0.2,
) -> list[Point]:
    best_solution = points
    while max_retry > 0:
        solution = construct_solution(points.copy(), random_factor)
        solution = local_search(solution)
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
        best = grasp_tsp(grid.points)
        print(total_distance(best))