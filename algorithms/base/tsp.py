import sys
import math
import random

LATITUDE = (-90, 90)
LONGITUDE  = (-180, 180)

def scale(value: float, limits: tuple[int, int]):
    """ Função para normalizar valores aleatórios em LONGITUDE/LATITUDE """
    _min, _max = limits
    return value * (_max - _min) + _min

class Point():
    def __init__(self, 
        longitude: float, 
        latitude: float,
        name: str = ""
    ):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
    
    def __str__(self) -> str:
        return f"Ponto {self.name}({self.longitude}°, {self.latitude}°)"

def euclidean_distance(p1: Point, p2: Point) -> float:
    """ Função para cálculo de distância euclidiana entre dois pontos """
    x_squared = (p2.latitude - p1.latitude) ** 2
    y_squared = (p2.longitude - p1.longitude) ** 2
    return math.sqrt((x_squared+y_squared))

def total_distance(points: list[Point]) -> float:
    """ Função que calcula a distância euclidiana dada uma lista de pontos do início ao início """
    d = 0
    for i in range(len(points)-1):
        d += euclidean_distance(points[i], points[i+1])
    return d + euclidean_distance(points[-1], points[0])

class Grid():
    """
    Classe utilizada para criar ou reconhecer grids. As grids são uma estrutura de lista com tuplas de latitude e longitude.
    Eles representam pontos em um plano de -180° até 180° de longitude e -90° até 90° de latitude. 
    """

    def __init__(self, points: list[Point]) -> None:
        """ Inicialização de uma Grid para visualização dos Pontos recebidos. """

        # Inicializando o mapa 360x180
        self.map = [["-" for _ in range(360)] for _ in range(180)]

        # Alocando os pontos
        for p in points:
            x = round(p.latitude) + 90 - 1
            y = round(p.longitude) + 180 - 1
            self.map[x][y] = p.name
        self.points = points

    @property
    def total_distance(self) -> float:
        """ Método para cálculo das distâncias baseado na ordem dos pontos dados. """

        d = 0
        for i in range(len(self.points)-1):
            d += euclidean_distance(self.points[i], self.points[i+1])
        return d + euclidean_distance(self.points[-1], self.points[0])

    def show(self) -> None:
        """ Método para mostrar a grid. """

        print("\n" + "#" * 50)
        print("Grid Points")
        for p in self.points:
            print(f"Point {p.name} -> Latitude: {p.latitude:.2f}, Longitude: {p.longitude:.2f}")
        print(f"Total Distance: {self.total_distance}")

    def __str__(self) -> None:
        return f"Points: {[str(p) for p in self.points]}"

    @classmethod
    def generate(cls, n: int) -> "Grid":
        """ Função geradora de uma Grid com pontos aleatórios conforme o valor passado. """

        # Alocando pontos aleatórios
        points = []
        while (n > 0):
            # Definindo valores aleatórios para X e Y
            x = round(scale(random.random(), LATITUDE), 2)
            y = round(scale(random.random(), LONGITUDE), 2)

            # Verificando se já não existe pontos iguais
            while (
                any(p.latitude == x and p.longitude == y for p in points)
            ):
                x = round(scale(random.random(), LATITUDE), 2)
                y = round(scale(random.random(), LONGITUDE), 2)

            # Criando ponto real 
            p = Point(latitude=x, longitude=y, name=f"P{n}")
            points.append(p)

            # Decrementando
            n = n -1

        return cls(points)
    
    @classmethod
    def import_maps(cls, arq: str) -> list["Grid"]:
        """ Método de importação de Grid com base em um arquivo. """

        # Lendo as linhas do arquivo
        with open(arq, "r") as f: 
            lines = f.readlines()

        # Transformando cada linha em uma lista
        lists = [eval(l.strip()) for l in lines]

        # Transformando cada lista em uma lista de pontos 
        grids: list[Grid] = []
        for points in lists:
            grids.append(Grid([
                Point(longitude, latitude, f"P{index}") 
                for index, (latitude, longitude) in enumerate(points)
            ]))

        return grids

# Geração de Benchmarks do TSP
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "./tsp.py <n> <archive>"
            "<n> - quantidade de pontos na grid "
            "<archive> - nome do arquivo para salvar"
        )
    else:
        n = int(sys.argv[1])
        archive = sys.argv[2]
        with open(archive, "w") as f:
            for _ in range(10):
                grid = Grid.generate(n)
                f.write(f"{[(p.latitude, p.longitude) for p in grid.points]}\n")