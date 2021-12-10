import queue
import sys

class Nodo:
    def __init__(self, pos_barco, diccionario_pos_id, lista_p_init, lista_p_1, lista_p_2, coste_acumulado, parent, accion):
        self.parent = parent
        self.pos_barco = pos_barco
        self.diccionario_pos_id = diccionario_pos_id
        #print(str(self.diccionario_pos_id) + ' del constructor')
        self.lista_p_init = lista_p_init
        #print(str(self.lista_p_init) + ' del constructor')
        self.lista_p_1 = lista_p_1
        self.lista_p_2 = lista_p_2
        self.coste_acumulado = coste_acumulado
        self.accion = accion
        #self.successors = self.get_sucesores()

    def get_sucesores(self):
        sucesores = []
        #print(self.lista_p_init)
        for contenedor in dic_valores.keys():
            for pos in self.diccionario_pos_id.keys():
                sucesores_carga = self._cargar(self.pos_barco, contenedor, pos)
                if sucesores_carga != None and sucesores_carga not in sucesores and sucesores_carga[1].accion != self.accion:
                    sucesores.append(sucesores_carga)
                sucesores_carga_refrig = self._cargar_refrigerado(self.pos_barco, contenedor, pos)
                if sucesores_carga_refrig != None and sucesores_carga_refrig not in sucesores and sucesores_carga_refrig[1].accion != self.accion:
                    sucesores.append(sucesores_carga_refrig)
                sucesores_descarga = self._descargar(self.pos_barco, contenedor, pos)
                if sucesores_descarga != None and sucesores_descarga not in sucesores and sucesores_descarga[1].accion != self.accion:
                    sucesores.append(sucesores_descarga)
                sucesores_navegar = self._navegar(self.pos_barco)
                if sucesores_navegar != None and sucesores_navegar not in sucesores and sucesores_navegar[1].accion != self.accion:
                    sucesores.append(sucesores_navegar)
        return sucesores

    def _cargar(self, pos_barco, contenedor, pos_en_matriz):
        if pos_barco == 0 and contenedor in self.lista_p_init and dic_valores[contenedor][1] != 'R' and contenedor not in self.diccionario_pos_id.values():
            profundidad, valid = self.colocar_en_matriz(pos_en_matriz)
            if valid:
                dic_local = self.diccionario_pos_id.copy()
                dic_local[pos_en_matriz] = contenedor
                lista_p_init_local = list(self.lista_p_init)
                lista_p_init_local.remove(contenedor)
                coste_acumulado_local = self.coste_acumulado
                coste_acumulado_local += (10+profundidad)
                sucesor = Nodo(pos_barco, dic_local, lista_p_init_local, self.lista_p_1, self.lista_p_2, coste_acumulado_local, self, "cargar("+str(pos_barco)+","+str(contenedor)+","+str(pos_en_matriz)+")")
                return tuple([coste_acumulado_local + heuristica(self), sucesor])
        elif pos_barco == 1 and contenedor in self.lista_p_1 and dic_valores[contenedor][1] != 'R' and contenedor not in self.diccionario_pos_id.values() and dic_valores[contenedor][0] == '2':
            profundidad, valid = self.colocar_en_matriz(pos_en_matriz)
            if valid:
                dic_local = self.diccionario_pos_id.copy()
                dic_local[pos_en_matriz] = contenedor
                lista_p_1_local = list(self.lista_p_1)
                lista_p_1_local.remove(contenedor)
                coste_acumulado_local = self.coste_acumulado
                coste_acumulado_local += (10 + profundidad)
                sucesor = Nodo(pos_barco, dic_local, self.lista_p_init, lista_p_1_local, self.lista_p_2, coste_acumulado_local, self, "cargar(" + str(pos_barco) + "," + str(contenedor) + "," + str(pos_en_matriz) + ")")
                return tuple([coste_acumulado_local + heuristica(self), sucesor])

    def _cargar_refrigerado(self, pos_barco, contenedor, pos_en_matriz):
        if pos_barco == 0 and contenedor in self.lista_p_init and dic_valores[contenedor][1] == 'R' and contenedor not in self.diccionario_pos_id.values():
            profundidad, valid = self.colocar_en_matriz_refrig(pos_en_matriz)
            if valid:
                #print('aaaaa')
                dic_local = self.diccionario_pos_id.copy()
                dic_local[pos_en_matriz] = contenedor
                #print(str(dic_local)+' en '+ str(pos_barco))
                #print(dic_local[pos_en_matriz])
                lista_p_init_local = list(self.lista_p_init)
                #print(contenedor in lista_p_init_local)
                lista_p_init_local.remove(contenedor)
                #print(lista_p_init_local)
                #print(contenedor in lista_p_init_local)
                coste_acumulado_local = self.coste_acumulado
                coste_acumulado_local += (10 + profundidad)
                sucesor = Nodo(pos_barco, dic_local, lista_p_init_local, self.lista_p_1, self.lista_p_2, coste_acumulado_local, self, "cargar_refrigerado("+str(pos_barco)+","+str(contenedor)+","+str(pos_en_matriz)+")")
                return tuple([coste_acumulado_local + heuristica(self), sucesor])
        elif pos_barco == 1 and contenedor in self.lista_p_1 and dic_valores[contenedor][1] == 'R' and contenedor not in self.diccionario_pos_id.values() and dic_valores[contenedor][0] == '2':
            profundidad, valid = self.colocar_en_matriz_refrig(pos_en_matriz)
            if valid:
                dic_local = self.diccionario_pos_id.copy()
                dic_local[pos_en_matriz] = contenedor
                lista_p_1_local = list(self.lista_p_1)
                lista_p_1_local.remove(contenedor)
                coste_acumulado_local = self.coste_acumulado
                coste_acumulado_local += (10 + profundidad)
                sucesor = Nodo(pos_barco, dic_local, self.lista_p_init, lista_p_1_local, self.lista_p_2, coste_acumulado_local, self, "cargar_refrigerado(" + str(pos_barco) + "," + str(contenedor) + "," + str(pos_en_matriz) + ")")
                return tuple([coste_acumulado_local + heuristica(self), sucesor])

    def colocar_en_matriz(self, pos_en_matriz):
        if ((pos_en_matriz) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz] != '') or ((pos_en_matriz + N) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz + N] == ''):
            return None, False
        return pos_en_matriz // N, True

    def colocar_en_matriz_refrig(self, pos_en_matriz):
        if matriz_celdas[pos_en_matriz // N][pos_en_matriz % N] != 'E' or ((pos_en_matriz) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz] != '') or ((pos_en_matriz + N) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz + N] == ''):
            return None, False
        return pos_en_matriz // N, True

    def _descargar(self, pos_barco, contenedor, pos_en_matriz):
        """if pos_barco == 0 and contenedor in self.diccionario_pos_id.values() and (pos_en_matriz // N == 0 or ((pos_en_matriz - N) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz - N] == '')) and contenedor not in self.lista_p_init:
            dic_local = self.diccionario_pos_id
            for i in dic_local.keys():
                if dic_local[i] == contenedor:
                    dic_local[i] = ''
            #dic_local[pos_en_matriz] = ''
            lista_p_init_local = list(self.lista_p_init)
            lista_p_init_local.append(contenedor)
            coste_acumulado_local = self.coste_acumulado
            coste_acumulado_local += (15 + 2*(pos_en_matriz // N))
            sucesor = Nodo(pos_barco, dic_local, lista_p_init_local, self.lista_p_1, self.lista_p_2, coste_acumulado_local, self, "descargar(" + str(pos_barco) + "," + str(contenedor) + "," + str(pos_en_matriz) + ")")
            return tuple([coste_acumulado_local + heuristica(self), sucesor])"""
        #print(pos_barco == 1 and contenedor in list(self.diccionario_pos_id.values()) and (pos_en_matriz // N == 0 or ((pos_en_matriz - N) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz - N] == '')) and contenedor not in self.lista_p_1)
        #print(str(contenedor not in self.lista_p_1) +" "+str(contenedor))
        #print(self.lista_p_1)
        if pos_barco == 1 and self.diccionario_pos_id[pos_en_matriz] == contenedor and contenedor in list(self.diccionario_pos_id.values()) and (pos_en_matriz // N == 0 or ((pos_en_matriz - N) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz - N] == '')) and contenedor not in self.lista_p_1:
            dic_local = self.diccionario_pos_id.copy()
            #print(str(dic_local)+' en '+str(pos_barco))
            for i in dic_local.keys():
                if dic_local[i] == contenedor:
                    dic_local[i] = ''
            #print(dic_local)
            # dic_local[pos_en_matriz] = ''
            lista_p_1_local = list(self.lista_p_1)
            #print(contenedor in lista_p_1_local)
            lista_p_1_local.append(contenedor)
            #print(contenedor in lista_p_1_local)
            coste_acumulado_local = self.coste_acumulado
            coste_acumulado_local += (15 + 2 * (pos_en_matriz // N))
            sucesor = Nodo(pos_barco, dic_local, self.lista_p_init, lista_p_1_local, self.lista_p_2, coste_acumulado_local, self, "descargar(" + str(pos_barco) + "," + str(contenedor) + "," + str(pos_en_matriz) + ")")
            return tuple([coste_acumulado_local + heuristica(self), sucesor])
        elif pos_barco == 2 and self.diccionario_pos_id[pos_en_matriz] == contenedor and contenedor in self.diccionario_pos_id.values() and (pos_en_matriz // N == 0 or ((pos_en_matriz - N) in list(self.diccionario_pos_id.keys()) and self.diccionario_pos_id[pos_en_matriz - N] == '')) and contenedor not in self.lista_p_2:
            dic_local = self.diccionario_pos_id.copy()
            for i in dic_local.keys():
                if dic_local[i] == contenedor:
                    #posicion = i
                    dic_local[i] = ''
            # dic_local[pos_en_matriz] = ''
            lista_p_2_local = list(self.lista_p_2)
            lista_p_2_local.append(contenedor)
            coste_acumulado_local = self.coste_acumulado
            coste_acumulado_local += (15 + 2 * (pos_en_matriz // N))
            sucesor = Nodo(pos_barco, dic_local, self.lista_p_init, self.lista_p_1, lista_p_2_local, coste_acumulado_local, self, "descargar(" + str(pos_barco) + "," + str(contenedor) + "," + str(pos_en_matriz) + ")")
            return tuple([coste_acumulado_local + heuristica(self), sucesor])

    def _navegar(self, pos_barco):
        if pos_barco == 1:
            for contenedor in self.diccionario_pos_id.values():
                if contenedor != '' and dic_valores[contenedor][0] == '1':
                    return None
            #print(self.lista_p_init)
            #print(self.lista_p_1)
            #print(self.lista_p_2)
            coste_acumulado_local = self.coste_acumulado
            coste_acumulado_local += 3500
            #print('navegando desde '+ str(pos_barco))
            sucesor = Nodo(pos_barco+1, self.diccionario_pos_id.copy(), self.lista_p_init, self.lista_p_1, self.lista_p_2, coste_acumulado_local, self, "navegar("+str(pos_barco)+")")
            return tuple([coste_acumulado_local + heuristica(self), sucesor])
        elif pos_barco == 0:
            for contenedor in dic_valores.keys():
                if contenedor in self.lista_p_init:
                    return None
            coste_acumulado_local = self.coste_acumulado
            coste_acumulado_local += 3500
            #print('navegando desde ' + str(pos_barco))
            sucesor = Nodo(pos_barco + 1, self.diccionario_pos_id.copy(), self.lista_p_init, self.lista_p_1, self.lista_p_2,
                           coste_acumulado_local, self, "navegar(" + str(pos_barco) + ")")
            return tuple([coste_acumulado_local + heuristica(self), sucesor])

    def __lt__(self, other):
        if self.coste_acumulado < other.coste_acumulado:
            return self

    def __eq__(self, other):
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
    def __init__(self, tupla_nodo_init):
        self.abierta = queue.PriorityQueue()
        self.abierta.put(tupla_nodo_init)
        self.cerrada = []
        self.exito = False
        self.nodos_expandidos = 0

    def solve(self):
        while not self.abierta.empty() and not self.exito:
            primer_nodo_abierta = self.abierta.get()
            #print('a' +str(primer_nodo_abierta)+str(primer_nodo_abierta[1].diccionario_pos_id))
            while primer_nodo_abierta in self.cerrada:
                primer_nodo_abierta = self.abierta.get()

            if is_final(primer_nodo_abierta[1]):
                self.exito = True
            else:
                self.cerrada.append(primer_nodo_abierta)
                successors = primer_nodo_abierta[1].get_sucesores()
                #print(successors)
                #print(primer_nodo_abierta[1].lista_p_init)
                self.nodos_expandidos += 1
                #print(self.nodos_expandidos)
                for s in successors:
                    self.abierta.put(s)

        solucion = []
        if self.exito:
            nodo = primer_nodo_abierta[1]
            while nodo.parent is not None:
                solucion.append(nodo.accion)
                #print(nodo.diccionario_pos_id)
                print(nodo.coste_acumulado)
                nodo = nodo.parent

        return solucion, self.nodos_expandidos, primer_nodo_abierta[1].coste_acumulado


def heuristica(nodo):
    if HEURISTICA == 'heuristica1':
        return len(dic_valores.keys()) - (len(nodo.lista_p_1) + len(nodo.lista_p_2))


def is_final(nodo):
    if (nodo.pos_barco == 0) or len(nodo.lista_p_init) > 0:
        #print(nodo.lista_p_init)
        return False
    for i in nodo.diccionario_pos_id.values():
        if i != '':
            #print('b')
            return False
    for contenedor in dic_valores.keys():
        if (dic_valores[contenedor][0] == '1' and contenedor not in nodo.lista_p_1) or (dic_valores[contenedor][0] == '2' and contenedor not in nodo.lista_p_2):
            #print('c')
            return False
    #print(nodo.lista_p_1)
    #print(nodo.lista_p_2)
    return True


abierta = []
cerrada = []
exito = False

PATH = sys.argv[1] + "/"
MAPA = PATH + sys.argv[2]
CONTENEDORES = PATH + sys.argv[3]
HEURISTICA = sys.argv[4]
dominio1 = []
dominio2 = []
matriz_celdas = []
i = 0
counter_i = 0
counter_j = 0
M = 0
N = 0
try:
    with open(MAPA, "r+", encoding='utf-8', newline="") as file:
        for line in file:
            counter_j = 0
            for character in line:
                if character != ' ' and character != '\r' and character != '\n':
                    counter_j += 1
            if counter_j > N:
                N = counter_j
            counter_i += 1
        M = counter_i
except FileNotFoundError as ex:
    raise Exception("Wrong file or file path\n") from ex
print(M)
print(N)
counter = 0
try:
    with open(MAPA, "r+", encoding='utf-8', newline="") as file:
        for line in file:
            matriz_celdas.append([])
            prev_character = 'X'
            j = 0
            for character in line:
                if (prev_character == ' ' or character != ' ' or (j == 0 and character == ' ' [0] == character)) and character != '\r' and character != '\n':
                    if character == ' ':
                        matriz_celdas[i].append('X')
                    else:
                        matriz_celdas[i].append(character)
                    prev_character = 'X'
                    if character != 'X' and character != ' ':
                        dominio1.append(counter)
                        if character == 'E':
                            dominio2.append(counter)
                    counter += 1
                if character == ' ':
                    prev_character = ' '
                j += 1
            if len(matriz_celdas[i]) < N:
                matriz_celdas[i].append('X')
            i += 1
        print(dominio1)
        print(dominio2)
        print(matriz_celdas)

except FileNotFoundError as ex:
    raise Exception("Wrong file or file path\n") from ex

dic_valores = {}
try:
    with open(CONTENEDORES, "r+", encoding='utf-8', newline="") as file:
        for line in file:
            i = 0
            buf1 = ''
            while line[i] != ' ':
                buf1 += line[i]
                i += 1
            dic_valores[str(buf1)] = [str(line[i + 3]), str(line[i + 1])]
        print(dic_valores)
except FileNotFoundError as ex:
    raise Exception("Wrong file or file path\n") from ex

"""IDEA: matriz_celdas[(pos_en_matriz - N)//N][(pos_en_matriz - N)%N] == '-')"""

diccionario_pos_id = {}
for i in dominio1:
    diccionario_pos_id[i] = ''
nodo_init = Nodo(0, diccionario_pos_id, list(dic_valores.keys()), [], [], 0, None, "")
tupla_nodo_init = tuple([heuristica(nodo_init), nodo_init])

aestrella = Aestrella(tupla_nodo_init)
print(aestrella.solve())