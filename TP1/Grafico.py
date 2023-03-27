import tkinter as tk

class Grafic:
    def __init__(self, filas, columnas, obstaculos, camino,final):
        self.filas = filas
        self.columnas = columnas
        self.obstaculos = obstaculos
        self.camino = camino
        self.final = final

    def dibujar_grafico(self):
        # Crear matriz con ceros
        matriz = [[0 for j in range(self.columnas)] for i in range(self.filas)]


        # Pintar obstáculos
        for i, j in self.obstaculos:
            matriz[i][j] = 3
        # Pintar camino
        for i, j in self.camino:
            matriz[i][j] = 2

        # Pintar resto en blanco
        for i in range(self.filas):
            for j in range(self.columnas):
                if matriz[i][j] == 0:
                    matriz[i][j] = 1

        matriz[self.final[0]][self.final[1]]=4

        # Crear ventana
        ventana = tk.Tk()
        ventana.title("Grafico")

        # Crear lienzo
        lienzo = tk.Canvas(ventana)

        # Crear rectángulos
        for i in range(self.filas):
            for j in range(self.columnas):
                x1 = j * 30
                y1 = i * 30
                x2 = x1 + 30
                y2 = y1 + 30
                color = "white"
                if matriz[i][j] == 2:
                    color = "yellow"
                elif matriz[i][j] == 3:
                    color = "black"
                elif matriz[i][j] == 4:
                    color = "red"
                lienzo.create_rectangle(x1, y1, x2, y2, fill=color)

        # Ajustar tamaño del lienzo
        lienzo.config(width=self.columnas * 30, height=self.filas * 30)

        # Mostrar ventana
        lienzo.pack()
        ventana.mainloop()
