from constraint import *
import sys

# Guardamos los argumentos en variables
PATH = sys.argv[1] + "/"
MAPA = PATH + sys.argv[2]
CONTENEDORES = PATH + sys.argv[3]

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
        # Iteramos por cada linea y cada caracter de cada linea
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

# Inicializamos el problema de python constraint
problem = Problem()

# Si hay una X por medio del mapa no se pueden poner contenedores encima
for i in range(0, M - 1):
    for j in range(0, N):
        # Si encontramos en el mapa una celda de 'X' que no corresponde al suelo la cambiamos en la matriz por '-'
        # para diferenciarla de las celdas de suelo
        if matriz_celdas[i][j] == 'X' and matriz_celdas[i + 1][j] != 'X':
            k = (i - 1) * N + j
            matriz_celdas[i][j] = '-'
            # Cada celda encima de esa celda invalida se quita de los dominios
            while k >= 0:
                dominio1.remove(k)
                if k in dominio2:
                    dominio2.remove(k)
                k -= N

# Asignamos las variables a sus dominios
# Los contendores refrigerados iran solo a celdas de energia (dominio2) y los normales a cualquiera (dominio1)
for var in dic_valores.keys():
    if dic_valores[var][1] == 'R':
        problem.addVariable(var, dominio2)
    else:
        problem.addVariable(var, dominio1)

# Incluimos la restriccion de que cada contenedor debera ir a una celda diferente
problem.addConstraint(AllDifferentConstraint(), dic_valores.keys())


# Almacenaje uno encima de otro
def uno_encima_de_otro(*args):
    # Creamos una lista con las variables
    var_list = []
    for elements in args:
        var_list.append(elements)
    # Para cada varable miramos si existe alguna variable de las demas que este debajo de ella o si está en el suelo
    # (tome como valor la posicion de abajo)
    for var1 in range(0, len(var_list)):
        counter_var = 0
        for var2 in range(0, len(var_list)):
            if var1 != var2:
                for m in range(0, M - 1):
                    for n in range(0, N):
                        # Las posiciones se calculando siguiendo la formula i*N+j, o en este caso: o*N+p
                        # Por tanto para clacular la posicion de debajo de o*N+p habra que sumarle N
                        if matriz_celdas[m+1][n] != 'X' and var_list[var1] == m*N + n and var_list[var2] != m*N + n + N:
                            # Un contador va incrementando por cada variable que no este debajo de ella
                            counter_var += 1
        # Si el contador es igual al numero total de variables menos 1, significa que no hay
        # ninguna variable debajo de ella y por tanto la restriccion no se satisface
        if counter_var == len(var_list) - 1:
            return False
    return True


# Incluimos la restriccion de almacenaje de que un contenedor deba tener otro debajo o estar sobre suelo
problem.addConstraint(uno_encima_de_otro, dic_valores.keys())


# Un contenedor que vaya al puerto 2 no podra colocarse sobre uno que vaya al puerto 1
def puerto1_arriba(*args):
    # Creamos una lista con las variables
    var_list = []
    for elements in args:
        var_list.append(elements)
    # Para cada par de contenedores distintos miramos si uno va al puerto 2 y si el otro esta debajo y va al puerto 1
    keys = list(dic_valores.keys())
    for var1 in range(0, len(var_list)):
        for var2 in range(0, len(var_list)):
            if var1 != var2:
                for o in range(0, M):
                    for p in range(0, N):
                        # Las posiciones se calculando siguiendo la formula i*N+j, o en este caso: o*N+p
                        # Por tanto para clacular la posicion de debajo de o*N+p habra que sumarle N
                        if ((var_list[var1] == o*N + p) and dic_valores[keys[var1]][0] == '2') and ((var_list[var2] == o*N + p + N) and dic_valores[keys[var2]][0] != '2'):
                            return False
    return True


# Incluimos la restriccion de que, para que no hay recolocaciones, los contenedores que vayan al puerto 2 no pueden
# tener contenedores que vayan al puerto 1 debajo
problem.addConstraint(puerto1_arriba, dic_valores.keys())


# Asignar todos los contenedores a alguna celda
def todas_asignadas(*args):
    counter_vars = 0
    for value in dominio1:
        if value in list(args):
            counter_vars += 1
    # Si el numero de variables asignadas es igual al numero de variables entonces se cumple la restriccion
    if counter_vars == len(dic_valores.keys()):
        return True
    return False


# Incluimos la restriccion de que todos los contenedores han de ser asignados a una celda
problem.addConstraint(todas_asignadas, dic_valores.keys())

# Guardamos la lista de todas las soluciones en una variable
list_solutions = problem.getSolutions()

# Para poder traducir las posiciones numericas a tuplas (pila, profundidad) creamos una matriz de posiciones numericas
# Estas posiciones siguen la formula i*N+j
matriz_posiciones = []
for i in range(0, M):
    matriz_posiciones.append([])
    for j in range(0, N):
        matriz_posiciones[i].append(i * N + j)

try:
    # Abrimos o creamos un archivo de salida donde incluiremos las soluciones del problema
    with open(PATH + sys.argv[2] + "-" + sys.argv[3] + ".output", "w+", encoding='utf-8', newline="") as file:
        # En la primera linea del archivo escribimos el numero total de soluciones
        file.write("Número de soluciones: " + str(len(list_solutions)) + "\n")
        # Para cada solucion formamos un diccionario con las soluciones de tal forma que para cada id de contenedor
        # quede asociado una tupla con su posicion en la matriz de la forma (pila, profundidad).
        # Para hacer esto comparamos los valores de posiciones numericas de la solucion con los valores de i y j en la
        # matriz de posiciones numericas creada antes
        for times in range(0, len(list_solutions)):
            dic_solution = {}
            for var in list_solutions[times].keys():
                for i in range(0, M):
                    for j in range(0, N):
                        if list_solutions[times][var] == matriz_posiciones[i][j]:
                            dic_solution[var] = (j, i)
            # Se escribe el diccionario de la solucion con la forma (pila, profundidad) para cada id de contenedor
            file.write(str(dic_solution) + "\n")
except FileNotFoundError as ex:
    # En caso de no poder abrir el archivo del mapa saltará una excepcion
    raise Exception("Wrong file or file path\n") from ex
# Cerramos el archivo
file.close()
