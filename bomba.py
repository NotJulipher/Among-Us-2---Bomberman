class Bomba:
    fotograma = 0

    def __init__(self, r, x, y, mapa, bombero):
        self.rango = r
        self.pos_x = x
        self.pos_y = y
        self.tiempo = 3000
        self.bombero = bombero
        self.sectores = []
        self.obtener_rango(mapa)

    def actualizar(self, dt):

        self.tiempo = self.tiempo - dt

        if self.tiempo < 1000:
            self.fotograma = 2
        elif self.tiempo < 2000:
            self.fotograma = 1

    def obtener_rango(self, mapa):

        self.sectores.append([self.pos_x, self.pos_y])

        for x in range(1, self.rango):
            if mapa[self.pos_x + x][self.pos_y] == 1:
                break
            elif mapa[self.pos_x + x][self.pos_y] == 0 or mapa[self.pos_x - x][self.pos_y] == 3:
                self.sectores.append([self.pos_x + x, self.pos_y])
            elif mapa[self.pos_x + x][self.pos_y] == 2:
                self.sectores.append([self.pos_x + x, self.pos_y])
                break
        for x in range(1, self.rango):
            if mapa[self.pos_x - x][self.pos_y] == 1:
                break
            elif mapa[self.pos_x - x][self.pos_y] == 0 or mapa[self.pos_x - x][self.pos_y] == 3:
                self.sectores.append([self.pos_x - x, self.pos_y])
            elif mapa[self.pos_x - x][self.pos_y] == 2:
                self.sectores.append([self.pos_x - x, self.pos_y])
                break
        for x in range(1, self.rango):
            if mapa[self.pos_x][self.pos_y + x] == 1:
                break
            elif mapa[self.pos_x][self.pos_y + x] == 0 or mapa[self.pos_x][self.pos_y + x] == 3:
                self.sectores.append([self.pos_x, self.pos_y + x])
            elif mapa[self.pos_x][self.pos_y + x] == 2:
                self.sectores.append([self.pos_x, self.pos_y + x])
                break
        for x in range(1, self.rango):
            if mapa[self.pos_x][self.pos_y - x] == 1:
                break
            elif mapa[self.pos_x][self.pos_y - x] == 0 or mapa[self.pos_x][self.pos_y - x] == 3:
                self.sectores.append([self.pos_x, self.pos_y - x])
            elif mapa[self.pos_x][self.pos_y - x] == 2:
                self.sectores.append([self.pos_x, self.pos_y - x])
                break
