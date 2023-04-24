import random

def cruce_ordenado(padre1, padre2):
    # Seleccionar dos puntos de cruce al azar
    punto_cruce_1 = random.randint(0, len(padre1)-1)
    punto_cruce_2 = random.randint(0, len(padre1)-1)

    # Asegurarse de que el primer punto de cruce sea menor que el segundo punto de cruce
    if punto_cruce_1 > punto_cruce_2:
        punto_cruce_1, punto_cruce_2 = punto_cruce_2, punto_cruce_1

    print("Punto de cruce 1: ", punto_cruce_1)
    print("Punto de cruce 2: ", punto_cruce_2)
    # Inicializar el hijo
    hijo = [None] * len(padre1)

    # Copiar los elementos de los padres entre los puntos de cruce, cruzados
    hijo[punto_cruce_1:punto_cruce_2+1] = padre1[punto_cruce_1:punto_cruce_2+1]

    # Buscar el valor correspondiente en el segundo padre a partir del punto de cruce 2
    valor_cruce_2 = padre1[punto_cruce_2]
    idx_valor_cruce_2 = padre2.index(valor_cruce_2)

    # Copiar los valores restantes en orden sin duplicados
    j = punto_cruce_2 + 1
    for i in range(idx_valor_cruce_2, len(padre2)):
        if j == len(hijo):
            j = 0
        if padre2[i] not in hijo:
            hijo[j] = padre2[i]
            j += 1
            if j == len(hijo):
                j = 0
    for i in range(0, idx_valor_cruce_2):
        if j == len(hijo):
            j = 0
        if padre2[i] not in hijo:
            hijo[j] = padre2[i]
            j += 1
            if j == len(hijo):
                j = 0

    return hijo



lis1 = [1,2,3,4,5,6,7,8,9,10]
lis2 = [10,9,8,7,6,5,4,3,2,1]
hijo = []

hijo = cruce_ordenado(lis1, lis2)
# nueva_generacion = []

# cut1 = random.randint(0, len(lis1) - 1)
# cut2 = random.randint(0, len(lis2) - 1)

# while True:
#     if cut1 == cut2:
#         cut1 = random.randint(0, len(lis1) - 1)
#         cut2 = random.randint(0, len(lis2) - 1)
#     else:
#         break

# if cut1 > cut2:
#     cut1, cut2 = cut2, cut1

# print(cut1+1, cut2+1)

# # Inicializar el hijo con la sección del padre 1
# hijo1 = [None]*len(lis1)
# hijo2 = [None]*len(lis2)
# hijo1[cut1:cut2+1] = lis2[cut1:cut2+1]
# hijo2[cut1:cut2+1] = lis1[cut1:cut2+1]

# for i in range(cut2, len(lis1)):
#     print("hijo: ", hijo1[i])
#     pos = lis1.index(hijo1[i])
#     if i+1 < len(lis1):
#         if lis1[pos+1] not in hijo1:
#             if pos+1 < len(lis1):
#                 hijo1[i+1] = lis1[pos+1]
#             else:
#                 hijo1[i+1] = lis1[pos+1-len(lis1)]
#         else:
#             k=0
#             while True:
#                 if lis1[pos+k] not in hijo1:
#                     pos = lis1.index(lis1[pos+1])
#                 else:
#                     hijo1[i+1] = lis1[pos+1]
#                     break
# # for i in range(cut2):
# #     pos = lis1.index(hijo1[i])
# #     if i+1 < len(lis1) and pos+1 < len(lis1):
# #         hijo1[i+1] = lis1[pos+1]

print(hijo)
