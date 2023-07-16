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
def ponderar (matriz_simbolos,matriz_ponderar,pesos,movimientos,filas,columnas):
    visitados = set()
    parqueaderos = set()
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
                    parqueaderos.add((nueva_x,nueva_y))
    return matriz_ponderar,parqueaderos

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

## Función recursiva que recorre la lista de eventos, si el evento es positivo (avión aterriza), le asigna un parqueadero al avión,
## si el evento es negativo, busca una salida disponible. De no ser posible dicha salida, se realiza backtracking, acomodando nuevamente los
## aviones hasta encontrar una solución factible.
def resolver_problema(matriz_simbolos, matriz_ponderar, eventos, filas, columnas, lista_solucion, diccionario,parqueaderos):
    contador = 0
    if len(eventos)==0:
        return True
    for i in range(len(eventos)):
        if eventos[i]>0:
            contador+=1
        else:
            break
    if contador > len(parqueaderos):
        return False
    else:
        evento_actual = eventos.popleft()
        if evento_actual>0:
            for i in parqueaderos:
                    if matriz_ponderar[i[0]][i[1]]!=None:
                        if  matriz_ponderar[i[0]][i[1]]>0:
                            lista_solucion.append((matriz_simbolos[i[0]][i[1]], evento_actual))
                            diccionario[evento_actual] = ((i[0],i[1]),matriz_simbolos[i[0]][i[1]])
                            matriz_simbolos[i[0]][i[1]] = '##'
                            matriz_ponderar,parqueaderos = pre_ponderacion(matriz_simbolos,filas,columnas)
                            if resolver_problema(matriz_simbolos, matriz_ponderar, eventos, filas, columnas, lista_solucion, diccionario,parqueaderos):
                                return True
                            else:
                                lista_solucion.pop()
                                matriz_simbolos[diccionario[evento_actual][0][0]][diccionario[evento_actual][0][1]] = diccionario[evento_actual][1]
                                matriz_ponderar,parqueaderos = pre_ponderacion(matriz_simbolos,filas,columnas)
                                diccionario.pop(evento_actual)
            eventos.appendleft(evento_actual)
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
                            if resolver_problema(matriz_simbolos, matriz_ponderar, eventos, filas, columnas, lista_solucion, diccionario,parqueaderos):
                                return True
                            break
            matriz_simbolos[diccionario[evento_actual_2][0][0]][diccionario[evento_actual_2][0][1]] = "##"
            matriz_ponderar,parqueaderos = pre_ponderacion(matriz_simbolos,filas,columnas)
            eventos.appendleft(evento_actual)
            return False

## Función principal, que se encarga de crear la matriz de simbolos (aeropuerto en general), almacenar los eventos en una lista, 
## generar la primera ponderación, hacer el llamado al algoritmo que soluciona el problema e imprimir la solución.
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
            for i in range(numero_filas):
                fila = input().split()
                matriz_simbolos.append(fila)
            eventos = deque(map(int, input().split()))
            ponderacion_inicial,pq = pre_ponderacion(matriz_simbolos,numero_filas,numero_columnas)
            resultado = resolver_problema(matriz_simbolos, ponderacion_inicial, eventos, numero_filas, numero_columnas, lista_solucion, diccionario,pq)
            lista_solucion_organizada = sorted(lista_solucion,key = lambda x: x[1])
            if resultado:
                print("Case {}: Yes".format(numero_caso))
                for i in range(len(lista_solucion)-1):
                    print(lista_solucion_organizada[i][0],end = " ")
                print(lista_solucion_organizada[-1][0])
            else:
                print("Case {}: No".format(numero_caso))
if __name__ == '__main__':
    principal()
