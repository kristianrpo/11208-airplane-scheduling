from collections import deque
## Función que evalúa si la posición a la cual se quiere acceder se encuentra dentro de la matriz
def casilla_es_valido(filas,columnas,nueva_x,nueva_y):
    return nueva_x>=0 and nueva_y>=0 and nueva_x<filas and nueva_y<columnas

## Función que evalúa si la posición a la que se quiere acceder es una casilla en negro (bloqueo)
def casilla_es_casilla_negra(matriz_simbolos,x,y):
    if matriz_simbolos[x][y] == '##':
        return True

## Función que evalúa si la posición a la que se quiere acceder es una casilla en blanco (pista)
def casilla_es_blanca(matriz_simbolos,x,y):
    if matriz_simbolos[x][y] == '..':
        return True
    
## Función que evalúa si la posición a la que se quiere acceder es un parqueadero
def casilla_es_parqueadero(matriz_simbolos,x,y):
    return matriz_simbolos[x][y].isdigit()

## Función que evalúa si la posición a la que se quiere acceder es una casilla gris (entrada-salida ó aeropuerto)
def casilla_es_aeropuerto(matriz_simbolos,x,y):
    if matriz_simbolos[x][y] == '==':
        return True
    
## Función en la que se asigna un peso a cada casilla desde su respectivo aeropuerto (entrada/salida). Primero, se guarda en el deque (pesos) las coordenadas de los puntos 
## entradas/salidas (antes de ingresar a la funcion), luego, si la posicion adyasente a mi actual es casilla en blanco, añado esta en el inicio del deque, y le asigno el mismo peso de mi actual,
## si es parqueadero, lo añado en el final de mi deque, y le asigno el peso de mi actual + 1, y si es bloqueo, no lo añado al deque y le asigno el valor de infinito (-11).
## Ademas, se guarda las coordenadas de cada uno de los parqueaderos.
def ponderar (matriz_simbolos,matriz_ponderar,pesos,movimientos,filas,columnas):
    visitados = set()
    parqueaderos = []
    while(len(pesos)>0):
        actual_coordenada = pesos.popleft()
        for i in range(len(movimientos)):
            nueva_x = actual_coordenada[0] + movimientos[i][0]
            nueva_y = actual_coordenada[1] + movimientos[i][1]
            if casilla_es_valido(filas,columnas,nueva_x,nueva_y) and (nueva_x,nueva_y) not in visitados:
                if casilla_es_casilla_negra(matriz_simbolos,nueva_x,nueva_y):
                    matriz_ponderar[nueva_x][nueva_y] = -11
                    visitados.add((nueva_x,nueva_y))
                if casilla_es_blanca(matriz_simbolos,nueva_x,nueva_y):
                    matriz_ponderar[nueva_x][nueva_y] = matriz_ponderar[actual_coordenada[0]][actual_coordenada[1]]
                    pesos.appendleft((nueva_x,nueva_y))
                    visitados.add((nueva_x,nueva_y))
                if casilla_es_parqueadero(matriz_simbolos, nueva_x,nueva_y):
                    matriz_ponderar[nueva_x][nueva_y] = matriz_ponderar[actual_coordenada[0]][actual_coordenada[1]] + 1
                    pesos.append((nueva_x,nueva_y))
                    visitados.add((nueva_x,nueva_y))
                    parqueaderos.append(((nueva_x,nueva_y),matriz_ponderar[nueva_x][nueva_y]))
    parqueaderos_ordenados = sorted(parqueaderos,key = lambda x: x[1])
    return matriz_ponderar,parqueaderos_ordenados

## Función que crea una matriz del tamaño de la matriz original del aeropuerto, con todos sus valores en NONE, aquí se registrará los pesos de cada casilla.
def matriz_pesos(filas,columnas):
    matriz_pesos = []
    for i in range(filas):
        matriz_pesos.append([None]*columnas)
    return matriz_pesos

## Función que guarda la matriz vacía a ponderar, crea el deque, y agrega al mismo las coordenadas de los puntos entradas/salidas, para posteriormente, 
## enviarlo a la función ponderar para asignar peso a cada casilla. La lista de movimientos indica como se puede mover el avión.
def pre_ponderacion(matriz_simbolos,filas,columnas):
    pesos = deque()
    movimientos = [[0,1],[1,0],[0,-1],[-1,0]]
    matriz_vacia = matriz_pesos(filas,columnas)
    for i in range(filas):
            for j in range(columnas):
                if matriz_simbolos[i][j] == '==':
                    matriz_vacia[i][j] = 0
                    pesos.append((i,j))
    return ponderar(matriz_simbolos,matriz_vacia,pesos,movimientos,filas,columnas)

