from constraint import *
import sys
import os
from pathlib import Path

PATH = sys.argv[1] + "/"
MAPA = PATH + sys.argv[2]
CONTENEDORES = PATH + sys.argv[3]
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

problem = Problem()

#si hay una X por medio del mapa no se pueden poner contenedores encima
for i in range(0, M-1):
    for j in range(0, N):
        if matriz_celdas[i][j] == 'X' and matriz_celdas[i+1][j] != 'X':
            k = (i-1) * N + j
            matriz_celdas[i][j] = '-'
            while k >= 0:
                print(k)
                dominio1.remove(k)
                if k in dominio2:
                    dominio2.remove(k)
                k -= N
print(dominio1)
print(dominio2)
print(matriz_celdas)

#contendores refrigerados a celdas de energia
for var in dic_valores.keys():
    if dic_valores[var][1] == 'R':
        problem.addVariable(var, dominio2)
    else:
        problem.addVariable(var, dominio1)
#cada contenedor en una celda
problem.addConstraint(AllDifferentConstraint(), dic_valores.keys())

#almacenaje uno encima de otro
def uno_encima_de_otro(*args):
    var_list = []
    for elements in args:
        var_list.append(elements)
    #print('a' + str(len(var_list)))
    for var1 in range(0, len(var_list)):
        #print('b'+str(var_list[var1]))
        counter_var = 0
        for var2 in range(0, len(var_list)):
            if var1 != var2:
                for m in range(0, M-1):
                    for n in range(0, N):
                        if matriz_celdas[m+1][n] != 'X' and var_list[var1] == m*N + n and var_list[var2] != m*N + n + N:
                            #print('esta no esta debajo')
                            counter_var += 1
        #print('a'+str(counter_var))
        if counter_var == len(var_list)-1:
            print(False)
            return False
    print(True)
    return True
problem.addConstraint(uno_encima_de_otro, dic_valores.keys())

def puerto1_arriba(*args):
    var_list = []
    for elements in args:
        var_list.append(elements)
    keys = list(dic_valores.keys())
    #print(len(var_list))
    #print(var_list)
    for var1 in range(0, len(var_list)):
        #print('u' + keys[var1])
        for var2 in range(0, len(var_list)):
            #print('uu' + keys[var2])
            if var1 != var2:
                #print('var1: ' + str(var1) + ' var2: ' + str(var2) + ' var3: ' + str(var3))
                for o in range(0, M):
                    for p in range(0, N):
                        #print('b'+ str(dic_valores[keys[var1]][0]))
                        if ((var_list[var1] == o*N + p) and dic_valores[keys[var1]][0] == '2') and ((var_list[var2] == o*N + p + N) and dic_valores[keys[var2]][0] != '2'):
                            print('False2')
                            return False
    print('True2')
    return True
problem.addConstraint(puerto1_arriba, dic_valores.keys())

def todas_asignadas(*args):
    counter_vars = 0
    for value in dominio1:
        if value in list(args):
            counter_vars += 1
    if counter_vars == len(dic_valores.keys()):
        print('True3')
        return True
    print('False3')
    return False
    #if all(variable in list(args) for variable in dominio1):
    #    print('True3')
    #    return True
    #print('False3')
    #return False

problem.addConstraint(todas_asignadas, dic_valores.keys())

list_solutions = problem.getSolutions()
print(list_solutions)
print(dic_valores)
print(matriz_celdas)
print(dominio1)
print(dominio2)
matriz_posiciones = []
for i in range(0, M):
    matriz_posiciones.append([])
    for j in range(0, N):
        matriz_posiciones[i].append(i*N + j)

try:
    with open(PATH + sys.argv[2] +"-"+sys.argv[3]+".output", "w+", encoding='utf-8', newline="") as file:
        file.write("Número de soluciones: " + str(len(list_solutions)) + "\n")
        for times in range(0, len(list_solutions)):
            dic_solution = {}
            for var in list_solutions[times].keys():
                for i in range(0, M):
                    for j in range(0, N):
                        if list_solutions[times][var] == matriz_posiciones[i][j]:
                            dic_solution[var] = (j, i)
            print(str(dic_solution))
            file.write(str(dic_solution) + "\n")
except FileNotFoundError as ex:
    raise Exception("Wrong file or file path\n") from ex
file.close()
