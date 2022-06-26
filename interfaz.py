import curses 
from curses import wrapper
from curses.textpad import rectangle
import time
from ia import *

def main(stdscr):#función principal

    def print_circle(x,y,color):
        tablero.addstr(y*4+1,x*9+2,"  ▄▄  ",color)
        tablero.addstr(y*4+2,x*9+2," █  █ ",color)
        tablero.addstr(y*4+3,x*9+2,"  ▀▀  ",color)

    def print_cross(x,y,color):
        tablero.addstr(y*4+1,x*9+2," ▄  ▄ ",color)
        tablero.addstr(y*4+2,x*9+2,"  ██  ",color)
        tablero.addstr(y*4+3,x*9+2," ▀  ▀ ",color)

    def print_score(puntos_jug,puntos_maq):
        puntuaciones.addstr(0,2,"PUNTUACIONES", VERDE_FONDO_NEGRO)
        puntuaciones.addstr(2,0,f"Jugador: {puntos_jug}", VERDE_FONDO_NEGRO)
        puntuaciones.addstr(4,0,f"Máquina: {puntos_maq}", VERDE_FONDO_NEGRO)
        puntuaciones.refresh()

    def print_board(array):
        tablero.addstr( 0,0,"╔════════╦════════╦════════╗")
        tablero.addstr( 1,0,"║        ║        ║        ║")
        tablero.addstr( 2,0,"║        ║        ║        ║")
        tablero.addstr( 3,0,"║        ║        ║        ║")
        tablero.addstr( 4,0,"╠════════╬════════╬════════╣")
        tablero.addstr( 5,0,"║        ║        ║        ║")
        tablero.addstr( 6,0,"║        ║        ║        ║")
        tablero.addstr( 7,0,"║        ║        ║        ║")
        tablero.addstr( 8,0,"╠════════╬════════╬════════╣")
        tablero.addstr( 9,0,"║        ║        ║        ║")
        tablero.addstr(10,0,"║        ║        ║        ║")
        tablero.addstr(11,0,"║        ║        ║        ║")
        tablero.addstr(12,0,"╚════════╩════════╩════════╝")

        filas, columnas = array.shape
        for x in range(filas):
            for y in range(columnas):
                color = BLANCO_FONDO_NEGRO
                if determinar_color(array,x,y) == 2: color = VERDE_FONDO_NEGRO
                if determinar_color(array,x,y) == 1: color = ROJO_FONDO_NEGRO
                if array[x,y] == -1: print_circle(x,y,color)
                if array[x,y] == 1: print_cross(x,y,color)
        tablero.refresh()

    def print_dialog(mensaje:str,color):
        cuadro_dialogo.addstr(0,0,mensaje,color)
        cuadro_dialogo.refresh()

    def asignar_valor_casilla(jugador,array,x,y):
        if array[x,y] == 0:
                if jugador == "jugador":
                    array[x,y] = -1
                if jugador == "maquina":
                    array[x,y] = 1
        else: 
            print_dialog("     Esa casilla ya está ocupada.", ROJO_FONDO_NEGRO)
            jugada_usuario(array)
            
    def jugada_usuario(array):
        jugada = stdscr.getkey()
        cuadro_dialogo.clear()
        cuadro_dialogo.refresh()
        casillas = {
            (0,0) : ["KEY_A1","7"],
            (1,0) : ["KEY_A2","8"],
            (2,0) : ["KEY_A3","9"],
            (0,1) : ["KEY_B1","4"],
            (1,1) : ["KEY_B2","5"],
            (2,1) : ["KEY_B3","6"],
            (0,2) : ["KEY_C1","1"],
            (1,2) : ["KEY_C2","2"],
            (2,2) : ["KEY_C3","3"],
        }
        if jugada == "x": quit()
        for key,value in casillas.items():
            if jugada in value:
                asignar_valor_casilla("jugador",array,key[0],key[1])
        if any(jugada in value for value in casillas.values()) == False: 
            print_dialog("     Eso no es una casilla.", ROJO_FONDO_NEGRO)
            jugada_usuario(array)
        
    def jugada_maquina(array):
        if primeraJugadaMq(array) == False:
            jugada = eleccionJugada(posiblesJugadas(array))
        else: 
            jugada = eleccion1JugadaMq()
        asignar_valor_casilla("maquina",array,jugada[0],jugada[1])

    ###FONDO
    rectangle(stdscr, 0, 0, 25, 78)
    #COLORES
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    VERDE_FONDO_NEGRO = curses.color_pair(1)
    NEGRO_FONDO_VERDE = curses.color_pair(2)
    BLANCO_FONDO_NEGRO = curses.color_pair(3)
    ROJO_FONDO_NEGRO = curses.color_pair(4)
    #TITULO
    stdscr.addstr(2,23,"                                ", curses.A_STANDOUT| VERDE_FONDO_NEGRO)
    stdscr.addstr(3,23,"          TRES EN RAYA          ", curses.A_STANDOUT| VERDE_FONDO_NEGRO | curses.A_BOLD)
    stdscr.addstr(4,23,"                                ", curses.A_STANDOUT| VERDE_FONDO_NEGRO)
    #CREDITOS
    stdscr.addstr(24,1," "*78,NEGRO_FONDO_VERDE)
    stdscr.addstr(24,1,"Creado por: Laura y Carla",NEGRO_FONDO_VERDE)
    #INSTRUCCIONES
    stdscr.addstr(10,59,"╔═══╦═══╦═══╗", VERDE_FONDO_NEGRO)
    stdscr.addstr(11,59,"║ 7 ║ 8 ║ 9 ║", VERDE_FONDO_NEGRO)
    stdscr.addstr(12,59,"╠═══╬═══╬═══╣", VERDE_FONDO_NEGRO)
    stdscr.addstr(13,59,"║ 4 ║ 5 ║ 6 ║", VERDE_FONDO_NEGRO)
    stdscr.addstr(14,59,"╠═══╬═══╬═══╣", VERDE_FONDO_NEGRO)
    stdscr.addstr(15,59,"║ 1 ║ 2 ║ 3 ║", VERDE_FONDO_NEGRO)
    stdscr.addstr(16,59,"╚═══╩═══╩═══╝", VERDE_FONDO_NEGRO)
    stdscr.addstr(17,59,"  NUMPAD     ", VERDE_FONDO_NEGRO)
    #SALIR
    stdscr.addstr(0,77," X ", curses.A_STANDOUT | ROJO_FONDO_NEGRO | curses.A_BOLD)
    ###PUNTUACIONES
    puntuaciones = curses.newwin(6,20,10,4)
    ###TABLERO
    tablero = curses.newwin(15,30,7,25)
    ###CUADRO DE DIÁLOGO 
    cuadro_dialogo=curses.newwin(1,40,22,20)

    stdscr.refresh()

    ###LOOP PRINCIPAL
    array = np.zeros((3,3))
    puntos_jug = 0
    puntos_maq = 0
    rondas = 0
    while True:
        maquina = False
        if rondas % 2 == 0: maquina = True
        print_score(puntos_jug,puntos_maq)
        while resultado(array) == 0:
            print_board(array)
            if maquina == True:
                time.sleep(0.5)
                jugada_maquina(array)
                maquina = False
            else:
                jugada_usuario(array)
                maquina = True
        print_board(array)
        if resultado(array) == 1: 
            puntos_jug += 1
            print_dialog("Gana el jugador.", VERDE_FONDO_NEGRO)
        if resultado(array) == 2:
            puntos_maq += 1
            print_dialog("Gana la máquina.", ROJO_FONDO_NEGRO)
        if resultado(array) == 3:
            print_dialog("Empate.", VERDE_FONDO_NEGRO)
        rondas += 1
        array = np.zeros((3,3))
        time.sleep(1.5)

wrapper(main)#función importada que llama a la función main
