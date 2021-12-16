import queue
import sys
import time


class Nodo:
    """ Esta clase representa cada estado del problema"""
    def __init__(self, pos_barco, diccionario_pos_id, lista_p_init, lista_p_1, lista_p_2, coste_acumulado, parent, accion):
        """ Aqui se define cada atributo de la clase Nodo"""
        # parent es el nodo padre del nodo actual
        self.parent = parent
        # pos_barco es el puerto en el que se encuentra el barco en este nodo (0, 1 o 2)
        self.pos_barco = pos_barco
        # diccionario_pos_id es el diccionario que indica que contenedores estan en cada psoicion valida de la matriz
        # del barco, las claves son las posiciones validas y sus valores los contenedores (o '' si esta vacia)
        self.diccionario_pos_id = diccionario_pos_id
        # lista_p_init contiene los contenedores que se encuentran en el peurto inicial en este nodo
        self.lista_p_init = lista_p_init
        # lista_p_1 contiene los contenedores que se encuentran en el peurto 1 en este nodo
        self.lista_p_1 = lista_p_1
        # lista_p_2 contiene los contenedores que se encuentran en el peurto 2 en este nodo
        self.lista_p_2 = lista_p_2
        # coste_acumulado indica el coste acumulado hasta este nodo
        self.coste_acumulado = coste_acumulado
        # accion indica la accion inmediatamente anterior que se llevo a cabo para llegar a este nodo
        self.accion = accion

    def get_sucesores(self):
        """ Este metodo se utiliza para generar los sucesores del nodo actual"""
        # Creamos una lista vacia en la que iremos incluyendo los sucesores si cumplen
        # las precondiciones de cada operador
        # Solo se incluiran en la lista de sucesores aquellos que no se hayan generado anteriormente
        # y cuya accion no sea la misma que la de su nodo padre (el nodo actual)
        sucesores = []
        # Iteramos por cada contenedor y posicion posible en el barco
        for contenedor in dic_valores.keys():
            for pos in self.diccionario_pos_id.keys():
                # Calculamos los sucesores que puedan resultar del operador cargar
                sucesores_carga = self._cargar(self.pos_barco, contenedor, pos)
                if sucesores_carga != None and sucesores_carga not in sucesores and sucesores_carga[1].accion != self.accion:
                    sucesores.append(sucesores_carga)
                # Calculamos los sucesores que puedan resultar del operador cargar_refrigerado
                sucesores_carga_refrig = self._cargar_refrigerado(self.pos_barco, contenedor, pos)
                if sucesores_carga_refrig != None and sucesores_carga_refrig not in sucesores and sucesores_carga_refrig[1].accion != self.accion:
                    sucesores.append(sucesores_carga_refrig)
                # Calculamos los sucesores que puedan resultar del operador descargar
                sucesores_descarga = self._descargar(self.pos_barco, contenedor, pos)
                if sucesores_descarga != None and sucesores_descarga not in sucesores and sucesores_descarga[1].accion != self.accion:
                    sucesores.append(sucesores_descarga)
                # Calculamos los sucesores que puedan resultar del operador navegar
                sucesores_navegar = self._navegar(self.pos_barco)
                if sucesores_navegar != None and sucesores_navegar not in sucesores and sucesores_navegar[1].accion != self.accion:
                    sucesores.append(sucesores_navegar)
        return sucesores

    def _cargar(self, pos_barco, contenedor, pos_en_matriz):
        """ Este operador simula la carga de un contenedor normal en el barco"""
        # Si el barco se encuentra en el puerto inicial, el contenedor a cargar esta en ese puerto
        # y no es refrigerado ni esta en el barco, se cumplen las precondiciones
        if pos_barco == 0 and contenedor in self.lista_p_init and dic_valores[contenedor][1] != 'R' and contenedor not in self.diccionario_pos_id.values():
            # Confirmamos que la posicion es valida y calculamos la profundidad a traves de una funcion auxiliar
            profundidad, valid = self.colocar_en_matriz(pos_en_matriz)
            if valid:
                # Copiamos el diccionario de posiciones del nodo actual y, en la copia, incluimos el contenedor a cargar
                # en la posicion indicada
                dic_local = self.diccionario_pos_id.copy()
                dic_local[pos_en_matriz] = contenedor
                # Copiamos la lista del puerto inicial y eliminamos de ella el contenedor que vamos a cargar en el barco
                lista_p_init_local = list(self.lista_p_init)
                lista_p_init_local.remove(contenedor)
                # Copiamos el coste a una variable local y lo incrementamos con el coste de carga
                coste_acumulado_local = self.coste_acumulado
                coste_acumulado_local += (10+profundidad)
                # Creamos una instancia de la clase Nodo con los cambios hechos que sera un sucesor del nodo actual
                sucesor = Nodo(pos_barco, dic_local, lista_p_init_local, self.lista_p_1, self.lista_p_2, coste_acumulado_local, self, "cargar("+str(pos_barco)+","+str(contenedor)+","+str(pos_en_matriz)+")")
                # Devolvemos una tupla de la forma (f(x), sucesor),
                # donde f(x) es la suma del coste acumulado y la heuristica
                return tuple([coste_acumulado_local + heuristica(self), sucesor])
        # Si el barco se encuentra en el puerto 1, el contenedor a cargar esta en ese puerto
        # y no es refrigerado ni esta en el barco, se cumplen las precondiciones, si no devolvera None
        elif pos_barco == 1 and contenedor in self.lista_p_1 and dic_valores[contenedor][1] != 'R' and contenedor not in self.diccionario_pos_id.values() and dic_valores[contenedor][0] == '2':
            # Confirmamos que la posicion es valida y calculamos la profundidad a traves de una funcion auxiliar
            profundidad, valid = self.colocar_en_matriz(pos_en_matriz)
            if valid:
                # Copiamos el diccionario de posiciones del nodo actual y, en la copia, incluimos el contenedor a cargar
                # en la posicion indicada
                dic_local = self.diccionario_pos_id.copy()
                dic_local[pos_en_matriz] = contenedor
                # Copiamos la lista del puerto 1 y eliminamos de ella el contenedor que vamos a cargar en el barco
                lista_p_1_local = list(self.lista_p_1)
                lista_p_1_local.remove(contenedor)
                # Copiamos el coste a una variable local y lo incrementamos con el coste de carga
                coste_acumulado_local = self.coste_acumulado
                coste_acumulado_local += (10 + profundidad)
                # Creamos una instancia de la clase Nodo con los cambios hechos que sera un sucesor del nodo actual
                sucesor = Nodo(pos_barco, dic_local, self.lista_p_init, lista_p_1_local, self.lista_p_2, coste_acumulado_local, self, "cargar(" + str(pos_barco) + "," + str(contenedor) + "," + str(pos_en_matriz) + ")")
                # Devolvemos una tupla de la forma (f(x), sucesor),
                # donde f(x) es la suma del coste acumulado y la heuristica
                return tuple([coste_acumulado_local + heuristica(self), sucesor])

    def _cargar_refrigerado(self, pos_barco, contenedor, pos_en_matriz):
        """ Este operador simula la carga de un contenedor refrigerado en el barco"""
        # Si el barco se encuentra en el puerto inicial, el contenedor a cargar esta en ese puerto, es refrigerado
        # y no esta en el barco, se cumplen las precondiciones
        if pos_barco == 0 and contenedor in self.lista_p_init and dic_valores[contenedor][1] == 'R' and contenedor not in self.diccionario_pos_id.values():
            # Confirmamos que la posicion es valida y calculamos la profundidad a traves de una funcion auxiliar
            profundidad, valid = self.colocar_en_matriz_refrig(pos_en_matriz)
            if valid:
                # Copiamos el diccionario de posiciones del nodo actual y, en la copia, incluimos el contenedor a cargar
                # en la posicion indicada
                dic_local = self.diccionario_pos_id.copy()
                dic_local[pos_en_matriz] = contenedor
                # Copiamos la lista del puerto inicial y eliminamos de ella el contenedor que vamos a cargar en el barco
                lista_p_init_local = list(self.lista_p_init)
                lista_p_init_local.remove(contenedor)
                # Copiamos el coste a una variable local y lo incrementamos con el coste de carga
                coste_acumulado_local = self.coste_acumulado
                coste_acumulado_local += (10 + profundidad)
                # Creamos una instancia de la clase Nodo con los cambios hechos que sera un sucesor del nodo actual
                sucesor = Nodo(pos_barco, dic_local, lista_p_init_local, self.lista_p_1, self.lista_p_2, coste_acumulado_local, self, "cargar_refrigerado("+str(pos_barco)+","+str(contenedor)+","+str(pos_en_matriz)+")")
                # Devolvemos una tupla de la forma (f(x), sucesor),
                # donde f(x) es la suma del coste acumulado y la heuristica
                return tuple([coste_acumulado_local + heuristica(self), sucesor])
        # Si el barco se encuentra en el puerto 1, el contenedor a cargar esta en ese puerto, es refrigerado
        # y no esta en el barco, se cumplen las precondiciones, si no devolvera None
        elif pos_barco == 1 and contenedor in self.lista_p_1 and dic_valores[contenedor][1] == 'R' and contenedor not in self.diccionario_pos_id.values() and dic_valores[contenedor][0] == '2':
            # Confirmamos que la posicion es valida y calculamos la profundidad a traves de una funcion auxiliar
            profundidad, valid = self.colocar_en_matriz_refrig(pos_en_matriz)
            if valid:
                # Copiamos el diccionario de posiciones del nodo actual y, en la copia, incluimos el contenedor a cargar
                # en la posicion indicada
                dic_local = self.diccionario_pos_id.copy()
                dic_local[pos_en_matriz] = contenedor
                # Copiamos la lista del puerto 1 y eliminamos de ella el contenedor que vamos a cargar en el barco
                lista_p_1_local = list(self.lista_p_1)
                lista_p_1_local.remove(contenedor)
                # Copiamos el coste a una variable local y lo incrementamos con el coste de carga
                coste_acumulado_local = self.coste_acumulado
                coste_acumulado_local += (10 + profundidad)
                # Creamos una instancia de la clase Nodo con los cambios hechos que sera un sucesor del nodo actual
                sucesor = Nodo(pos_barco, dic_local, self.lista_p_init, lista_p_1_local, self.lista_p_2, coste_acumulado_local, self, "cargar_refrigerado(" + str(pos_barco) + "," + str(contenedor) + "," + str(pos_en_matriz) + ")")
                # Devolvemos una tupla de la forma (f(x), sucesor),
                # donde f(x) es la suma del coste acumulado y la heuristica
                return tuple([coste_acumulado_local + heuristica(self), sucesor])

    def colocar_en_matriz(self, pos_en_matriz):
        """ Metodo auxiliar de cargar que nos permite verificar que la posicion en la que se quiere cargar el contenedor
        es valida. Una posicion es valida solo si es encima del suelo o de otro contenedor
        (no puede estar flotando el contenedor que queremos colocar)"""
        if ((pos_en_matriz) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz] != '') or ((pos_en_matriz + N) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz + N] == ''):
            return None, False
        return pos_en_matriz // N, True

    def colocar_en_matriz_refrig(self, pos_en_matriz):
        """ Metodo auxiliar de cargar que nos permite verificar que la posicion en la que se quiere cargar el contenedor
        refrigerado es valida. Una posicion es valida para un contenedor refrigerado solo si es una celda de energis y
        esta encima del suelo o de otro contenedor (no puede estar flotando el contenedor que queremos colocar)"""
        if matriz_celdas[pos_en_matriz // N][pos_en_matriz % N] != 'E' or ((pos_en_matriz) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz] != '') or ((pos_en_matriz + N) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz + N] == ''):
            return None, False
        return pos_en_matriz // N, True

    def _descargar(self, pos_barco, contenedor, pos_en_matriz):
        """ Este operador simula la descarga de un contenedor del barco en el puerto en el que se encuentre"""
        # Si el barco se encuentra en el puerto 1, el contenedor a descargar esta en la posicion del barco indicada
        # y no tiene ningun contenedor encima o esta en el top del stack y no esta en el puerto 1,
        # se cumplen las precondiciones
        if pos_barco == 1 and self.diccionario_pos_id[pos_en_matriz] == contenedor and contenedor in list(self.diccionario_pos_id.values()) and (pos_en_matriz // N == 0 or ((pos_en_matriz - N) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz - N] == '')) and contenedor not in self.lista_p_1:
            # Copiamos el diccionario de posiciones del nodo actual y, en la copia, quitamos el contenedor a descargar
            # de la posicion indicada del barco
            dic_local = self.diccionario_pos_id.copy()
            dic_local[pos_en_matriz] = ''
            # Copiamos la lista del puerto 1 y incluimos en ella el contenedor que vamos a descargar del barco
            lista_p_1_local = list(self.lista_p_1)
            lista_p_1_local.append(contenedor)
            # Copiamos el coste a una variable local y lo incrementamos con el coste de descarga
            coste_acumulado_local = self.coste_acumulado
            coste_acumulado_local += (15 + 2 * (pos_en_matriz // N))
            # Creamos una instancia de la clase Nodo con los cambios hechos que sera un sucesor del nodo actual
            sucesor = Nodo(pos_barco, dic_local, self.lista_p_init, lista_p_1_local, self.lista_p_2, coste_acumulado_local, self, "descargar(" + str(pos_barco) + "," + str(contenedor) + "," + str(pos_en_matriz) + ")")
            # Devolvemos una tupla de la forma (f(x), sucesor),
            # donde f(x) es la suma del coste acumulado y la heuristica
            return tuple([coste_acumulado_local + heuristica(self), sucesor])
        # Si el barco se encuentra en el puerto 2, el contenedor a descargar esta en la posicion del barco indicada
        # y no tiene ningun contenedor encima o esta en el top del stack y no esta en el puerto 1,
        # se cumplen las precondiciones, si no devolvera None
        elif pos_barco == 2 and self.diccionario_pos_id[pos_en_matriz] == contenedor and contenedor in self.diccionario_pos_id.values() and (pos_en_matriz // N == 0 or ((pos_en_matriz - N) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz - N] == '')) and contenedor not in self.lista_p_2:
            # Copiamos el diccionario de posiciones del nodo actual y, en la copia, quitamos el contenedor a descargar
            # de la posicion indicada del barco
            dic_local = self.diccionario_pos_id.copy()
            dic_local[pos_en_matriz] = ''
            # Copiamos la lista del puerto 2 y incluimos en ella el contenedor que vamos a descargar del barco
            lista_p_2_local = list(self.lista_p_2)
            lista_p_2_local.append(contenedor)
            # Copiamos el coste a una variable local y lo incrementamos con el coste de descarga
            coste_acumulado_local = self.coste_acumulado
            coste_acumulado_local += (15 + 2 * (pos_en_matriz // N))
            # Creamos una instancia de la clase Nodo con los cambios hechos que sera un sucesor del nodo actual
            sucesor = Nodo(pos_barco, dic_local, self.lista_p_init, self.lista_p_1, lista_p_2_local, coste_acumulado_local, self, "descargar(" + str(pos_barco) + "," + str(contenedor) + "," + str(pos_en_matriz) + ")")
            # Devolvemos una tupla de la forma (f(x), sucesor),
            # donde f(x) es la suma del coste acumulado y la heuristica
            return tuple([coste_acumulado_local + heuristica(self), sucesor])

    def _navegar(self, pos_barco):
        """ Este operador simula la navegacion del barco de un puerto al siguiente"""
        # Si el barco se encuentra en el puerto 1 se cumplen las precondiciones
        if pos_barco == 1:
            # Si algun contenedor de los que lleva el barco va al puerto 1, no puede navegar
            for contenedor in self.diccionario_pos_id.values():
                if contenedor != '' and dic_valores[contenedor][0] == '1':
                    return None
            # Copiamos el coste a una variable local y lo incrementamos con el coste de navegar
            coste_acumulado_local = self.coste_acumulado
            coste_acumulado_local += 3500
            # Creamos una instancia de la clase Nodo con los cambios hechos que sera un sucesor del nodo actual
            # El barco pasara al siguiente puerto (pos_barco+1)
            sucesor = Nodo(pos_barco+1, self.diccionario_pos_id.copy(), self.lista_p_init, self.lista_p_1, self.lista_p_2, coste_acumulado_local, self, "navegar("+str(pos_barco)+")")
            # Devolvemos una tupla de la forma (f(x), sucesor),
            # donde f(x) es la suma del coste acumulado y la heuristica
            return tuple([coste_acumulado_local + heuristica(self), sucesor])
        # Si el barco se encuentra en el puerto inicial se cumplen las precondiciones
        elif pos_barco == 0:
            # Si no ha cargado algun contenedor no puede navegar
            for contenedor in dic_valores.keys():
                if contenedor in self.lista_p_init:
                    return None
            # Copiamos el coste a una variable local y lo incrementamos con el coste de navegar
            coste_acumulado_local = self.coste_acumulado
            coste_acumulado_local += 3500
            # Creamos una instancia de la clase Nodo con los cambios hechos que sera un sucesor del nodo actual
            # El barco pasara al siguiente puerto (pos_barco+1)
            sucesor = Nodo(pos_barco + 1, self.diccionario_pos_id.copy(), self.lista_p_init, self.lista_p_1, self.lista_p_2,
                           coste_acumulado_local, self, "navegar(" + str(pos_barco) + ")")
            # Devolvemos una tupla de la forma (f(x), sucesor),
            # donde f(x) es la suma del coste acumulado y la heuristica
            return tuple([coste_acumulado_local + heuristica(self), sucesor])

    def __lt__(self, other):
        """ Este metodo nos permite elegir que nodo es menor a otro. Se tendra en cuenta unicamente el coste acumulado"""
        if self.coste_acumulado < other.coste_acumulado:
            return True
        return False

    def __eq__(self, other):
        """ Este metodo se utiliza para poder comparar instancias de Nodo.
        Dos nodos son iguales solo si el valor de sus listas, diccionario de posiciones y posicion del barco son iguales"""
        for cont in self.lista_p_init:
            if cont not in other.lista_p_init:
                return False
        for cont in self.lista_p_1:
            if cont not in other.lista_p_1:
                return False
        for cont in self.lista_p_2:
            if cont not in other.lista_p_2:
                return False
        if self.pos_barco != other.pos_barco or self.diccionario_pos_id != other.diccionario_pos_id:
            return False
        return True


class Aestrella:
    """ Esta clase define el algoritmo de busqueda A* para la resolucion del problema"""
    def __init__(self, tupla_nodo_init):
        """ Aqui se define cada atributo de la clase Aestrella"""
        # abierta representa, como una cola con prioridad, la cola abierta del algoritmo
        self.abierta = queue.PriorityQueue()
        # Se incluye en abierta la tupla con el nodo inicial del problema
        self.abierta.put(tupla_nodo_init)
        # cerrada representa la lista cerrada del problema
        self.cerrada = []
        # exito es una variable booleana que indica si se ha llegado al estado final
        self.exito = False
        # nodos_expandidos es una variable que lleva la cuenta de cuantos nodos han sido expandidos en la busqueda
        self.nodos_expandidos = 0

    def solve(self):
        """ Este metodo incluye la implementacion del algoritmo de A* para la resolucion de problemas de busqueda"""
        # Hasta que la cola abierta este vacia o el atributo exito sea verdadero se ejecuta el bucle
        while not self.abierta.empty() and not self.exito:
            # Se van cogiendo nodos de la cola abierta hasta encontrar uno que no este en la lista cerrada
            primer_nodo_abierta = self.abierta.get()
            while primer_nodo_abierta in self.cerrada:
                primer_nodo_abierta = self.abierta.get()

            # Si el nodo corresponde al estado final entonces la variable exito pasa a ser verdadera
            if is_final(primer_nodo_abierta[1]):
                self.exito = True
            else:
                # Si no se expande el nodo y se mete en cerrada, generando el conjunto de sus sucesores
                self.cerrada.append(primer_nodo_abierta)
                successors = primer_nodo_abierta[1].get_sucesores()
                # Se incrementa el contador de nodos expandidos
                self.nodos_expandidos += 1
                # cada sucesor se incluye en la cola abierta
                for s in successors:
                    self.abierta.put(s)

        # Se crea una lista vacia, que se ira rellenando con las acciones de solucion en caso de exito
        solucion = []
        if self.exito:
            # Iteramos por los padres de cada nodo , subiendo en el arbol hasta llegar al nodo inicial
            nodo = primer_nodo_abierta[1]
            while nodo.parent is not None:
                # Se incluye en la lista la accion que llevo a cada nodo a crearse
                solucion.append(nodo.accion)
                nodo = nodo.parent
        # Se devuelve una tupla con la lista de acciones, el numero de nodos expandidos y el coste total
        # El coste total es igual al coste acumulado del ultimo nodo de la solucion
        # ya que la heuristica en ese nodo es 0
        return solucion, self.nodos_expandidos, primer_nodo_abierta[1].coste_acumulado


def heuristica(nodo):
    """ La funcion heuristica nos permite calcular el valor de la heuristica que se usara para calcular f(x) en A*
    Dependiendo de que heuristica se eligiera en los argumentos se usara una o la otra:
    -La primera heuristica solo tiene en cuenta los contenedores que no estan en sus puertos de destino
    -La segunda heuristica ademas de los contenedores que faltan por llegar a su destino tiene en cuenta sus
    costes fijos de carga y descarga"""
    if HEURISTICA == 'heuristica1':
        return len(dic_valores.keys()) - (len(nodo.lista_p_1) + len(nodo.lista_p_2))
    elif HEURISTICA == 'heuristica2':
        return (len(dic_valores.keys()) - (len(nodo.lista_p_1) + len(nodo.lista_p_2))) * (25)


def is_final(nodo):
    """ Esta funcion nos permite decidir si un estado es el estado final.
    Un estado final tiene que estar necesariamente fuera del peurto inicial y la no puede
    haber contenedores en el puerto inicial. Ademas, el barco no puede tener ontenedores encima en ese estado y
    todos los contenedores que fueran al puerto 1 deben estar en el puerto 1 y los que fueran al 2 en el peurto 2."""
    if (nodo.pos_barco == 0) or len(nodo.lista_p_init) > 0:
        return False
    for i in nodo.diccionario_pos_id.values():
        if i != '':
            return False
    for contenedor in dic_valores.keys():
        if (dic_valores[contenedor][0] == '1' and contenedor not in nodo.lista_p_1) or (dic_valores[contenedor][0] == '2' and contenedor not in nodo.lista_p_2):
            return False
    return True


abierta = []
cerrada = []
exito = False

# Guardamos los argumentos en variables
PATH = sys.argv[1] + "/"
MAPA = PATH + sys.argv[2]
CONTENEDORES = PATH + sys.argv[3]
HEURISTICA = sys.argv[4]

# Calculamos el numero de filas y de columnas total de la matriz que lleva el barco.
# Teniendo en cuenta que pueda haber unas filas con menos elementos que otras para prevenir futuros errores
counter_i = 0
counter_j = 0
M = 0
N = 0
try:
    # Abrimos el archivo del mapa
    with open(MAPA, "r+", encoding='utf-8', newline="") as file:
        # Iteramos por cada linea y por cada caracter dentro de cada linea
        for line in file:
            counter_j = 0
            for character in line:
                # Solo incrementamos el contador de columnas si se trata de un caracter valido para el problema
                if character != ' ' and character != '\r' and character != '\n':
                    counter_j += 1
            # Si una fila tiene mas caracteres que otra actualizamos el numero total de columnas
            if counter_j > N:
                N = counter_j
            counter_i += 1
        # Pasamos el valor del numero total de filas a la variable M
        M = counter_i
except FileNotFoundError as ex:
    # En caso de no poder abrir el archivo del mapa saltará una excepcion
    raise Exception("Wrong file or file path\n") from ex

# Declaramos las listas que seran los dominios y se rellenaran mas tarde
dominio1 = []
dominio2 = []
# Declaramos las variables que usaremos para parsear el input del mapa
# En matriz_celdas colocaremos los elementos del mapa tal y como se pasaron por input
i = 0
counter = 0
matriz_celdas = []
try:
    # Abrimos el archivo del mapa
    with open(MAPA, "r+", encoding='utf-8', newline="") as file:
        for line in file:
            # Por cada fila en el archivo ponemos una lista mas en la lista de listas (matriz)
            matriz_celdas.append([])
            # Inicializamos la variable prev_character que nos indicara el valor del caracter anterior
            # La utilizaremos para poder rellenar la matriz con 'X'
            # en las celdas en las que el mapa input no haya definido ningun valor
            prev_character = 'X'
            j = 0
            for character in line:
                if (prev_character == ' ' or character != ' ' or (j == 0 and character == ' ' [0] == character)) and character != '\r' and character != '\n':
                    # Si el primer caracter es un espacio rellenamos el hueco con una 'X'
                    if character == ' ':
                        matriz_celdas[i].append('X')
                    else:
                        # Si el caracter no es un espacio se incuira en la matriz el elemento del mapa
                        matriz_celdas[i].append(character)
                    prev_character = 'X'
                    # Si el caracter no es una 'X' ni un espacio incluimos esa posicion en el dominio1
                    # Y si ademas la celda es de Energia se guarda la posicion en el dominio2
                    if character != 'X' and character != ' ':
                        dominio1.append(counter)
                        if character == 'E':
                            dominio2.append(counter)
                    counter += 1
                # Si el caracter actual es un espacio actualizamos la variable prev_character
                # para la siguiente iteracion
                if character == ' ':
                    prev_character = ' '
                j += 1
            # Rellenamos la fila con 'X' si no habia tantos caracteres como el numero total de columnas
            if len(matriz_celdas[i]) < N:
                matriz_celdas[i].append('X')
            i += 1

except FileNotFoundError as ex:
    # En caso de no poder abrir el archivo del mapa saltará una excepcion
    raise Exception("Wrong file or file path\n") from ex

# Declaramos el diccionario donde se relacionaran los contenedores con sus datos: puerto destino y tipo de contenedor
dic_valores = {}
try:
    # Abrimos el archivo de contenedores
    with open(CONTENEDORES, "r+", encoding='utf-8', newline="") as file:
        for line in file:
            i = 0
            buf1 = ''
            while line[i] != ' ':
                buf1 += line[i]
                i += 1
            # Por cada linea incluimos una entrada al diccionario con key igual al id del contenedor
            # y valor asociado una lista con el puerto destino y el tipo de contenedor
            dic_valores[str(buf1)] = [str(line[i + 3]), str(line[i + 1])]

except FileNotFoundError as ex:
    # En caso de no poder abrir el archivo del mapa saltará una excepcion
    raise Exception("Wrong file or file path\n") from ex

# Creamos un diccionario que relaciona cada posicion valida en la matriz con el contenedor que la está ocupando
# En caso de ser '' el valor, significara que esa posicion esta vacia
diccionario_pos_id = {}
for i in dominio1:
    diccionario_pos_id[i] = ''

# Guardamo el tiempo actual en una variable
t1 = time.time()

# Creamos el estado (nodo) inicial del problema:
# Barco en puerto inicial (0), todos los contenedores en el puerto inicial, el resto de puertos vacios,
# coste acumulado 0, no tendra nodo padre (es el primero) y no se ha llegado a el por medio de ninguna accion ("")
nodo_init = Nodo(0, diccionario_pos_id, list(dic_valores.keys()), [], [], 0, None, "")
# Se crea la tupla (f(x), nodo). En este caso como no hay coste acumulado, f(x) es igual a la heuristica
tupla_nodo_init = tuple([heuristica(nodo_init), nodo_init])

# Inicializamos el algoritmo A* con la tupla del nodo inicial
aestrella = Aestrella(tupla_nodo_init)
# Resolvemos el problema usando A*
solucion = aestrella.solve()

# Guardamos el tiempo actual en una variable
t2 = time.time()
# Calculamos el tiempo transcurrido desde las dos mediciones para saber cuanto ha tardado A* en resolver el problema
tiempo_total = t2 - t1

try:
    # Creamos y abrimos un archivo de salida donde escribiremos la secuencia de acciones para llegar a la solucion
    with open(PATH + sys.argv[2] +"-"+sys.argv[3]+"-"+sys.argv[4]+".output", "w+", encoding='utf-8', newline="") as file:
        # Por cada accion en la lista devuelta en la primera posicion de la tupla de solucion
        # escribimos en el archivo de salida cada accion en una linea
        for acciones in range(1, len(solucion[0])+1):
            file.write(solucion[0][(-1) * acciones] + "\n")

except FileNotFoundError as ex:
    # En caso de no poder abrir el archivo del mapa saltará una excepcion
    raise Exception("Wrong file or file path\n") from ex
# Cerramos el archivo
file.close()
try:
    # CReamos y abrimos otro archivo de salida donde escribiremos las estadisticas de la resolucion del problema
    with open(PATH + sys.argv[2] +"-"+sys.argv[3]+"-"+sys.argv[4]+".stat", "w+", encoding='utf-8', newline="") as file:
        # Escribimos en una linea el tiempo transcurrido
        file.write("Tiempo total: " + str(tiempo_total) + "\n")
        # Escribimos en otra linea el coste total del problema
        file.write("Coste total: " + str(solucion[2]) + "\n")
        # Escribimos en otra linea el numero de acciones llevadas a cabo para solucionar el problema
        file.write("Longitud del plan: " + str(len(solucion[0])) + "\n")
        # Escribimos en otra linea el numero total de nodos expandidos
        file.write("Nodos expandidos: " + str(solucion[1]) + "\n")

except FileNotFoundError as ex:
    # En caso de no poder abrir el archivo del mapa saltará una excepcion
    raise Exception("Wrong file or file path\n") from ex
# Cerramos el archivo
file.close()
