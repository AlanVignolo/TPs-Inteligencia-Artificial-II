import random

def pmx(parent1, parent2):
    # Seleccionar dos puntos de corte aleatorios
    cut1 = random.randint(0, len(parent1) - 1)
    cut2 = random.randint(0, len(parent1) - 1)

    if cut1 > cut2:
        cut1, cut2 = cut2, cut1

    print(cut1, cut2)

    # Inicializar el hijo con la sección del padre 1
    hijo1 = [None]*len(parent1)
    hijo2 = [None]*len(parent1)
    hijo1[cut1:cut2+1] = parent1[cut1:cut2+1]
    hijo2[cut1:cut2+1] = parent2[cut1:cut2+1]

    # Copiar los genes del padre 2 que no están en el hijo
    for i in range(len(parent2)):
        if parent2[i] not in hijo1:
            idx = i
            while hijo1[idx] is not None:
                idx = parent2.index(parent1[idx])
            hijo1[idx] = parent2[i]
        if parent1[i] not in hijo2:
            idx = i
            while hijo2[idx] is not None:
                idx = parent1.index(parent2[idx])
            hijo2[idx] = parent1[i]

    # Completar los genes restantes del hijo
    for i in range(len(hijo1)):
        if hijo1[i] is None:
            hijo1[i] = parent2[parent1.index(parent2[i])]
        if hijo2[i] is None:
            hijo2[i] = parent1[parent2.index(parent1[i])]
    return hijo1, hijo2

# definir las dimensiones de la matriz
filas = 2
columnas = 10

# crear una lista vacía para almacenar la matriz
matriz = []

# crear la matriz de ceros usando bucles for
for i in range(filas):
    # crear una lista de ceros para cada fila
    fila = []
    for j in range(columnas):
        # agregar un cero a la fila para cada columna
        fila.append(0)
    # agregar la fila a la matriz
    matriz.append(fila)

matriz[0] = random.sample(range(1, 11), 10)
matriz[1] = random.sample(range(1, 11), 10)
hijo1, hijo2 = pmx(matriz[0], matriz[1])
print(matriz)
print(hijo1, hijo2)
