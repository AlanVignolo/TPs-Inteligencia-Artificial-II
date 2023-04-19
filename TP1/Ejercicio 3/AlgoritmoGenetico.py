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