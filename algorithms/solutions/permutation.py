import sys
from ..tsp import (
    Grid,
    Point,
    total_distance,
)

def _permutation(
    symbols: list[any],
    index: int = 0, 
    memory: list = ...,
    results: list = ...,
) -> list[list[any]]:
    """ Algoritmo de permutação que gera todas as possibilidades dentre os símbolos passados. """

    # Inicialização memória
    if memory == ...:
        memory = [-1] * len(symbols)
    if results == ...:
        results = []

    # Percorrendo os símbolos enquanto o índice não for maior que o tamanho da memória
    if index < len(memory):
        for i in range(len(symbols)):
            memory[index] = symbols[i]
            new_symbols = symbols[:i] + symbols[i+1:]
            results = _permutation(symbols=new_symbols, memory=memory, index=index + 1, results=results)
    else:
        results.append(memory.copy())
    
    # Devolvendo os resultados para a próxima iteração
    return results

def traveler_permutations(points: list[Point]) -> list[Point]:
    """ 
    Algoritmo que realiza a permutação de todos os pontos e encontra aquele com a menor distância euclidiana seguindo
    o camino do caixeiro viajante.
    """

    # Gerando permutações
    permutations: list[list[Point]] = _permutation(points)

    # Percorrendo permutações
    best_distance, best_permutation = total_distance(permutations[0]), permutations[0]
    for permutation in permutations[1:]:
        current_distance = total_distance(permutation)
        if current_distance < best_distance:
            best_permutation, best_distance = permutation, current_distance
    
    best_permutation.append(best_permutation[0])
    return best_permutation

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "./grid.py <n> or <archive>\n"
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
                grid = Grid.generate(int(sys.argv[1]))
            case str():
                grid = Grid.import_maps(parameter)[0]
        best = traveler_permutations(grid.points)
        print(total_distance(best))