import pygame
import random
from bomba import Bomba
from nodo import Nodo
from enums.algoritmo import Algoritmo


class Enemigo:

    dire = [[1, 0, 1], [0, 1, 0], [-1, 0, 3], [0, -1, 2]]

    TAMAÑO_CASILLA = 4

    def __init__(self, x, y, alg):
        self.vida = True
        self.camino = []
        self.camino_movimiento = []
        self.pos_x = x * Enemigo.TAMAÑO_CASILLA
        self.pos_y = y * Enemigo.TAMAÑO_CASILLA
        self.direccion = 0
        self.fotograma = 0
        self.animacion = []
        self.rango = 3
        self.limite_bombas = 1
        self.plantar = False
        self.algoritmo = alg

    def mover(self, mapa, bombas, explosiones, enemigo):

        if self.direccion == 0:
            self.pos_y += 1
        elif self.direccion == 1:
            self.pos_x += 1
        elif self.direccion == 2:
            self.pos_y -= 1
        elif self.direccion == 3:
            self.pos_x -= 1

        if self.pos_x % Enemigo.TAMAÑO_CASILLA == 0 and self.pos_y % Enemigo.TAMAÑO_CASILLA == 0:
            self.camino_movimiento.pop(0)
            self.camino.pop(0)
            if len(self.camino) > 1:
                grid = self.crear_cuadricula(mapa, bombas, explosiones, enemigo)
                siguiente = self.camino[1]
                if grid[siguiente[0]][siguiente[1]] > 1:
                    self.camino_movimiento.clear()
                    self.camino.clear()

        if self.fotograma == 2:
            self.fotograma = 0
        else:
            self.fotograma += 1

    def hacer_movimiento(self, mapa, bombas, explosiones, enemigo):

        if not self.vida:
            return
        if len(self.camino_movimiento) == 0:
            if self.plantar:
                bombas.append(self.plantar_bomba(mapa))
                self.plantar = False
                mapa[int(self.pos_x / Enemigo.TAMAÑO_CASILLA)][int(self.pos_y / Enemigo.TAMAÑO_CASILLA)] = 3
            if self.algoritmo is Algoritmo.DFS:
                self.dfs(self.crear_cuadricula(mapa, bombas, explosiones, enemigo))
            else:
                self.dijkstra(self.crear_cuadricula_dijkstra(mapa, bombas, explosiones, enemigo))

        else:
            self.direccion = self.camino_movimiento[0]
            self.mover(mapa, bombas, explosiones, enemigo)

    def plantar_bomba(self, mapa):
        b = Bomba(self.rango, round(self.pos_x / Enemigo.TAMAÑO_CASILLA), round(self.pos_y / Enemigo.TAMAÑO_CASILLA), mapa, self)
        self.limite_bombas -= 1
        return b

    def comprobar_muerte(self, exp):

        for e in exp:
            for s in e.sectores:
                if int(self.pos_x / Enemigo.TAMAÑO_CASILLA) == s[0] and int(self.pos_y / Enemigo.TAMAÑO_CASILLA) == s[1]:
                    self.vida = False
                    return

    def dfs(self, cuadricula):

        nuevo_camino = [[int(self.pos_x / Enemigo.TAMAÑO_CASILLA), int(self.pos_y / Enemigo.TAMAÑO_CASILLA)]]
        profundidad = 0
        if self.limite_bombas == 0:
            self.dfs_rec(cuadricula, 0, nuevo_camino, profundidad)
        else:
            self.dfs_rec(cuadricula, 2, nuevo_camino, profundidad)

        self.camino = nuevo_camino

    def dfs_rec(self, cuadricula, fin, camino, profundidad):

        ultimo = camino[-1]
        if profundidad > 200:
            return
        if cuadricula[ultimo[0]][ultimo[1]] == 0 and fin == 0:
            return
        elif fin == 2:
            if cuadricula[ultimo[0] + 1][ultimo[1]] == fin or cuadricula[ultimo[0] - 1][ultimo[1]] == fin \
                    or cuadricula[ultimo[0]][ultimo[1] + 1] == fin \
                    or cuadricula[ultimo[0]][ultimo[1] - 1] == fin:
                if len(camino) == 1 and fin == 2:
                    self.plantar = True
                return

        cuadricula[ultimo[0]][ultimo[1]] = 9

        random.shuffle(self.dire)

        # seguro
        if cuadricula[ultimo[0] + self.dire[0][0]][ultimo[1] + self.dire[0][1]] == 0:
            camino.append([ultimo[0] + self.dire[0][0], ultimo[1] + self.dire[0][1]])
            self.camino_movimiento.append(self.dire[0][2])
        elif cuadricula[ultimo[0] + self.dire[1][0]][ultimo[1] + self.dire[1][1]] == 0:
            camino.append([ultimo[0] + self.dire[1][0], ultimo[1] + self.dire[1][1]])
            self.camino_movimiento.append(self.dire[1][2])
        elif cuadricula[ultimo[0] + self.dire[2][0]][ultimo[1] + self.dire[2][1]] == 0:
            camino.append([ultimo[0] + self.dire[2][0], ultimo[1] + self.dire[2][1]])
            self.camino_movimiento.append(self.dire[2][2])
        elif cuadricula[ultimo[0] + self.dire[3][0]][ultimo[1] + self.dire[3][1]] == 0:
            camino.append([ultimo[0] + self.dire[3][0], ultimo[1] + self.dire[3][1]])
            self.camino_movimiento.append(self.dire[3][2])

        # inseguro
        elif cuadricula[ultimo[0] + self.dire[0][0]][ultimo[1] + self.dire[0][1]] == 1:
            camino.append([ultimo[0] + self.dire[0][0], ultimo[1] + self.dire[0][1]])
            self.camino_movimiento.append(self.dire[0][2])
        elif cuadricula[ultimo[0] + self.dire[1][0]][ultimo[1] + self.dire[1][1]] == 1:
            camino.append([ultimo[0] + self.dire[1][0], ultimo[1] + self.dire[1][1]])
            self.camino_movimiento.append(self.dire[1][2])
        elif cuadricula[ultimo[0] + self.dire[2][0]][ultimo[1] + self.dire[2][1]] == 1:
            camino.append([ultimo[0] + self.dire[2][0], ultimo[1] + self.dire[2][1]])
            self.camino_movimiento.append(self.dire[2][2])
        elif cuadricula[ultimo[0] + self.dire[3][0]][ultimo[1] + self.dire[3][1]] == 1:
            camino.append([ultimo[0] + self.dire[3][0], ultimo[1] + self.dire[3][1]])
            self.camino_movimiento.append(self.dire[3][2])
        else:
            if len(self.camino_movimiento) > 0:
                camino.pop(0)
                self.camino_movimiento.pop(0)
        profundidad += 1
        self.dfs_rec(cuadricula, fin, camino, profundidad)

    def dijkstra(self, cuadricula):

        fin = 1
        if self.limite_bombas == 0:
            fin = 0

        visitado = []
        lista_abierta = []
        actual = cuadricula[int(self.pos_x / Enemigo.TAMAÑO_CASILLA)][int(self.pos_y / Enemigo.TAMAÑO_CASILLA)]
        actual.peso = actual.peso_base
        nuevo_camino = []
        while True:
            visitado.append(actual)
            random.shuffle(self.dire)
            if (actual.valor == fin and fin == 0) or\
                    (fin == 1 and (cuadricula[actual.x+1][actual.y].valor == 1 or cuadricula[actual.x-1][actual.y].valor == 1 or
                cuadricula[actual.x][actual.y+1].valor == 1 or cuadricula[actual.x][actual.y-1].valor == 1)):
                nuevo_camino.append([actual.x, actual.y])
                while True:
                    if actual.padre is None:
                        break
                    actual = actual.padre
                    nuevo_camino.append([actual.x, actual.y])
                nuevo_camino.reverse()
                for xd in range(len(nuevo_camino)):
                    if nuevo_camino[xd] is not nuevo_camino[-1]:
                        if nuevo_camino[xd][0] - nuevo_camino[xd+1][0] == -1:
                            self.camino_movimiento.append(1)
                        elif nuevo_camino[xd][0] - nuevo_camino[xd + 1][0] == 1:
                            self.camino_movimiento.append(3)
                        elif nuevo_camino[xd][1] - nuevo_camino[xd + 1][1] == -1:
                            self.camino_movimiento.append(0)
                        elif nuevo_camino[xd][1] - nuevo_camino[xd + 1][1] == 1:
                            self.camino_movimiento.append(2)
                if len(nuevo_camino) == 1 and fin == 1:
                    self.plantar = True
                self.camino = nuevo_camino
                return

            for i in range(len(self.dire)):
                if actual.x + self.dire[i][0] < len(cuadricula) and actual.y + self.dire[i][1] < len(cuadricula):
                    if cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].alcance \
                            and cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]] not in visitado:
                        if cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]] in lista_abierta:
                            if cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].peso >\
                                    cuadricula[actual.x][actual.y].peso \
                                    + cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].peso_base:
                                cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].padre = actual
                                cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].peso = actual.peso + cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].peso_base
                                cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].direccion = self.dire[i][2]

                        else:
                            cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].padre = actual
                            cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].peso =\
                                actual.peso + cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].peso_base
                            cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].direccion = self.dire[i][2]
                            lista_abierta.append(cuadricula[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]])

            if len(lista_abierta) == 0:
                self.camino = [[int(self.pos_x / Enemigo.TAMAÑO_CASILLA), int(self.pos_y / Enemigo.TAMAÑO_CASILLA)]]
                return

            siguiente_nodo = lista_abierta[0]
            for n in lista_abierta:
                if n.peso < siguiente_nodo.peso:
                    siguiente_nodo = n
            lista_abierta.remove(siguiente_nodo)
            actual = siguiente_nodo

    def crear_cuadricula(self, mapa, bombas, explosiones, enemigos):
        cuadricula = [[0] * len(mapa) for r in range(len(mapa))]

        # 0 - seguro
        # 1 - inseguro
        # 2 - destruible
        # 3 - inalcanzable

        for b in bombas:
            b.obtener_rango(mapa)
            for x in b.sectores:
                cuadricula[x[0]][x[1]] = 1
            cuadricula[b.pos_x][b.pos_y] = 3

        for e in explosiones:
            for s in e.sectores:
                cuadricula[s[0]][s[1]] = 3

        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                if mapa[i][j] == 1:
                    cuadricula[i][j] = 3
                elif mapa[i][j] == 2:
                    cuadricula[i][j] = 2

        for x in enemigos:
            if x == self:
                continue
            elif not x.vida:
                continue
            else:
                cuadricula[int(x.pos_x / Enemigo.TAMAÑO_CASILLA)][int(x.pos_y / Enemigo.TAMAÑO_CASILLA)] = 2

        return cuadricula

    def crear_cuadricula_dijkstra(self, mapa, bombas, explosiones, enemigos):
        cuadricula = [[None] * len(mapa) for r in range(len(mapa))]

        # 0 - seguro
        # 1 - destruible
        # 2 - inalcanzable
        # 3 - inseguro
        for i in range(len(mapa)):
            for j in range(len(mapa)):
                if mapa[i][j] == 0:
                    cuadricula[i][j] = Nodo(i, j, True, 1, 0)
                elif mapa[i][j] == 2:
                    cuadricula[i][j] = Nodo(i, j, False, 999, 1)
                elif mapa[i][j] == 1:
                    cuadricula[i][j] = Nodo(i, j, False, 999, 2)
                elif mapa[i][j] == 3:
                    cuadricula[i][j] = Nodo(i, j, False, 999, 2)

        for b in bombas:
            b.obtener_rango(mapa)
            for x in b.sectores:
                cuadricula[x[0]][x[1]].peso = 5
                cuadricula[x[0]][x[1]].valor = 3
            cuadricula[b.pos_x][b.pos_y].alcanzable = False

        for e in explosiones:
            for s in e.sectores:
                cuadricula[s[0]][s[1]].alcanzable = False

        for x in enemigos:
            if x == self:
                continue
            elif not x.vida:
                continue
            else:
                cuadricula[int(x.pos_x / Enemigo.TAMAÑO_CASILLA)][int(x.pos_y / Enemigo.TAMAÑO_CASILLA)].alcanzable = False
                cuadricula[int(x.pos_x / Enemigo.TAMAÑO_CASILLA)][int(x.pos_y / Enemigo.TAMAÑO_CASILLA)].valor = 1
        return cuadricula

    def cargar_animaciones(self, en, escala):
        frente = []
        atras = []
        izquierda = []
        derecha = []
        resize_ancho = escala
        resize_alto = escala

        ruta_imagen = 'images/enemigo/e'
        if en == '':
            ruta_imagen = 'images/heroe/p'

        f1 = pygame.image.load(ruta_imagen + en + 'f0.png')
        f2 = pygame.image.load(ruta_imagen + en + 'f1.png')
        f3 = pygame.image.load(ruta_imagen + en + 'f2.png')

        f1 = pygame.transform.scale(f1, (resize_ancho, resize_alto))
        f2 = pygame.transform.scale(f2, (resize_ancho, resize_alto))
        f3 = pygame.transform.scale(f3, (resize_ancho, resize_alto))

        frente.append(f1)
        frente.append(f2)
        frente.append(f3)

        r1 = pygame.image.load(ruta_imagen + en + 'r0.png')
        r2 = pygame.image.load(ruta_imagen + en + 'r1.png')
        r3 = pygame.image.load(ruta_imagen + en + 'r2.png')

        r1 = pygame.transform.scale(r1, (resize_ancho, resize_alto))
        r2 = pygame.transform.scale(r2, (resize_ancho, resize_alto))
        r3 = pygame.transform.scale(r3, (resize_ancho, resize_alto))

        derecha.append(r1)
        derecha.append(r2)
        derecha.append(r3)

        b1 = pygame.image.load(ruta_imagen + en + 'b0.png')
        b2 = pygame.image.load(ruta_imagen + en + 'b1.png')
        b3 = pygame.image.load(ruta_imagen + en + 'b2.png')

        b1 = pygame.transform.scale(b1, (resize_ancho, resize_alto))
        b2 = pygame.transform.scale(b2, (resize_ancho, resize_alto))
        b3 = pygame.transform.scale(b3, (resize_ancho, resize_alto))

        atras.append(b1)
        atras.append(b2)
        atras.append(b3)

        l1 = pygame.image.load(ruta_imagen + en + 'l0.png')
        l2 = pygame.image.load(ruta_imagen + en + 'l1.png')
        l3 = pygame.image.load(ruta_imagen + en + 'l2.png')

        l1 = pygame.transform.scale(l1, (resize_ancho, resize_alto))
        l2 = pygame.transform.scale(l2, (resize_ancho, resize_alto))
        l3 = pygame.transform.scale(l3, (resize_ancho, resize_alto))

        izquierda.append(l1)
        izquierda.append(l2)
        izquierda.append(l3)

        self.animacion.append(frente)
        self.animacion.append(derecha)
        self.animacion.append(atras)
        self.animacion.append(izquierda)
