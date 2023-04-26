from TempleSimulado import Temple
import multiprocessing as mp
import time
import numpy as np
import random

class Genetico:
    # Constructor
    def __init__(self):
        self.poblacion = np.zeros((16, 120))
        self.filas = 3
        self.columnas = 5
        self.inicio = 1
        self.fin = 1
        self.seleccionados = np.zeros((4, 120))
        self.costo_sel = []

    # Funcion que inicializa la poblacion aleatoria
    def PoblacionAleatoria(self):
        for i in range(0 , len(self.poblacion)):
            self.poblacion[i] = random.sample(range(1, 121), 120)

    # Funcion que calcula el costo de cada individuo
    def calculo(self, orden, poblacion, costo_i):
        # Para cada individuo se calcula el costo total que tendran 10 ordenes
        costos = []
        for i in range(0, len(poblacion)):
            auxiliar = []
            costo_total = 0
            for k in range(0, len(orden)):
                aux = poblacion[i].tolist()
                for l in range(0, len(orden[k])):
                    auxiliar.append(aux.index(orden[k][l])+1)

                Orden = Temple(self.filas, self.columnas, self.inicio, self.fin, auxiliar)
                Templef = Orden.TempleSimulado()
                costo_total += Orden.Tamaño(Templef)
                auxiliar.clear()
            costos.append(costo_total)
        costo_i.put(costos)
        
    def seleccion(self, costos):    
        # Seleccion de los mejores individuos
        aux1 = []
        aux1 = sorted(costos, reverse=False) # Tiene que ser al revez
        for i in range(0, len(self.seleccionados)):
            pos = costos.index(aux1[i])
            self.seleccionados[i] = self.poblacion[pos]
        self.costo_sel.clear()
        self.costo_sel = aux1[0:4]
        return aux1
    
    # Funcion que realiza el coss-over
    def cruce(self):
        nueva_generacion = np.zeros((16, 120))
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
        for k in range(0, 12, 2):
            cut1 = random.randint(0, len(nueva_generacion[k]) - 1)
            cut2 = random.randint(0, len(nueva_generacion[k+1]) - 1)

            if cut1 > cut2:
                cut1, cut2 = cut2, cut1

            # Inicializar el hijo con la sección del padre 1
            hijo1 = [None]*len(nueva_generacion[k])
            hijo2 = [None]*len(nueva_generacion[k+1])
            hijo1[cut1:cut2+1] = nueva_generacion[k+1][cut1:cut2+1]
            hijo2[cut1:cut2+1] = nueva_generacion[k][cut1:cut2+1]

            # Buscar el valor correspondiente en el segundo padre a partir del punto de cruce 2
            idx_2 = nueva_generacion[k+1].tolist().index(nueva_generacion[k][cut2])
            idx_1 = nueva_generacion[k].tolist().index(nueva_generacion[k+1][cut2])

            # Cruce de Orden
            j = cut2 + 1
            for i in range(idx_2, len(nueva_generacion[k+1])):
                if j == len(hijo2):
                    j = 0
                if nueva_generacion[k+1][i] not in hijo2:
                    hijo2[j] = nueva_generacion[k+1][i]
                    j += 1
                    if j == len(hijo2):
                        j = 0
            l = cut2 + 1
            for i in range(idx_1, len(nueva_generacion[k])):
                if l == len(hijo1):
                    l = 0
                if nueva_generacion[k][i] not in hijo1:
                    hijo1[l] = nueva_generacion[k][i]
                    l += 1
                    if l == len(hijo1):
                        l = 0

            for i in range(0, idx_2):
                if j == len(hijo2):
                    j = 0
                if nueva_generacion[k+1][i] not in hijo2:
                    hijo2[j] = nueva_generacion[k+1][i]
                    j += 1
                    if j == len(hijo2):
                        j = 0

            for i in range(0, idx_1):
                if l == len(hijo1):
                    l = 0
                if nueva_generacion[k][i] not in hijo1:
                    hijo1[l] = nueva_generacion[k][i]
                    l += 1
                    if l == len(hijo1):
                        l = 0
            # MuTACION
            while True:
                cut1 = random.randint(0, len(nueva_generacion[k]) - 1)
                cut2 = random.randint(0, len(nueva_generacion[k+1]) - 1)
                if cut1 != cut2:
                    break
            hijo1[cut1], hijo1[cut2] = hijo1[cut2], hijo1[cut1]

            nueva_generacion[k] = hijo1
            nueva_generacion[k+1] = hijo2

        nueva_generacion[0] = self.seleccionados[0]
        nueva_generacion[1] = self.seleccionados[1]
        nueva_generacion[2] = self.seleccionados[2]
        nueva_generacion[3] = self.seleccionados[3]
        self.poblacion = nueva_generacion.copy()

