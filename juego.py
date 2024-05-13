from time import sleep
import pygame
import sys
import random

from enums.power_up_type import TipoPowerUp
from jugador import Jugador
from explosion import Explosion
from enemigo import Enemigo
from enums.algoritmo import Algoritmo
from power_up import Potenciador

COLOR_FONDO = (107, 142, 35)

fuente = None

jugador = None
lista_enemigos = []
bloques_enemigos = []
bombas = []
explosiones = []
power_ups = []


BASE_GRID = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


def iniciar_juego(surface, path, algoritmo_jugador, algoritmo_en1, algoritmo_en2, algoritmo_en3, escala):

    global fuente
    fuente = pygame.font.SysFont('Bebas', escala)

    global lista_enemigos
    global bloques_enemigos
    global jugador

    lista_enemigos = []
    bloques_enemigos = []
    global explosiones
    global bombas
    global power_ups
    bombas.clear()
    explosiones.clear()
    power_ups.clear()

    jugador = Jugador()

    if algoritmo_en1 is not Algoritmo.NINGUNO:
        en1 = Enemigo(11, 11, algoritmo_en1)
        en1.cargar_animaciones('1', escala)
        lista_enemigos.append(en1)
        bloques_enemigos.append(en1)

    if algoritmo_en2 is not Algoritmo.NINGUNO:
        en2 = Enemigo(1, 11, algoritmo_en2)
        en2.cargar_animaciones('2', escala)
        lista_enemigos.append(en2)
        bloques_enemigos.append(en2)

    if algoritmo_en3 is not Algoritmo.NINGUNO:
        en3 = Enemigo(11, 1, algoritmo_en3)
        en3.cargar_animaciones('3', escala)
        lista_enemigos.append(en3)
        bloques_enemigos.append(en3)

    if algoritmo_jugador is Algoritmo.JUGADOR:
        jugador.cargar_animaciones(escala)
        bloques_enemigos.append(jugador)
    elif algoritmo_jugador is not Algoritmo.NINGUNO:
        en0 = Enemigo(1, 1, algoritmo_jugador)
        en0.cargar_animaciones('', escala)
        lista_enemigos.append(en0)
        bloques_enemigos.append(en0)
        jugador.vida = False
    else:
        jugador.vida = False

    imagen_pasto = pygame.image.load('images/terreno/grass.png')
    imagen_pasto = pygame.transform.scale(imagen_pasto, (escala, escala))

    imagen_bloque = pygame.image.load('images/terreno/block.png')
    imagen_bloque = pygame.transform.scale(imagen_bloque, (escala, escala))

    imagen_caja = pygame.image.load('images/terreno/box.png')
    imagen_caja = pygame.transform.scale(imagen_caja, (escala, escala))

    imagen_bomba1 = pygame.image.load('images/bomba/1.png')
    imagen_bomba1 = pygame.transform.scale(imagen_bomba1, (escala, escala))

    imagen_bomba2 = pygame.image.load('images/bomba/2.png')
    imagen_bomba2 = pygame.transform.scale(imagen_bomba2, (escala, escala))

    imagen_bomba3 = pygame.image.load('images/bomba/3.png')
    imagen_bomba3 = pygame.transform.scale(imagen_bomba3, (escala, escala))

    imagen_explosion1 = pygame.image.load('images/explosion/1.png')
    imagen_explosion1 = pygame.transform.scale(imagen_explosion1, (escala, escala))

    imagen_explosion2 = pygame.image.load('images/explosion/2.png')
    imagen_explosion2 = pygame.transform.scale(imagen_explosion2, (escala, escala))

    imagen_explosion3 = pygame.image.load('images/explosion/3.png')
    imagen_explosion3 = pygame.transform.scale(imagen_explosion3, (escala, escala))

    imagenes_terreno = [imagen_pasto, imagen_bloque, imagen_caja, imagen_pasto]
    imagenes_bomba = [imagen_bomba1, imagen_bomba2, imagen_bomba3]
    imagenes_explosion = [imagen_explosion1, imagen_explosion2, imagen_explosion3]

    imagen_power_up_bomba = pygame.image.load('images/power_up/bomb.png')
    imagen_power_up_bomba = pygame.transform.scale(imagen_power_up_bomba, (escala, escala))

    imagen_power_up_fuego = pygame.image.load('images/power_up/fire.png')
    imagen_power_up_fuego = pygame.transform.scale(imagen_power_up_fuego, (escala, escala))

    imagenes_power_ups = [imagen_power_up_bomba, imagen_power_up_fuego]

    principal(surface, escala, path, imagenes_terreno, imagenes_bomba, imagenes_explosion, imagenes_power_ups)


