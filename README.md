# Airplane Scheduling
La actividad evaluativa del semestre en la asignatura **ESTRUCTRA DE DATOS Y ALGORITMOS 2** ha girado en torno al problema 11208 del juez en línea de la Universidad de Valladolid, titulado Airplane Scheduling. Este es un problema de backtracking, donde el tiempo de ejecución juega un papel vital en la solución al mismo.
# Contexto del problema
Los aeropuertos tienen un gran terreno llano para que los aviones aterricen y despeguen. El problema radica en la siguiente pregunta, ¿es posible que cada avión aterrice, se estacione, y despegue correctamente sin chocarse con otros aviones y/o atravesarse por lugares indebidos?.
Se  da  un  aeropuerto,  la  información  de  donde  aterrizan  los  aviones,  y  el  orden  con el cual ingresan y salen del aeropuerto.
# Algoritmo que se desarrolló
La función principal, llamada 'resolver_problema' se encarga de recorrer la lista de eventos ingresada por el usuario y verificar si se realiza un despegue o un aterrizaje, esto lo determina el signo del evento. Una vez identificada la acción a realizar, se debe encontrar un parqueadero accesible desde los puntos entrada/salida, y para esto, se planteó un algoritmo Greedy en la función 'ponderar', el cual le asigna un valor a todas las casillas desde los puntos iniciales, y almacena los parqueaderos accesibles. Ya teniendo los lugares donde se puede establecer el avion, se parquea el mismo y se continua evaluando los siguientes eventos, si finalmente no se llegó a una solución factible, se prueba establecer el evento actual en un nuevo parqueadero, para asi finalmente probar todas las posibilidades. Ahora bien, en el caso de que el evento sea un despegue, se verifica las casillas adyasentes al parqueadero en donde se estableció el avión, y si alguna de las mismas esta ponderada, significa que hay un camino hacia la salida desde ella, y por lo tanto, se define que desde el parqueadero actual, también se puede salir. En caso de que no exista una salida, se debe volver a evaluar el posicionamiento de los aviones. Si finalmente se probaron todas las posibilidades y no se llegó a una solución factible, se imprime que no existe un resultado, de lo contrario, se imprime el parqueadero en el que se debe establecer cada avion para que se llegue a una solucion factible.
Este algoritmo cumple con los casos en la plataforma de Udebug, pero, no pasa el jurado internacional de Online Judge por el limite de tiempo establecido.
# Mejoras a futuro
* Finalmente, en el proceso de evaluación del problema, se llegó a la conclusión que es importante la implementación de grafos para la solución del mismo, donde cada vertice representa un parqueadero (excepción del inicial, que es un punto de entrada/salida), y las aristas entre los mismos determinan hacia donde se puede llegar. 
* En el algoritmo Greedy para este mismo problema, presentado durante el curso, se llegó a la conclusión que el avión siempre debe intentar parquearse en una hoja del grafo, asi, se evita bloquear la menor cantidad de parqueaderos disponibles, mejorando lo planteado en un inicio, de siempre ubicarlo en la casilla de mayor ponderación, ya que a la hora de un avión despegar, es más probable que el mismo no lo puediese hacer, ya que existirían otros aviones los cuales bloqueaban su salida.
* También se planteo un concepto muy importante, las "restricciones", el cual es un algoritmo que nos ayuda a determinar que aviones no se pueden establecer en el camino de otro evento, así, reduciendo la cantidad de casos que se evaluan.
### Sobre el contenido en el repositorio
En el repositorio se encuentran varias carpetas, las cuales en cada una se almacena un codigo, junto a los avances que se realizaron durante la semana de trabajo. la carpeta llamada 'entrega final', contiene el codigo presentado, junto al informe final propuesto por el docente de la asignatura.
### Autor
Kristian Restrepo Osorio
