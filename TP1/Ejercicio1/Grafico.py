import tkinter as tk

class Grafico:
    def __init__(self, filas, columnas, obstaculos):
        self.filas = filas
        self.columnas = columnas
        self.obstaculos = obstaculos

    def dibujar_grafico(self,camino,final):
        self.camino = camino
        self.final = final
        print(self.camino)
        print(self.final)

        matriz = [[0 for j in range(self.columnas)] for i in range(self.filas)]

        # Pintar obstáculos
        for i, j in self.obstaculos:
            matriz[i][j] = 2
        # Pintar camino
        r=4
        for sublist in self.camino:
            for subsublist in sublist:
                i, j = subsublist[0], subsublist[1]
                matriz[i][j] = r
            r+=1
        # Pintar final
        for i, j in self.final:
            matriz[i][j] = 3

        # Pintar resto en blanco
        for i in range(self.filas):
            for j in range(self.columnas):
                if matriz[i][j] == 0:
                    matriz[i][j] = 1
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
                if matriz[i][j] == 1:
                    color = "white"
                if matriz[i][j] == 2:
                    color = "black"
                elif matriz[i][j] == 3:
                    color = "red"
                elif matriz[i][j] == 4:
                    color = "yellow"
                elif matriz[i][j] == 5:
                    color = "blue"
                elif matriz[i][j] == 6:
                    color = "green"
                elif matriz[i][j] == 7:
                    color = "orange"
                elif matriz[i][j] == 8:
                    color = "purple"
                elif matriz[i][j] == 9:
                    color = "grey"
                elif matriz[i][j] == 10:
                    color = "brown"
                elif matriz[i][j] == 11:
                    color = "pink"
                elif matriz[i][j] == 12:
                    color = "cyan"
                elif matriz[i][j] == 13:
                    color = "magenta"
                elif matriz[i][j] == 14:
                    color = "gold"
                elif matriz[i][j] == 15:
                    color = "silver"
                elif matriz[i][j] == 16:
                    color = "dark green"
                elif matriz[i][j] == 17:
                    color = "dark blue"
                elif matriz[i][j] == 18:
                    color = "dark red"
                elif matriz[i][j] == 19:
                    color = "dark grey"
                elif matriz[i][j] == 20:
                    color = "dark cyan"
                elif matriz[i][j] == 21:
                    color = "dark magenta"
                elif matriz[i][j] == 22:
                    color = "dark yellow"
                lienzo.create_rectangle(x1, y1, x2, y2, fill=color)

        # Ajustar tamaño del lienzo
        lienzo.config(width=self.columnas * 30, height=self.filas * 30)

        # Mostrar ventana
        lienzo.pack()
        ventana.mainloop()
