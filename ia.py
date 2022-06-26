import numpy as np
import random

# jugada de la maquina
# 0. recorrer casillas
# 1. decidir si la casilla esta vacia
# 2. si esta vacia, calcular su valor horizontal, vertical y diagonal (de tener)
# 2.5 calcular su valor min y max en funcion a esos valores
# 3. sumar estos valores para tener el valor total de min y max para cada casilla
# 4. realiza su jugada en funcion al valor

m = np.zeros((3, 3))  # matriz basica de partida

# transformar lista en matriz de 3 x 3:
l = [0, 0, 1, -1, 0, 0, 1, 0, 0]
m1 = np.array(l).reshape(3, 3)



def valor_filas(matriz):
    valor_filas = np.apply_along_axis(sum, 1, matriz)
    return valor_filas.tolist()


def valor_columnas(matriz):
    valor_columnas = np.apply_along_axis(sum, 0, matriz)
    return valor_columnas.tolist()


def valor_diagonal(matriz):
    suma = sum(matriz.diagonal())
    return suma


def valor_diagonal_reversa(matriz):
    matriz_reversa = np.fliplr(matriz)
    suma = sum(matriz_reversa.diagonal())
    return suma



def seleccionarJugada(jugadas: dict, mejorjugada, evitarjugada, x, y):   
    if (mejorjugada == 2): # comprueba si hay una jugada ganadora y la almacena directamente en el diccionario de las jugadas posibles
        jugadas[(x, y)] = mejorjugada
    elif (evitarjugada == -2):# comprueba si hay una jugada a evitar
        jugadas[(x, y)] = evitarjugada      
    elif (mejorjugada > 0):
        jugadas[(x, y)] = mejorjugada  # prioriza las jugadas positivas no urgentes
    elif (evitarjugada < 0):
        jugadas[(x, y)] = evitarjugada  # jugadas a evitar no urgentes
    else:
        jugadas[(x, y)] = 0
    return jugadas


def posiblesJugadas(m):
    filas, columnas = m.shape
    jugadas = {}
    for x in range(0, filas):
        for y in range(0, columnas):
            if m[x, y] == 0:  # si está vacía                
                valores = [] #se almacenan los valores de la casilla por columna, filas y diagonales si estuviese en una  
                valores.append(valor_columnas(m)[y])
                valores.append(valor_filas(m)[x])
                if x == y:
                    valores.append(valor_diagonal(m))
                if ((x == 0 and y == 2) or (x == 1 and y == 1) or (x == 2 and y == 0)):
                    valores.append(valor_diagonal_reversa(m))
                mejorjugada = max(valores) 
                evitarjugada = min(valores)
                seleccionarJugada(jugadas, mejorjugada, evitarjugada, x, y)#aquí se elige la mejor jugada para esa casilla y se almacena en el diccionario jugadas
    return jugadas


def eleccionJugada(jugadas: dict):
    maxValue = max(jugadas.values())
    minValue = min(jugadas.values())
    jugadaElegida = None
    if abs(maxValue) >= abs(minValue):
        jugadaElegida = maxValue
    else:
        jugadaElegida = minValue
    for key in jugadas:
        if jugadas[key] == jugadaElegida:
            return key


def resultado(m):
    valores = [valor_filas(m),valor_columnas(m)] #lista de listas... poner mas bonito
    flat_list = []
    for sublist in valores:
        for item in sublist:
            flat_list.append(item)
    flat_list.append(valor_diagonal(m))
    flat_list.append(valor_diagonal_reversa(m))

    if 0 not in m: 
        return 3 #empate
    if 3 in flat_list:
        return 2 #gana maquina
    if -3 in flat_list:
        return 1 #gana jugador
    return 0 #partida sigue

def valor_casilla(array,x,y):
    valor_fila = valor_filas(array)[x]
    valor_columna = valor_columnas(array)[y]
    return valor_fila,valor_columna

def determinar_color(array,x,y):
        casilla = (y,x)
        diagonal = [(0,0),(1,1),(2,2)]
        diagonal_reversa = [(0,2),(1,1),(2,0)]
        if -3 in valor_casilla(array,x,y): return 2
        elif 3 in valor_casilla(array,x,y): return 1
        elif casilla in diagonal and valor_diagonal(array) == -3: return 2
        elif casilla in diagonal and valor_diagonal(array) == 3: return 1
        elif casilla in diagonal_reversa and valor_diagonal_reversa(array) == -3: return 2
        elif casilla in diagonal_reversa and valor_diagonal_reversa(array) == 3: return 1
        else: return 0
        
def primeraJugadaMq(matriz): #devuelve si es la primera jugada en el turno de la máquina
    primera=True
    for x in np.nditer(matriz):
        if x!=0:
            primera = False            
    return primera
    
def eleccion1JugadaMq():#devuelve una fila y columna aleatoria
        x = random.randint(0,2)
        y = random.randint(0,2)
        return (x, y)

