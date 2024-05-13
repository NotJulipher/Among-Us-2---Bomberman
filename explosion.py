from enums.power_up_type import TipoPowerUp
from power_up import Potenciador


class Explosion:

    bombero = None

    def __init__(self, x, y, r):
        self.fuenteX = x
        self.fuenteY = y
        self.alcance = r
        self.tiempo = 300
        self.fotograma = 0
        self.sectores = []

    def explotar(self, mapa, bombas, b, power_ups):

        self.bombero = b.bombero
        self.sectores.extend(b.sectores)
        bombas.remove(b)
        self.cadena_de_bombas(bombas, mapa, power_ups)

    def cadena_de_bombas(self, bombas, mapa, power_ups):

        for s in self.sectores:
            for x in power_ups:
                if x.pos_x == s[0] and x.pos_y == s[1]:
                    power_ups.remove(x)

            for x in bombas:
                if x.pos_x == s[0] and x.pos_y == s[1]:
                    mapa[x.pos_x][x.pos_y] = 0
                    x.bombero.limite_bombas += 1
                    self.explotar(mapa, bombas, x, power_ups)

    def limpiar_sectores(self, mapa, aleatorio, power_ups):

        for i in self.sectores:
            if mapa[i[0]][i[1]] == 2:
                r = aleatorio.randint(0, 9)
                if r == 0:
                    power_ups.append(Potenciador(i[0], i[1], TipoPowerUp.BOMBA))
                elif r == 1:
                    power_ups.append(Potenciador(i[0], i[1], TipoPowerUp.FUEGO))

            mapa[i[0]][i[1]] = 0

    def actualizar(self, dt):

        self.tiempo = self.tiempo - dt

        if self.tiempo < 100:
            self.fotograma = 2
        elif self.tiempo < 200:
            self.fotograma = 1
