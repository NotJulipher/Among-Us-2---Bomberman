class Nodo:

    padre = None
    peso = None
    direccion = 1

    def __init__(self, px, py, alcance, peso_base, valor):
        self.x = px
        self.y = py
        self.alcance = alcance
        self.peso_base = peso_base
        self.valor = valor

