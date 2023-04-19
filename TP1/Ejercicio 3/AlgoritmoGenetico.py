from TempleSimulado import Temple
import time

start_time = time.time()
def main():

    filas = 4
    columnas = 4
    inicio = 1
    fin = 1
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

    for i in range (10):
        Orden1 = Temple(filas,columnas,inicio,fin,ordenes[i])
        Templef = Orden1.TempleSimulado()
        tamañof = Orden1.Tamaño(Templef)

    #Orden1.Graficarresultado(Templef)

if __name__ == "__main__":
    main()
    end_time = time.time()
    total_time = end_time - start_time
    print("Tiempo total de ejecución:", total_time, "segundos")




class Genetico:
    # Constructor
    def __init__(self, matriz):
        self.combinacion = comb.Combinacion(matriz)
        self.orden_original = [1,2,25,26,3,4,27,28,5,6,29,30,7,8,31,32,
                              9,10,33,34,11,12,35,36,13,14,37,38,15,16,39,40,
                              17,18,41,42,19,20,43,44,21,22,45,46,23,24,47,48]
        self.objetivos = [1, 48, 8, 40, 20] # Esto es el dato del problema
        self.estantes={1:12,2:15,3:22,4:25,5:32,6:35,7:42,8:45,
                        9:72,10:75,11:82,12:85,13:92,14:95,15:102,16:105,
                        17:132,18:135,19:142,20:145,21:152,22:155,23:162,24:165,
                        25:16,26:19,27:26,28:29,29:36,30:39,31:46,32:49,
                        33:76,34:79,35:86,36:89,37:96,38:99,39:106,40:109,
                        41:136,42:139,43:146,44:149,45:156,46:159,47:166,48:169}
        self.poblacion = np.zeros((20, 48))

    # Funcion que inicializa la poblacion aleatoria
    def PoblacionAleatoria(self):
        for i in range(0 , len(self.poblacion)):
            for j in range(0, len(self.poblacion[i])):
                while True:
                    n = random.randint(1, len(self.poblacion[0]))
                    if n not in self.poblacion[i]:
                        self.poblacion[i,j] = n
                        break
       
    
    # Funcion que calcula el fitness de cada individuo
    def fitness(self):
        costo_total = 0
        lista = [] 
        lista_costos = []
        probabilidad = np.zeros(20)
        lista_lista = []
        lista_nodos = []
        print("flag 1")
        # En vez de cambiar las posiciones de la matriz hago una conversion de las nuevas a la original
        for i in range(0, len(self.poblacion)):
            # Este diccionario me ayuda a visualizar pero no tiene utilidad en el algoritmo
            # diccionario = {'p_original': [], 'p_nueva': [], 'objetivo': []} # Diccionario de largo 48
            for j in range(0, len(self.poblacion[i])):
                # diccionario['p_original'].append(self.orden_original[j])
                # diccionario['p_nueva'].append(self.poblacion[i,j])
                # diccionario['objetivo'].append(0)
                if self.poblacion[i,j] in self.objetivos:
                    # diccionario['objetivo'][j] = 1
                    lista.append(self.orden_original[j])    # Esta sera la lista transformada
            # Con los nodos definido lo mando al temple simulado
            print("flag 1.5")

            if len(lista) == 5:
                orden_nodos, camino, posiciones_visitadas, costo = self.combinacion.combinacion_optima(lista)
            else:
                print(self.poblacion[i])
                print("???????????????????????????")
                # cerrar el programa
                break
            print("flag 1.75")

            lista.clear()
            costo_total += costo
            lista_costos.append(costo)
            # lista_lista.append(lista)
            # lista_nodos.append(orden_nodos)
        print ("flag 2")
        for i in range(0, len(lista_costos)):
            probabilidad[i] = 1 - (lista_costos[i]/costo_total)

        lista_costos.clear()

        return probabilidad

    # Mutacion
    def mutacion(self, seleccionados, probabilidad):
        nueva_generacion = np.zeros((20, 48))
        k2 = 999
        k1 = 0
        print("flag 3")
        # Reordenamiento para la nueva generacion
        for i in range(0, len(nueva_generacion)):
            while True:
                k1 = random.randint(0, len(seleccionados)-1)
                #if probabilidad[k1] > random.random() and k1 != k2:
                if k1 != k2:
                    # Probabilidad de que sea aceptado y que no sea igual al anterior
                    # De esta forma la siguiente generacion no se repetira
                    nueva_generacion[i] = seleccionados[k1]
                    k2 = k1
                    break
        print("flag 4")
        # Cross over
        for j in range(0, 20, 2):   # 0, 2, 4, 6, 8, 10, 12, 14, 16, 18  
            # Posicion de corte
            while True:
                n = random.randint(0, len(seleccionados[0])) 
                if n != 0 and n != len(seleccionados[0]):   # Para que no se corte en la primera o ultima posicion
                    aux1 = nueva_generacion[j, n:]  # Guarda la parte de la derecha del corte]
                    aux2 = nueva_generacion[j+1, n:]    # Guarda la parte de la derecha del corte
                    aux3 = nueva_generacion[j, :n]  # Guarda la parte de la izquierda del corte
                    aux4 = nueva_generacion[j+1, :n]    # Guarda la parte de la izquierda del corte
                    nueva_generacion[j] = np.concatenate((aux3, aux2), axis=None) # Concatena la parte izquierda con la derecha
                    nueva_generacion[j+1] = np.concatenate((aux4, aux1), axis=None)   # Concatena la parte izquierda con la derecha                 
                    
                    break
        print("flag 5")
        self.poblacion = nueva_generacion