## Funcion que evalua el numero de caminos que afecta parquear un avion en cada uno de los parqueaderos de lo matriz de simbolos. 
## En una matriz nueva, se asigna en la misma coordenada el numero de parqueaderos que afecta parquear un avion en dicha posicion.
## Ademas, se guarda en una lista el numero de afectaciones de cada parqueadero, para asi, sacar el minimo de la misma en la funcion "resolver_problema".
def numero_cambios(matriz_ponderar_vieja,matriz_simbolos,filas,columnas,parqueaderos):
    matriz_cambios = matriz_pesos(filas,columnas)
    numero_afectaciones = []
    for parqueadero in parqueaderos:
        contador = 0
        simbolo_casilla= matriz_simbolos[parqueadero[0][0]][parqueadero[0][1]]
        matriz_simbolos[parqueadero[0][0]][parqueadero[0][1]] = "##"
        matriz_ponderar_nueva,parqueaderos_ordenados = pre_ponderacion(matriz_simbolos,filas,columnas)
        for i in range(filas):
            for j in range(columnas):
                if (i,j) != (parqueadero[0][0],parqueadero[0][1]) and matriz_ponderar_vieja[i][j] != matriz_ponderar_nueva[i][j]:
                    contador+=1
        matriz_cambios[parqueadero[0][0]][parqueadero[0][1]] = contador
        matriz_simbolos[parqueadero[0][0]][parqueadero[0][1]] = simbolo_casilla
        numero_afectaciones.append(contador)
    return matriz_cambios,numero_afectaciones




## Función recursiva que recorre la lista de eventos, si el evento es positivo (avión aterriza), le asigna un parqueadero al avión,
## si el evento es negativo, busca una salida disponible. Al ser un algoritmo greedy, la condición que se toma, y no se evalua nuevamente es
## en donde parqueamos el avión, que será en la posicion que menos caminos afecte si se parquea un avion en ese lugar. (tambien, se recorre
## los parqueaderos de menor a mayor ponderacion, asi, si un parqueadero tiene una ponderacion baja pero no afecta a el camino de los demas,
## dicha posicion es optima para el parqueo de un avión, ya que no estorba, y ademas puede salir mas facil).
## Si un avion no puede parquear, o no puede salir, no se reevalua la condicion como se hacia en backtracking, sino que simplemente modificamos la 
## lista de eventos de manera que ese evento pueda llevarse a cabo satisfactoriamente. 
def resolver_problema(matriz_simbolos, matriz_ponderar, eventos, filas, columnas, lista_solucion, diccionario,parqueaderos,lista_eventos_nueva,lista_espera):
    if len(eventos)==0:
        return True
    else:
        evento_actual = eventos.popleft()
        if evento_actual<0 and abs(evento_actual) in lista_espera:
            lista_eventos_nueva.pop(lista_eventos_nueva.index(evento_actual))
            lista_eventos_nueva.append(evento_actual)
            eventos.append(evento_actual)
            lista_espera.pop(lista_espera.index(abs(evento_actual)))
            if resolver_problema(matriz_simbolos, matriz_ponderar, eventos, filas, columnas, lista_solucion, diccionario,parqueaderos,lista_eventos_nueva,lista_espera):
                return True
            else:
                return False
        else:
            if evento_actual>0:
                matriz,numero_afectaciones = numero_cambios(matriz_ponderar,matriz_simbolos,filas,columnas,parqueaderos)
                for parqueadero in parqueaderos:
                    if matriz_ponderar[parqueadero[0][0]][parqueadero[0][1]]!=None:
                        if matriz[parqueadero[0][0]][parqueadero[0][1]] == min(numero_afectaciones):
                            lista_solucion.append((matriz_simbolos[parqueadero[0][0]][parqueadero[0][1]], evento_actual))
                            diccionario[evento_actual] = ((parqueadero[0][0],parqueadero[0][1]),matriz_simbolos[parqueadero[0][0]][parqueadero[0][1]])
                            matriz_simbolos[parqueadero[0][0]][parqueadero[0][1]] = '##'
                            matriz_ponderar,parqueaderos = pre_ponderacion(matriz_simbolos,filas,columnas)
                            if resolver_problema(matriz_simbolos, matriz_ponderar, eventos, filas, columnas, lista_solucion, diccionario,parqueaderos,lista_eventos_nueva,lista_espera):
                                return True
                            else:
                                return False
                lista_eventos_nueva.pop(lista_eventos_nueva.index(evento_actual))
                lista_eventos_nueva.append(evento_actual)
                lista_espera.append(evento_actual)
                eventos.append(evento_actual)
                if resolver_problema(matriz_simbolos, matriz_ponderar, eventos, filas, columnas, lista_solucion, diccionario,parqueaderos,lista_eventos_nueva,lista_espera):
                    return True
                else:
                    return False
            else:
                evento_actual_2 = abs(evento_actual)
                movimientos = [[0,1],[1,0],[0,-1],[-1,0]]
                for i in range(len(movimientos)):
                    nueva_x = diccionario[evento_actual_2][0][0] + movimientos[i][0]
                    nueva_y = diccionario[evento_actual_2][0][1] + movimientos[i][1]
                    if casilla_es_valido(filas,columnas,nueva_x,nueva_y):
                        if matriz_ponderar[nueva_x][nueva_y] != None and matriz_ponderar[nueva_x][nueva_y] != -11:
                            if matriz_ponderar[nueva_x][nueva_y] >=0:
                                matriz_simbolos[diccionario[evento_actual_2][0][0]][diccionario[evento_actual_2][0][1]] = diccionario[evento_actual_2][1]
                                matriz_ponderar,parqueaderos = pre_ponderacion(matriz_simbolos,filas,columnas)
                                if resolver_problema(matriz_simbolos, matriz_ponderar, eventos, filas, columnas, lista_solucion, diccionario,parqueaderos,lista_eventos_nueva,lista_espera):
                                    return True
                                else:
                                    return False
                lista_eventos_nueva.pop(lista_eventos_nueva.index(evento_actual))
                lista_eventos_nueva.append(evento_actual)
                eventos.append(evento_actual)
                if resolver_problema(matriz_simbolos, matriz_ponderar, eventos, filas, columnas, lista_solucion, diccionario,parqueaderos,lista_eventos_nueva,lista_espera):
                    return True
                else:
                    return False