def dibujar(s, grid, tamano_casilla, mostrar_camino, juego_terminado, imagenes_terreno, imagenes_bomba, imagenes_explosion, imagenes_power_ups):
    s.fill(COLOR_FONDO)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            s.blit(imagenes_terreno[grid[i][j]], (i * tamano_casilla, j * tamano_casilla, tamano_casilla, tamano_casilla))

    for pu in power_ups:
        s.blit(imagenes_power_ups[pu.tipo.value], (pu.pos_x * tamano_casilla, pu.pos_y * tamano_casilla, tamano_casilla, tamano_casilla))

    for x in bombas:
        s.blit(imagenes_bomba[x.fotograma], (x.pos_x * tamano_casilla, x.pos_y * tamano_casilla, tamano_casilla, tamano_casilla))

    for y in explosiones:
        for x in y.sectores:
            s.blit(imagenes_explosion[y.fotograma], (x[0] * tamano_casilla, x[1] * tamano_casilla, tamano_casilla, tamano_casilla))
    if jugador.vida:
        s.blit(jugador.animacion[jugador.direccion][jugador.fotograma],
               (jugador.pos_x * (tamano_casilla / 4), jugador.pos_y * (tamano_casilla / 4), tamano_casilla, tamano_casilla))
    for en in lista_enemigos:
        if en.vida:
            s.blit(en.animacion[en.direccion][en.fotograma],
                   (en.pos_x * (tamano_casilla / 4), en.pos_y * (tamano_casilla / 4), tamano_casilla, tamano_casilla))
            if mostrar_camino:
                if en.algoritmo == Algoritmo.DFS:
                    for sek in en.camino:
                        pygame.draw.rect(s, (255, 0, 0, 240),
                                         [sek[0] * tamano_casilla, sek[1] * tamano_casilla, tamano_casilla, tamano_casilla], 1)
                else:
                    for sek in en.camino:
                        pygame.draw.rect(s, (255, 0, 255, 240),
                                         [sek[0] * tamano_casilla, sek[1] * tamano_casilla, tamano_casilla, tamano_casilla], 1)

    if juego_terminado:
        tf = fuente.render("Presiona ESC para volver al menú", False, (153, 153, 255))
        s.blit(tf, (10, 10))

    pygame.display.update()


def generar_mapa(grid):
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            if grid[i][j] != 0:
                continue
            elif (i < 3 or i > len(grid) - 4) and (j < 3 or j > len(grid[i]) - 4):
                continue
            if random.randint(0, 9) < 7:
                grid[i][j] = 2

    return


def principal(s, tamano_casilla, mostrar_camino, imagenes_terreno, imagenes_bomba, imagenes_explosion, imagenes_power_ups):
    pasos = pygame.mixer.Sound(r"sonidos\pasos.mp3")
    fondo = pygame.mixer.Sound(r"sonidos\fondo.mp3")
    grid = [fila[:] for fila in BASE_GRID]
    generar_mapa(grid)
    # power_ups.append(PowerUp(1, 2, TipoPowerUp.BOMBA))
    # power_ups.append(PowerUp(2, 1, TipoPowerUp.FUEGO))
    reloj = pygame.time.Clock()
    
    fondo.play()

    ejecutando = True
    juego_terminado = False
    while ejecutando:
        dt = reloj.tick(15)
        for en in lista_enemigos:
            en.hacer_movimiento(grid, bombas, explosiones, bloques_enemigos)

        if jugador.vida:
            teclas = pygame.key.get_pressed()
            temp = jugador.direccion
            movimiento = False
            if teclas[pygame.K_DOWN]:
                temp = 0
                jugador.mover(0, 1, grid, bloques_enemigos, power_ups)
                movimiento = True
            elif teclas[pygame.K_RIGHT]:
                temp = 1
                jugador.mover(1, 0, grid, bloques_enemigos, power_ups)
                movimiento = True
            elif teclas[pygame.K_UP]:
                temp = 2
                jugador.mover(0, -1, grid, bloques_enemigos, power_ups)
                movimiento = True
            elif teclas[pygame.K_LEFT]:
                temp = 3
                jugador.mover(-1, 0, grid, bloques_enemigos, power_ups)
                movimiento = True
            if temp != jugador.direccion:
                jugador.fotograma = 0
                jugador.direccion = temp
            if movimiento:
                if jugador.fotograma == 2:
                    jugador.fotograma = 0
                else:
                    jugador.fotograma += 1
                    pasos.play()
                

        dibujar(s, grid, tamano_casilla, mostrar_camino, juego_terminado, imagenes_terreno, imagenes_bomba, imagenes_explosion, imagenes_power_ups)

        if not juego_terminado:
            juego_terminado = comprobar_fin_juego()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if jugador.limite_bombas == 0 or not jugador.vida:
                        continue
                    temp_bomba = jugador.plantar_bomba(grid)
                    bombas.append(temp_bomba)
                    grid[temp_bomba.pos_x][temp_bomba.pos_y] = 3
                    jugador.limite_bombas -= 1
                elif e.key == pygame.K_ESCAPE:
                    ejecutando = False

        actualizar_bombas(grid, dt)

    explosiones.clear()
    lista_enemigos.clear()
    bloques_enemigos.clear()
    power_ups.clear()
    fondo.stop()


def actualizar_bombas(grid, dt):
    for b in bombas:
        b.actualizar(dt)
        if b.tiempo < 1:
            b.bombero.limite_bombas += 1
            grid[b.pos_x][b.pos_y] = 0
            exp_temp = Explosion(b.pos_x, b.pos_y, b.rango)
            exp_temp.explotar(grid, bombas, b, power_ups)
            exp_temp.limpiar_sectores(grid, random, power_ups)
            explosiones.append(exp_temp)
    if jugador not in lista_enemigos:
        jugador.comprobar_muerte(explosiones)
    for en in lista_enemigos:
        en.comprobar_muerte(explosiones)
    for e in explosiones:
        e.actualizar(dt)
        if e.tiempo < 1:
            explosiones.remove(e)


def comprobar_fin_juego():
    if not jugador.vida:
        return True

    for en in lista_enemigos:
        if en.vida:
            return False

    return True
