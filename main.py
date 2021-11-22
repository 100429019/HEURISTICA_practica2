from constraint import *
import sys
import os
from pathlib import Path

PATH = str(Path.home()) + "/" + sys.argv[1] + "/"
MAPA = PATH + sys.argv[2]
CONTENEDORES = PATH + sys.argv[3]
dominio1 = []
dominio2 = []
matriz_celdas = []
i = 0
counter = 0
try:
    with open(MAPA, "r+", encoding='utf-8', newline="") as file:
        for line in file:
            matriz_celdas.append([])
            for character in line:
                if character != ' ' and character != '\r' and character != '\n':
                    matriz_celdas[i].append(character)
                    if character != 'X':
                        dominio1.append(counter)
                        if character == 'E':
                            dominio2.append(counter)
                    counter += 1
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
for i in range(0, len(matriz_celdas)-1):
    for j in range(0, len(matriz_celdas[0])):
        if matriz_celdas[i][j] == 'X' and matriz_celdas[i+1][j] != 'X':
            k = (i-1) * len(matriz_celdas[0]) + j
            matriz_celdas[i][j] = '-'
            while k <= 0:
                print(k)
                dominio1.remove(k)
                if k in dominio2:
                    dominio2.remove(k)
                k -= len(matriz_celdas[0])
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
    var_list = [args]
    for var1 in range(1, len(var_list)+1):
        counter_var = 0
        for var2 in range(1, len(var_list) + 1):
            if var1 != var2:
                for m in range(0, len(matriz_celdas)-1):
                    for n in range(0, len(matriz_celdas[0])):
                        if matriz_celdas[i+1][j] != 'X' and var_list[var1] == i + j and var_list[var2] != i + j + len(var_list):
                            counter_var += 1
        if counter_var == len(var_list)-1:
            return False
    return True
problem.addConstraint(uno_encima_de_otro, dic_valores.keys())

def puerto1_arriba(*args):
    var_list = [args]
    for var1 in range(1, len(var_list)+1):
        for var2 in range(1, len(var_list) + 1):
            for var3 in range(1, len(var_list) + 1):
                if var1 != var2 and var1 != var3 and var2 != var3:
                    for o in range(0, len(matriz_celdas)):
                        for p in range(0, len(matriz_celdas[0])):
                            if ((var_list[var1] == i + j and dic_valores[var_list[var1]][0] == 1) and (var_list[var2] != i + j + len(var_list) and dic_valores[var_list[var2]][0] == 2)) and (var_list[var3] != i + j + len(var_list) and dic_valores[var_list[var3]][0] != 2):
                                return False
    return True
problem.addConstraint(puerto1_arriba, dic_valores.keys())

def todas_asignadas(*args):
    return all(variable in list(args) for variable in dominio1)

problem.addConstraint(todas_asignadas, dic_valores.keys())

print(problem.getSolutions())



