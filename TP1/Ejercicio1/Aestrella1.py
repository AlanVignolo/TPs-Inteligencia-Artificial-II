import matplotlib.pyplot as plt
from Grafico import Grafico
import copy
from math import dist

class Aestrella():
    def __init__(self,filas,columnas):

        # Cantidad de filas y columnas de estantes
        self.Cantfilas = filas
        self.Cantcolumnas = columnas
        self.Obstaculos= self.CalcObstaculos()

    def calcularcamino(self,inicio,final):

        nodoinicial = list(self.Obstaculos[inicio-1])
        nodofinal = list(self.Obstaculos[final-1])

        nodofinalp = nodofinal.copy()

        nodosabiertos = []
        nodosvisitados = []

        if ((nodofinalp[0],nodofinalp[1])) in self.Obstaculos:
            nodofinalp[1] += 1
            if ((nodofinalp[0],nodofinalp[1])) in self.Obstaculos:
                nodofinalp[1] -= 2

        if ((nodoinicial[0],nodoinicial[1])) in self.Obstaculos:
            nodoinicial[1] += 1
            if ((nodoinicial[0],nodoinicial[1])) in self.Obstaculos:
                nodoinicial[1] -= 2
        r=0
        nodoactual = nodoinicial
        nodosvisitados.append(((nodoinicial[0]),(nodoinicial[1]),r))

        if nodoactual == nodofinalp:
            return 0, [nodoinicial, nodofinalp], nodofinalp
        
        while True:

            if nodoactual == nodofinalp:
                break

            r+=1
            iactual = nodoactual[0]
            jactual = nodoactual[1]

            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    inuevo = iactual + i
                    jnuevo = jactual + j
                    if ((inuevo, jnuevo) not in [(sublst[0], sublst[1]) for sublst in nodosabiertos]) and ((inuevo, jnuevo) not in self.Obstaculos) and ((inuevo, jnuevo) not in [(sublst[0], sublst[1]) for sublst in nodosvisitados]) and (inuevo >= 0) and (jnuevo >= 0) and (inuevo <= self.Cantfilas * 6) and (jnuevo <= self.Cantcolumnas * 4) and abs(i) != abs(j):
                        f = self.heuristica(nodofinalp[0], nodofinalp[1], inuevo, jnuevo) + r
                        nodosabiertos.append((inuevo, jnuevo,f , r, (iactual, jactual)))
            nodosabiertos = sorted(nodosabiertos, key=lambda x: x[2])
            nodoactual[0],nodoactual[1], *_ = nodosabiertos[0]
            nodosvisitados.append(((nodosabiertos[0][0]),(nodosabiertos[0][1]),(nodosabiertos[0][3]),(nodosabiertos[0][4])))
            nodosabiertos.pop(0)            

        listafinal=[]
        while True:

            for i in range(len(nodosvisitados)-1):
                if len(nodosvisitados)==2:
                    listafinal.insert(0,(nodosvisitados[-1][0],nodosvisitados[-1][1]))
                    listafinal.insert(0,(nodosvisitados[0][0],nodosvisitados[0][1]))
                    print(listafinal)
                    return len(listafinal),listafinal,nodofinalp
                
                while nodosvisitados[-i-1][3] != (nodosvisitados[-i-2][0],nodosvisitados[-i-2][1]):
                    nodosvisitados.pop(-i-2)
                
                listafinal.insert(0,(nodosvisitados[-i-1][0],nodosvisitados[-i-1][1]))
                
                if i ==len(nodosvisitados)-2:
                    listafinal.insert(0,(nodosvisitados[0][0],nodosvisitados[0][1]))
                    print(listafinal)
                    return len(listafinal),listafinal,nodofinalp
        
    def dibujar(self,nodosvisitados,nodofinalp):    
        Grafico1=Grafico(self.Cantfilas*6,self.Cantcolumnas*4,self.Obstaculos)
        Grafico1.dibujar_grafico(nodosvisitados,nodofinalp)


    def GraficarCamino (self,lista,lista2=0):

        nodosvisitados = []
        finales = []

        for i in range(len(lista)-1):
            
            nodosvisitados.append((self.calcularcamino(lista[i],lista[i+1]))[1])

        Grafico2=Grafico(self.Cantfilas*6,self.Cantcolumnas*4,self.Obstaculos)

        for x in lista:
            finales.append(self.Obstaculos[x-1])

        if lista2==0:
            Grafico2.dibujar_grafico(nodosvisitados,finales)
        else:
            total_elements = 0
            for sublist in  nodosvisitados:
                total_elements += len(sublist)
            return total_elements
        

    def heuristica (self,x,y,j,k):
        return (abs(x-j)**2+abs(y-k)**2)**0.5 

    # Funcion que calcula los nodos donde se encuentran estantes
    def CalcObstaculos(self):

        Obstaculos = []
        vecfilas = []
        veccolumnas = []

        n=2
        for i in range(self.Cantfilas):
            vecfilas.append(n)
            vecfilas.append(n+1)
            vecfilas.append(n+2)
            vecfilas.append(n+3)
            n+=6

        n=2
        for i in range(self.Cantcolumnas):
            veccolumnas.append(n)
            veccolumnas.append(n+1)
            n+=4

        for j in veccolumnas:
            for i in vecfilas:
                Obstaculos.append((i-1,j-1))
        return Obstaculos
    
AEstrella1 = Aestrella(4,6)
inicio=18
final=135
AEstrella1.calcularcamino(inicio,final)
AEstrella1.GraficarCamino([inicio,final])