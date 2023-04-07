from TempleSimulado import Orden

def main():

    filas = 4
    columnas = 4
    inicio = 1
    fin = 1
    estantes = [6,20,39,67,4,15]

    Orden1 = Orden(filas,columnas,inicio,fin,estantes)
    Templef = Orden1.TempleSimulado()
    tamañof = Orden1.Tamaño(Templef)

    print (Templef)
    print (tamañof)
    Orden1.Graficarresultado(Templef)

if __name__ == "__main__":
    main()