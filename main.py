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
def uno_encima_de_otro():
    for var1 in range(1, len(dic_valores.keys())+1):
        counter_var = 0
        for var2 in range(1, len(dic_valores.keys()) + 1):
            if var1 != var2:
                for i in range(0, len(matriz_celdas)):
                    for j in range(0, len(matriz_celdas[0])):
                        # añadir lo de and var1 not sobre suelo en el if
                        if dic_valores.keys()[str(var1)] == i + j and dic_valores.keys()[str(var2)] != i + j + len(dic_valores.keys()):
                            counter_var += 1
        if counter_var == len(dic_valores.keys())-1:
            return False
    return True