## Función principal, que se encarga de crear la matriz de simbolos (aeropuerto en general), almacenar los eventos en una lista, 
## generar la primera ponderación, hacer el llamado al algoritmo que soluciona el problema e imprimir la solución.
## Se crea una lista llamada "lista_eventos_nueva", la cual, en caso de no ser posible encontrar una solucion para la lista de eventos,
## se modifica, para hallar una combinacion en la cual se puedan cumplir todos los eventos.
## Así, si la lista de eventos que queremos modificar en dicho caso mencionado anteriormente, una vez evaluado los eventos, no cambió,
## imprime la solución al aeropuerto, en caso contrario, imprime la posible solucion del aeropuerto si se modificase dicha lista de eventos.
def principal():
    numero_caso = 0
    while(True):
        nfc = input().split()
        numero_aviones = int(nfc[0])
        if numero_aviones == 0:
            break
        else:
            numero_caso+=1
            numero_filas,numero_columnas = int(nfc[1]),int(nfc[2])
            lista_solucion = []
            diccionario = {}
            matriz_simbolos = []
            lista_espera_aviones = []
            for i in range(numero_filas):
                fila = input().split()
                matriz_simbolos.append(fila)
            eventos = deque(map(int, input().split()))
            lista_eventos_nueva = list(eventos)
            ponderacion_inicial,parqueaderos = pre_ponderacion(matriz_simbolos,numero_filas,numero_columnas)
            if len(parqueaderos)!=0:
                resolver_problema(matriz_simbolos, ponderacion_inicial, eventos.copy(), numero_filas, numero_columnas, lista_solucion, diccionario,parqueaderos,lista_eventos_nueva,lista_espera_aviones)
                lista_solucion_organizada = sorted(lista_solucion,key = lambda x: x[1])
                if eventos==deque(lista_eventos_nueva):
                    print("Case {}: Yes".format(numero_caso))
                    for i in range(len(lista_solucion_organizada)-1):
                        print(lista_solucion_organizada[i][0],end = " ")
                    print(lista_solucion_organizada[-1][0])
                else:
                    print("Case {}: No".format(numero_caso))
                    print("Si se modifica la lista de eventos de la siguiente forma: ")
                    for i in range(len(lista_eventos_nueva)-1):
                        print(lista_eventos_nueva[i],end = " ")
                    print(lista_eventos_nueva[-1])
                    print("Obtenemos la siguiente solucion: ")
                    for i in range(len(lista_solucion_organizada)-1):
                                print(lista_solucion_organizada[i][0],end = " ")
                    print(lista_solucion_organizada[-1][0])
            else:
                print("Case {}: No".format(numero_caso))


if __name__ == '__main__':
    principal()
