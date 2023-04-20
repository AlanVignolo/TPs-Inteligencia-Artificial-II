from TempleSimulado import Temple
import time
import numpy as np
import random

class Genetico:
    # Constructor
    def __init__(self):
        self.poblacion = np.zeros((12, 120))
        self.filas = 3
        self.columnas = 5
        self.inicio = 1
        self.fin = 1
        self.seleccionados = np.zeros((6, 120))

    # Funcion que inicializa la poblacion aleatoria
    def PoblacionAleatoria(self):
        for i in range(0 , len(self.poblacion)):
            self.poblacion[i] = random.sample(range(1, 121), 120)
    
    # Funcion que selecciona los individuos para la siguiente generacion
    def seleccion(self, ordenes):
        # Para cada individuo se calcula el costo total que tendran 10 ordenes
        costos = []
        for i in range(0, len(self.poblacion)):
            costo_total = 0
            for i in range(0, len(ordenes)):
                Orden = Temple(self.filas, self.columnas, self.inicio, self.fin, ordenes[i])
                Templef = Orden.TempleSimulado()
                costo_total += Orden.Tamaño(Templef)
                costos.append(costo_total) 
        
        # Seleccion de los mejores individuos
        aux1 = sorted(costos, reverse=False) # Tiene que ser al revez
        for i in range(0, len(self.seleccionados)):
            pos = np.where(costos == aux1[i])[0][0]
            self.seleccionados[i] = self.poblacion[pos]
    
    # Funcion que realiza el coss-over
    def cruce(self):
        nueva_generacion = np.zeros((12, 120))
        k2 = 999
        k1 = 0
        # Reordenamiento para la nueva generacion
        for i in range(0, len(nueva_generacion)):
            while True:
                k1 = random.randint(0, len(self.seleccionados)-1)
                if k1 != k2:
                    # Que no sea igual al anterior
                    nueva_generacion[i] = self.seleccionados[k1]
                    k2 = k1
                    break

        # Cross over
        for i in range(0, 12, 2):
            cut1 = random.randint(0, len(nueva_generacion[i]) - 1)
            cut2 = random.randint(0, len(nueva_generacion[i+1]) - 1)

            if cut1 > cut2:
                cut1, cut2 = cut2, cut1

            # Inicializar el hijo con la sección del padre 1
            hijo1 = [None]*len(nueva_generacion[i])
            hijo2 = [None]*len(nueva_generacion[i+1])
            hijo1[cut1:cut2+1] = nueva_generacion[i][cut1:cut2+1]
            hijo2[cut1:cut2+1] = nueva_generacion[i+1][cut1:cut2+1]

            # Copiar los genes del padre 2 que no están en el hijo
            for j in range(len(nueva_generacion[i])):
                if nueva_generacion[i][j] not in hijo1:
                    idx = i
                    while hijo1[idx] is not None:
                        idx = nueva_generacion[i+1].index(nueva_generacion[i][idx])
                    hijo1[idx] = nueva_generacion[i+1][j]
                if nueva_generacion[i][j] not in hijo2:
                    idx = i
                    while hijo2[idx] is not None:
                        idx = nueva_generacion[i].index(nueva_generacion[i+1][idx])
                    hijo2[idx] = nueva_generacion[i][j]

            # Completar los genes restantes del hijo
            for j in range(len(hijo1)):
                if hijo1[i] is None:
                    hijo1[i] = nueva_generacion[i+1][nueva_generacion[i].index(nueva_generacion[i][j])]
                if hijo2[i] is None:
                    hijo2[i] = nueva_generacion[i][nueva_generacion[i+1].index(nueva_generacion[i][j])]
            
            # Mutacion
            while True:
                cut1 = random.randint(0, len(nueva_generacion[i]) - 1)
                cut2 = random.randint(0, len(nueva_generacion[i+1]) - 1)
                if cut1 == cut2:
                    break
            hijo1[cut1], hijo1[cut2] = hijo1[cut2], hijo1[cut1]
            
            nueva_generacion[i] = hijo1
            nueva_generacion[i+1] = hijo2


start_time = time.time()
def main():

    order_1 = [22, 24, 25, 27, 29, 31, 33, 46, 47, 54, 55, 58, 62, 63, 65, 66, 70, 72, 73, 74, 80, 87, 95, 97, 98]
    order_2 = [12, 20, 24, 25, 27, 29, 33, 35, 37, 38, 42, 54, 55, 60, 70, 76, 77, 78, 97, 99]
    order_3 = [21, 23, 24, 25, 39, 40, 44, 50, 51, 59, 63, 64, 67, 69, 74, 75, 80, 81, 85, 90, 93, 95, 96, 98]
    order_4 = [0, 8, 17, 20, 25, 30, 31, 36, 37, 41, 45, 50, 51, 52, 54, 56, 60, 64, 65, 73, 80, 87, 90, 92, 93, 96, 97, 98]
    order_5 = [20, 21, 25, 29, 36, 50, 60, 65, 72, 73, 74, 76, 79, 84, 87, 90, 92, 93, 95, 99]
    order_6 = [3, 20, 30, 32, 33, 38, 47, 48, 57, 58, 61, 63, 66, 72, 76, 79, 80, 86, 89, 94, 95]
    order_7 = [8, 21, 39, 42, 48, 50, 52, 60, 63, 69, 72, 76, 77, 79, 81, 82, 83, 85, 88, 91, 94, 97, 98]
    order_8 = [5, 15, 20, 23, 24, 39, 41, 42, 55, 66, 67, 72, 75, 79, 81, 84, 90, 91, 92, 93, 95, 96, 97, 98]
    order_9 = [13, 23, 32, 44, 50, 51, 58, 75, 78, 91, 92, 94, 95, 99]
    order_10 = [20, 25, 33, 35, 41, 43, 47, 49, 52, 53, 60, 64, 76, 79, 84, 90, 94, 95, 97, 99]
    ordenes = [order_1, order_2, order_3, order_4, order_5, order_6, order_7, order_8, order_9, order_10]

    # Necesito una funcion que me transforme las ordenes a las posiciones de la matriz del temple

    i = 0
    g = Genetico()
    g.PoblacionAleatoria()

    while 10>i:
        i += 1
        g.seleccion(ordenes)
        g.cruce()


if __name__ == "__main__":
    main()
    end_time = time.time()
    total_time = end_time - start_time
    print("Tiempo total de ejecución:", total_time, "segundos")
