import sys


class Nodo:
    def __init__(self, pos_barco, diccionario_pos_id, lista_p_init, lista_p_1, lista_p_2):
        self.pos_barco = pos_barco
        self.diccionario_pos_id = diccionario_pos_id
        self.lista_p_init = lista_p_init
        self.lista_p_1 = lista_p_1
        self.lista_p_2 = lista_p_2
        self.successors = self.get_sucesores()

    def get_sucesores(self):
        sucesores = []
        for contenedor in dic_valores.keys():
            for pos in self.diccionario_pos_id.keys():
                sucesores.append(self._cargar(self.pos_barco, contenedor, pos))
                sucesores.append(self._cargar_refrigerado(self.pos_barco, contenedor, pos))
                sucesores.append(self._descargar(self.pos_barco, contenedor, pos))
        return sucesores

    def _cargar(self, pos_barco, contenedor, pos_en_matriz):
        if pos_barco == 0 and contenedor in self.lista_p_init and dic_valores[contenedor][1] != 'R':
            profundidad = self.colocar_en_matriz(contenedor, pos_en_matriz)
            dic_local = self.diccionario_pos_id
            dic_local[pos_en_matriz] = contenedor
            lista_p_init_local = self.lista_p_init
            lista_p_init_local.remove(contenedor)
            sucesor = Nodo(pos_barco, dic_local, lista_p_init_local, self.lista_p_1, self.lista_p_2)
            return((sucesor, 10+profundidad))
        elif pos_barco == 1 and contenedor in self.lista_p_1 and dic_valores[contenedor][1] != 'R':
            profundidad = self.colocar_en_matriz(contenedor, pos_en_matriz)
            dic_local = self.diccionario_pos_id
            dic_local[pos_en_matriz] = contenedor
            lista_p_1_local = self.lista_p_1
            lista_p_1_local.remove(contenedor)
            sucesor = Nodo(pos_barco, dic_local, self.lista_p_init, lista_p_1_local, self.lista_p_2)
            return((sucesor, 10+profundidad))

    def _cargar_refrigerado(self, pos_barco, contenedor, pos_en_matriz):
        if pos_barco == 0 and contenedor in self.lista_p_init and dic_valores[contenedor][1] == 'R':
            profundidad = self.colocar_en_matriz_refrig(contenedor, pos_en_matriz)
            dic_local = self.diccionario_pos_id
            dic_local[pos_en_matriz] = contenedor
            lista_p_init_local = self.lista_p_init
            lista_p_init_local.remove(contenedor)
            sucesor = Nodo(pos_barco, dic_local, lista_p_init_local, self.lista_p_1, self.lista_p_2)
            return((sucesor, 10+profundidad))
        elif pos_barco == 1 and contenedor in self.lista_p_1 and dic_valores[contenedor][1] == 'R':
            profundidad = self.colocar_en_matriz_refrig(contenedor, pos_en_matriz)
            dic_local = self.diccionario_pos_id
            dic_local[pos_en_matriz] = contenedor
            lista_p_1_local = self.lista_p_1
            lista_p_1_local.remove(contenedor)
            sucesor = Nodo(pos_barco, dic_local, self.lista_p_init, lista_p_1_local, self.lista_p_2)
            return((sucesor, 10+profundidad))

    def colocar_en_matriz(self, contenedor, pos_en_matriz):
        pass

    def colocar_en_matriz_refrig(self, contenedor, pos_en_matriz):
        pass


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

diccionario_pos_id = {}
for i in dominio1:
    diccionario_pos_id[i] = ''

nodo_init = Nodo(0, diccionario_pos_id, dic_valores.keys(), [], [])