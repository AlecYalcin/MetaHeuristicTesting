import sys 
import random 

class Item():
    def __init__(
        self,
        value: int,
        weight: int,
        name: str = ""
    ):
        self.value = value
        self.weight = weight
        self.name = name

    def __str__(self):
        return f"Item {self.name}: w={self.weight}, v={self.value}"

class Knapsack():
    class LimitExceeded(Exception):
        def __init__(self, message="Limite de peso ultrapasado."):
            super().__init__(message)

    def __init__(
        self,
        limit: int,
        items: list[Item] = ...,
    ):
        self.limit = limit
        self.items = items if isinstance(items, list) else [] 

        self.weight = 0
        self.value = 0
        for item in items: 
            if item.weight + self.weight > limit:
                raise self.LimitExceeded()
            else:
                self.weight = self.weight + item.weight
                self.value = self.value + item.value

    def __len__(self):
        return len(self.items)

    def add(self, item: Item):
        if item.weight + self.weight > self.limit:
            raise self.LimitExceeded()
        else:
            self.items.append(item)
            self.weight += item.weight
            self.value += item.value 
    
    def recalculate(self):
        self.weight = 0
        self.value = 0
        for item in self.items: 
            if item.weight + self.weight > self.limit:
                raise self.LimitExceeded()
            else:
                self.weight = self.weight + item.weight
                self.value = self.value + item.value

    def show(self):
        print("Dentro da Mochila:")
        for item in self.items:
            print(item, end=",\n")
        print("Peso Total: ", self.weight)
        print("Limite: ", self.limit)
        print("Valor Total: ", self.value)

    @staticmethod
    def generate( 
        n: int = 10, 
        w_range: range = ..., 
        v_range: range = ...,
    ):
        """ Função geradora de itens para uma mochila. Devolve os itens e o limite da mochila proposta. """

        if w_range == ...:
            w_range = range(1, n)
        if v_range == ...:
            v_range = range(1, n)
        
        items = []
        total = 0
        while len(items) < n:
            new_item = Item(
                value=random.choice(v_range),
                weight=random.choice(w_range),
                name=f"{len(items)}"
            )
            total += new_item.weight
            items.append(new_item)

        limit = (0.3 + random.random()*0.3) * total
        return (int(limit), items)
        
# Geração de Benchmarks do KP
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "./kp.py <n> <archive>"
            "<n> - quantidade de itens na mochila "
            "<archive> - nome do arquivo para salvar"
        )
    else:
        n = int(sys.argv[1])
        archive = sys.argv[2]
        with open(archive, "w") as f:
            for _ in range(10):
                while True:
                    limit, items = Knapsack.generate(n)
                    try:
                        knapsack = Knapsack(limit, items)
                    except Knapsack.LimitExceeded:
                        break
                f.write(f"{[(item.weight, item.value, item.name) for item in items]};{limit}\n")