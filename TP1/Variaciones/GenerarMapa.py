import Aestrella

def GenerarArchivo (filas,columnas):
    Aest= Aestrella.Aestrella(filas,columnas)

    archivo = open("Mapa.txt","w")

    for i in range ((filas*columnas*8)-1):
        for j in range (i+1,((filas*columnas*8)-1)):
            archivo.write(str(Aest.Obstaculos[i])+"/"+str(Aest.Obstaculos[j])+"-->"+str(Aest.calcularcamino(i+1,j+1)[0])+"\n")

    archivo.close()

def main():
    filas = 3
    columnas = 3
    GenerarArchivo(filas,columnas)

if __name__ == "__main__":
    main()