import pygame
import pygame_menu
import juego
from enums.algoritmo import Algoritmo

COLOR_FONDO = (153, 153, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_BLANCO = (255, 255, 255)
FPS = 60.0
COLOR_FONDO_MENU = (102, 102, 153)
COLOR_TITULO_MENU = (51, 51, 255)
ESCALA_VENTANA = 0.75

pygame.display.init()
INFO = pygame.display.Info()
TAMANO_CASILLA = int(INFO.current_h * 0.07)
TAMANO_VENTANA = (13 * TAMANO_CASILLA, 13 * TAMANO_CASILLA)

reloj = None
algoritmo_jugador = Algoritmo.JUGADOR
algoritmo_en1 = Algoritmo.DIJKSTRA
algoritmo_en2 = Algoritmo.DFS
algoritmo_en3 = Algoritmo.DIJKSTRA
mostrar_camino = False
superficie = pygame.display.set_mode(TAMANO_VENTANA)


def cambiar_camino(valor, c):
    global mostrar_camino
    mostrar_camino = c


def cambiar_jugador(valor, c):
    global algoritmo_jugador
    algoritmo_jugador = c


def cambiar_enemigo1(valor, c):
    global algoritmo_en1
    algoritmo_en1 = c


def cambiar_enemigo2(valor, c):
    global algoritmo_en2
    algoritmo_en2 = c


def cambiar_enemigo3(valor, c):
    global algoritmo_en3
    algoritmo_en3 = c


def ejecutar_juego():
    juego.iniciar_juego(superficie, mostrar_camino, algoritmo_jugador, algoritmo_en1, algoritmo_en2, algoritmo_en3, TAMANO_CASILLA)


def fondo_principal():
    global superficie
    superficie.fill(COLOR_FONDO) 


def bucle_menu():
    pygame.init()

    pygame.display.set_caption('Among Us 2 - Bomberman')
    reloj = pygame.time.Clock()

    tema_menu = pygame_menu.Theme(
        selection_color = COLOR_BLANCO,
        widget_font = pygame_menu.font.FONT_BEBAS,
        title_font_size = TAMANO_CASILLA,
        title_font_color = COLOR_NEGRO,
        title_font = pygame_menu.font.FONT_BEBAS,
        widget_font_color = COLOR_NEGRO,
        widget_font_size = int(TAMANO_CASILLA*0.7),
        background_color = COLOR_FONDO_MENU,
        title_background_color = COLOR_TITULO_MENU,

    )

    menu_jugar = pygame_menu.Menu(
        theme = tema_menu,
        height = int(TAMANO_VENTANA[1] * ESCALA_VENTANA),
        width = int(TAMANO_VENTANA[0] * ESCALA_VENTANA),
        title = 'Menu de Juego'
    )

    opciones_juego = pygame_menu.Menu(
        theme=tema_menu,
        height=int(TAMANO_VENTANA[1] * ESCALA_VENTANA),
        width=int(TAMANO_VENTANA[0] * ESCALA_VENTANA),
        title='Opciones'
    )
    opciones_juego.add.selector("Personaje 1", [("Jugador", Algoritmo.JUGADOR)], onchange=cambiar_jugador)
    
    opciones_juego.add.selector("Personaje 2", [("DIJKSTRA", Algoritmo.DIJKSTRA), ("DFS", Algoritmo.DFS),
                                                ("Ninguno", Algoritmo.NINGUNO)], onchange=cambiar_enemigo1,  default=0)
    
    opciones_juego.add.selector("Personaje 3", [("DIJKSTRA", Algoritmo.DIJKSTRA), ("DFS", Algoritmo.DFS),
                                                ("Ninguno", Algoritmo.NINGUNO)], onchange=cambiar_enemigo2,  default=0)
    
    opciones_juego.add.selector("Personaje 4", [("DIJKSTRA", Algoritmo.DIJKSTRA), ("DFS", Algoritmo.DFS),
                                                ("Ninguno", Algoritmo.NINGUNO)], onchange=cambiar_enemigo3,  default=0)
    
    opciones_juego.add.selector("Mostrar camino", [("Si", True), ("No", False)], onchange=cambiar_camino)

    opciones_juego.add.button('Atras', pygame_menu.events.BACK)
    
    menu_jugar.add.button('Comenzar', ejecutar_juego)

    menu_jugar.add.button('Opciones', opciones_juego)
    menu_jugar.add.button('Volver al menu principal', pygame_menu.events.BACK)

    tema_controles = pygame_menu.themes.Theme(
        selection_color = COLOR_BLANCO,
        widget_font = pygame_menu.font.FONT_BEBAS,
        title_font_size = TAMANO_CASILLA,
        title_font_color = COLOR_NEGRO,
        title_font = pygame_menu.font.FONT_BEBAS,
        widget_font_color = COLOR_NEGRO,
        widget_font_size = int(TAMANO_CASILLA*0.5),
        background_color = COLOR_FONDO_MENU,
        title_background_color = COLOR_TITULO_MENU
    )

    menu_controles = pygame_menu.Menu(
        theme=tema_controles,
        height = int(TAMANO_VENTANA[1] * ESCALA_VENTANA),
        width = int(TAMANO_VENTANA[0] * ESCALA_VENTANA),
        overflow = False,
        title = 'Controles'
    )
    menu_controles.add.label("Controles del jugador: ")
    menu_controles.add.label("Movimiento: Flechas")
    menu_controles.add.label("Plantar bomba: Espacio")
    menu_controles.add.button('Volver al menu principal', pygame_menu.events.BACK)

    menu_principal = pygame_menu.Menu(
        theme=tema_menu,
        height=int(TAMANO_VENTANA[1] * ESCALA_VENTANA),
        width=int(TAMANO_VENTANA[0] * ESCALA_VENTANA),
        onclose=pygame_menu.events.EXIT,
        title='Menu principal'
    )

    menu_principal.add.button('Jugar', menu_jugar)
    menu_principal.add.button('Controles', menu_controles)
    menu_principal.add.button('Salir', pygame_menu.events.EXIT)

    ejecutando = True
    while ejecutando:

        reloj.tick(FPS)

        fondo_principal()

        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                ejecutando = False

        if menu_principal.is_enabled():
            menu_principal.mainloop(superficie, fondo_principal)

        pygame.display.flip()

    exit()


if __name__ == "__main__":
    bucle_menu()
