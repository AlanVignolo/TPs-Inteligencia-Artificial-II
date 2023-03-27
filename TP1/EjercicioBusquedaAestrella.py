import matplotlib.pyplot as plt
from Grafico import Grafic

def heuristica (x,y,j,k):
    return (abs(x-j)**2+abs(y-k)**2)**0.5 * 100

def CalcObstaculos(Cantfilas,Cantcolumnas):

    Obstaculos = []
    vecfilas = []
    veccolumnas = []

    n=2
    for i in range(Cantfilas):
        vecfilas.append(n)
        vecfilas.append(n+1)
        vecfilas.append(n+2)
        vecfilas.append(n+3)
        n+=6

    n=2
    for i in range(Cantcolumnas):
        veccolumnas.append(n)
        veccolumnas.append(n+1)
        n+=4

    for j in veccolumnas:
        for i in vecfilas:
            Obstaculos.append((i-1,j-1))
    return Obstaculos

def Aestrella():

    Cantfilas = 8
    Cantcolumnas= 9

    nodofinal = [15,14]
    nodofinalp = nodofinal.copy()
    nodoinicial = [0,0]
    nodoactual = nodoinicial

    nodosabiertos = {}
    nodosvisitados = []

    Obstaculos= CalcObstaculos(Cantfilas,Cantcolumnas)

    if ((nodofinal[0],nodofinal[1])) in Obstaculos:
            nodofinal[1] += 1
            if ((nodofinal[0],nodofinal[1])) in Obstaculos:
                nodofinal[1] -= 2

    nodosabiertos[str(nodoactual[0])+","+str(nodoactual[1])] = heuristica(nodofinal[0],nodofinal[1],0,0)
    nodosvisitados.append(((nodoactual[0]),(nodoactual[1])))

    if ((nodofinalp[0],nodofinalp[1])) not in Obstaculos:
        print("El nodo final no es un estante")

    while True:

        iactual = int(nodoactual[0])
        jactual = int(nodoactual[1])


        for i in [-1,0,1]:
            for j in [-1,0,1]:
                iactual+i
                jactual+j
                if ((f"{str(iactual+i)},{str(jactual+j)}") not in nodosabiertos.keys()) and (((iactual+i),(jactual+j)) not in Obstaculos) and (((iactual+i),(jactual+j)) not in nodosvisitados) and (iactual+i >= 0) and (jactual+j >= 0) and (iactual+i <= Cantfilas*6) and (jactual+j <= Cantcolumnas*4) and i != j:
                    nodosabiertos[(f"{str(iactual+i)},{str(jactual+j)}")] = 100 + heuristica(nodofinal[0],nodofinal[1],iactual+i,jactual+j)

        del nodosabiertos[str(nodoactual[0])+","+str(nodoactual[1])]
        nodosabiertos = dict(sorted(nodosabiertos.items(), key=lambda item: item[1]))
        nodoactual = [int(x) for x in ((list(nodosabiertos.keys())[0]).split(","))]
        nodosvisitados.append(((nodoactual[0]),(nodoactual[1])))


        if nodoactual == nodofinal:
            break
    Graf=Grafic(Cantfilas*6,Cantcolumnas*4,Obstaculos,nodosvisitados,nodofinalp)
    Graf.dibujar_grafico()

Aestrella()