if __name__ == "__main__":
    start_time = time.time()

    order_1 = [22, 24, 25, 27, 29, 31, 33, 46, 47, 54, 55, 58, 62, 63, 65, 66, 70, 72, 73, 74, 80, 87, 95, 97, 98]
    order_2 = [12, 20, 24, 25, 27, 29, 33, 35, 37, 38, 42, 54, 55, 60, 70, 76, 77, 78, 97, 99]
    order_3 = [21, 23, 24, 25, 39, 40, 44, 50, 51, 59, 63, 64, 67, 69, 74, 75, 80, 81, 85, 90, 93, 95, 96, 98]
    order_4 = [1, 8, 17, 20, 25, 30, 31, 36, 37, 41, 45, 50, 51, 52, 54, 56, 60, 64, 65, 73, 80, 87, 90, 92, 93, 96, 97, 98]
    order_5 = [20, 21, 25, 29, 36, 50, 60, 65, 72, 73, 74, 76, 79, 84, 87, 90, 92, 93, 95, 99]
    order_6 = [3, 20, 30, 32, 33, 38, 47, 48, 57, 58, 61, 63, 66, 72, 76, 79, 80, 86, 89, 94, 95]
    order_7 = [8, 21, 39, 42, 48, 50, 52, 60, 63, 69, 72, 76, 77, 79, 81, 82, 83, 85, 88, 91, 94, 97, 98]
    order_8 = [5, 15, 20, 23, 24, 39, 41, 42, 55, 66, 67, 72, 75, 79, 81, 84, 90, 91, 92, 93, 95, 96, 97, 98]
    order_9 = [13, 23, 32, 44, 50, 51, 58, 75, 78, 91, 92, 94, 95, 99]
    order_10 = [20, 25, 33, 35, 41, 43, 47, 49, 52, 53, 60, 64, 76, 79, 84, 90, 94, 95, 97, 99]
    ordenes = [order_1, order_2, order_3, order_4, order_5, order_6, order_7, order_8, order_9, order_10]

    k = 0
    g = Genetico()
    g.PoblacionAleatoria()

    costo_a = mp.Queue()
    costo_b = mp.Queue()
    costo_c = mp.Queue()
    costo_d = mp.Queue()
    costo_e = mp.Queue()
    costo_f = mp.Queue()
    costo_g = mp.Queue()
    costo_h = mp.Queue()

    poblaciones = [g.poblacion[i:i+2].copy() for i in range(0, 16, 2)]

    procesos = []
    for poblacion, costo in zip(poblaciones, [costo_a, costo_b, costo_c, costo_d, costo_e, costo_f, costo_g, costo_h]):
        procesos.append(mp.Process(target=g.calculo, args=(ordenes, poblacion, costo)))

    for proceso in procesos:
        proceso.start()

    for proceso in procesos:
        proceso.join()

    costo_t = []
    costo_t = costo_a.get() + costo_b.get() + costo_c.get() + costo_d.get() + costo_e.get() + costo_f.get() + costo_g.get() + costo_h.get()
    costo = g.seleccion(costo_t)  # Devuelve la lista de costos ordenada y carga como parametro los mejores 4 individuos

    for proceso in procesos:
        proceso.close()
    
    print(f"Poblacion inicial:\t\tCosto: {costo[0]}")
    g.cruce()  

    while 10>k:
        k += 1

        poblaciones = [g.poblacion[i:i+2].copy() for i in range(4, 16, 2)]

        procesos = []
        for poblacion, costo in zip(poblaciones, [costo_a, costo_b, costo_c, costo_d, costo_e, costo_f]):
            procesos.append(mp.Process(target=g.calculo, args=(ordenes, poblacion, costo)))

        for proceso in procesos:
            proceso.start()

        for proceso in procesos:
            proceso.join()

        costo_t = []
        costo_m = []
        costo_m = costo_a.get() + costo_b.get() + costo_c.get() + costo_d.get() + costo_e.get() + costo_f.get()
        costo_t = g.costo_sel + costo_m
        print(costo_t)
        costo = g.seleccion(costo_t)

        for proceso in procesos:
            proceso.close()
        
        print(f"Generacion: {k}\t\t\tCosto: {costo[0]}")
        g.cruce()       

    # g.calculo(ordenes, g.poblacion, costo_a)
    # costo_t.clear()
    # costo_t = costo_a.get()
    # costo_t[:4] = g.costo_sel
    # costo = g.seleccion(costo_t)
    # print("Generacion: ", k)
    print("Mejor solucion: ", g.seleccionados[0])
    # print("Costo: ", costo[0])
    
    end_time = time.time()   
    print("Tiempo total de ejecución: ", end_time - start_time)
