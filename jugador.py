import pygame
import math

from bomba import Bomba
from enums.power_up_type import TipoPowerUp


class Jugador:
    pos_x = 4
    pos_y = 4
    direccion = 0
    fotograma = 0
    animacion = []
    alcance = 3
    limite_bombas = 1

    TAMANIO_CASILLA = 4

    def __init__(self):
        self.vida = True

    def mover(self, dx, dy, cuadricula, enemigos, potenciadores):
        tempx = int(self.pos_x / Jugador.TAMANIO_CASILLA)
        tempy = int(self.pos_y / Jugador.TAMANIO_CASILLA)

        mapa = []

        for i in range(len(cuadricula)):
            mapa.append([])
            for j in range(len(cuadricula[i])):
                mapa[i].append(cuadricula[i][j])

        for x in enemigos:
            if x == self:
                continue
            elif not x.vida:
                continue
            else:
                mapa[int(x.pos_x / Jugador.TAMANIO_CASILLA)][int(x.pos_y / Jugador.TAMANIO_CASILLA)] = 2

        if self.pos_x % Jugador.TAMANIO_CASILLA != 0 and dx == 0:
            if self.pos_x % Jugador.TAMANIO_CASILLA == 1:
                self.pos_x -= 1
            elif self.pos_x % Jugador.TAMANIO_CASILLA == 3:
                self.pos_x += 1
            return
        if self.pos_y % Jugador.TAMANIO_CASILLA != 0 and dy == 0:
            if self.pos_y % Jugador.TAMANIO_CASILLA == 1:
                self.pos_y -= 1
            elif self.pos_y % Jugador.TAMANIO_CASILLA == 3:
                self.pos_y += 1
            return

        # derecha
        if dx == 1:
            if mapa[tempx+1][tempy] == 0:
                self.pos_x += 1
        # izquierda
        elif dx == -1:
            tempx = math.ceil(self.pos_x / Jugador.TAMANIO_CASILLA)
            if mapa[tempx-1][tempy] == 0:
                self.pos_x -= 1

        # abajo
        if dy == 1:
            if mapa[tempx][tempy+1] == 0:
                self.pos_y += 1
        # arriba
        elif dy == -1:
            tempy = math.ceil(self.pos_y / Jugador.TAMANIO_CASILLA)
            if mapa[tempx][tempy-1] == 0:
                self.pos_y -= 1

        for pu in potenciadores:
            if pu.pos_x == math.ceil(self.pos_x / Jugador.TAMANIO_CASILLA) \
                    and pu.pos_y == math.ceil(self.pos_y / Jugador.TAMANIO_CASILLA):
                self.consumir_potenciador(pu, potenciadores)

    def plantar_bomba(self, mapa):
        b = Bomba(self.alcance, round(self.pos_x / Jugador.TAMANIO_CASILLA), round(self.pos_y / Jugador.TAMANIO_CASILLA), mapa, self)
        return b

    def comprobar_muerte(self, exp):
        for e in exp:
            for s in e.sectores:
                if int(self.pos_x / Jugador.TAMANIO_CASILLA) == s[0] and int(self.pos_y / Jugador.TAMANIO_CASILLA) == s[1]:
                    self.vida = False

    def consumir_potenciador(self, potenciador, potenciadores):
        if potenciador.tipo == TipoPowerUp.BOMBA:
            self.limite_bombas += 1
        elif potenciador.tipo == TipoPowerUp.FUEGO:
            self.alcance += 1

        potenciadores.remove(potenciador)

    def cargar_animaciones(self, escala):
        frente = []
        derecha = []
        atras = []
        izquierda = []
        ancho_redimensionado = escala
        alto_redimensionado = escala

        f1 = pygame.image.load('images/heroe/pf0.png')
        f2 = pygame.image.load('images/heroe/pf1.png')
        f3 = pygame.image.load('images/heroe/pf2.png')

        f1 = pygame.transform.scale(f1, (ancho_redimensionado, alto_redimensionado))
        f2 = pygame.transform.scale(f2, (ancho_redimensionado, alto_redimensionado))
        f3 = pygame.transform.scale(f3, (ancho_redimensionado, alto_redimensionado))

        frente.append(f1)
        frente.append(f2)
        frente.append(f3)

        r1 = pygame.image.load('images/heroe/pr0.png')
        r2 = pygame.image.load('images/heroe/pr1.png')
        r3 = pygame.image.load('images/heroe/pr2.png')

        r1 = pygame.transform.scale(r1, (ancho_redimensionado, alto_redimensionado))
        r2 = pygame.transform.scale(r2, (ancho_redimensionado, alto_redimensionado))
        r3 = pygame.transform.scale(r3, (ancho_redimensionado, alto_redimensionado))

        derecha.append(r1)
        derecha.append(r2)
        derecha.append(r3)

        b1 = pygame.image.load('images/heroe/pb0.png')
        b2 = pygame.image.load('images/heroe/pb1.png')
        b3 = pygame.image.load('images/heroe/pb2.png')

        b1 = pygame.transform.scale(b1, (ancho_redimensionado, alto_redimensionado))
        b2 = pygame.transform.scale(b2, (ancho_redimensionado, alto_redimensionado))
        b3 = pygame.transform.scale(b3, (ancho_redimensionado, alto_redimensionado))

        atras.append(b1)
        atras.append(b2)
        atras.append(b3)

        l1 = pygame.image.load('images/heroe/pl0.png')
        l2 = pygame.image.load('images/heroe/pl1.png')
        l3 = pygame.image.load('images/heroe/pl2.png')

        l1 = pygame.transform.scale(l1, (ancho_redimensionado, alto_redimensionado))
        l2 = pygame.transform.scale(l2, (ancho_redimensionado, alto_redimensionado))
        l3 = pygame.transform.scale(l3, (ancho_redimensionado, alto_redimensionado))

        izquierda.append(l1)
        izquierda.append(l2)
        izquierda.append(l3)

        self.animacion.append(frente)
        self.animacion.append(derecha)
        self.animacion.append(atras)
        self.animacion.append(izquierda)
