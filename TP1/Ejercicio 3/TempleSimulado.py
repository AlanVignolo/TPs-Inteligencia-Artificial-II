import random
from Aestrella import Aestrella
import math
import copy

class Temple ():
    def __init__ (self,filas,columnas,inicio,fin,estantes):
        self.filas = filas
        self.columnas = columnas
        self.inicio = inicio
        self.fin = fin
        self.estantes = estantes
        random.shuffle(self.estantes)
        self.lista = copy.deepcopy(estantes)
        (self.lista).insert(0,self.inicio)
        (self.lista).append(self.fin)
        self.Aestrella = Aestrella(filas,columnas)
        self.distancias = []
        self.suma=0
        self.DistanciaInicial=self.distancia()
        
        
    def distancia(self):
        aux=0
        for i in range (len(self.estantes)+1):
            aux = (self.Aestrella.calcularcamino(self.lista[i],self.lista[i+1]))[0]
            self.suma += aux
            (self.distancias).append(aux)
    
    def distanciaActual(self,suma,i):
        try:
            if i != len(self.estantes):
                suma -= self.distancias[i+1] - self.distancias[i-1]
                self.distancias[i-1] = self.Aestrella.calcularcamino(self.lista[i-1],self.lista[i])[0]
                self.distancias[i+1] = self.Aestrella.calcularcamino(self.lista[i],self.lista[i+1])[0]
                suma += self.distancias[i+1] + self.distancias[i-1]
            else:
                suma -= self.distancias [0] - self.distancias[1] - self.distancias [-1] - self.distancias[-2]
                self.distancias[0] = self.Aestrella.calcularcamino(self.lista[0],self.lista[1])[0]
                self.distancias[-1] = self.Aestrella.calcularcamino(self.lista[-1],self.lista[-2])[0]
                self.distancias[1] = self.Aestrella.calcularcamino(self.lista[1],self.lista[2])[0]
                self.distancias[-2] = self.Aestrella.calcularcamino(self.lista[-2],self.lista[-3])[0]
                suma += self.distancias[0] + self.distancias[-1] + self.distancias[1] + self.distancias[-2]
            return suma 
        except:
            return self.suma
    
    def VariarValores(self):
            numero_aleatorio1 = random.randint(1, len(self.estantes))
            listaaux = self.lista[:]

            if numero_aleatorio1 != len(self.estantes):
                listaaux[numero_aleatorio1], listaaux[numero_aleatorio1+1] = self.lista[numero_aleatorio1+1], self.lista[numero_aleatorio1]
            else:
                listaaux[numero_aleatorio1], listaaux[1] = self.lista[1], self.lista[numero_aleatorio1]
            return listaaux,numero_aleatorio1

    def TempleSimulado(self):

        nodos_visitados = set()
        nodos_visitados.add(self.lista[0])

        T = 50
        while T > 0.01:
            vecino = self.VariarValores()
            vecinodist = self.distanciaActual(self.suma,vecino[1]) 
            delta_distancia = self.suma - vecinodist

            if delta_distancia > 0 or math.exp(delta_distancia/T) < random.random():
                self.lista = list(vecino[0])
            T *= math.exp(-0.1)
        return self.lista
    
    def Graficarresultado(self,resultado1):
        (self.Aestrella).GraficarCamino(resultado1)

    def Tamaño(self,resultado):
        return (self.Aestrella).GraficarCamino(resultado,1)