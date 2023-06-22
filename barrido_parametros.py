import numpy as np
import matplotlib.pyplot as plt
import math
from copy import copy

# Generador basado en ejemplo del curso CS231 de Stanford: 
# CS231n Convolutional Neural Networks for Visual Recognition
# (https://cs231n.github.io/neural-networks-case-study/)
def generar_datos_clasificacion(cantidad_ejemplos, cantidad_clases):

    # Calculamos la cantidad de puntos por cada clase, asumiendo la misma cantidad para cada 
    # una (clases balanceadas)
    

    # Entradas: 2 columnas (x1 y x2)
    x = np.zeros((cantidad_ejemplos, 1))
    # Salida deseada ("target"): 1 columna que contendra la clase correspondiente (codificada como un entero)
    t = np.zeros((cantidad_ejemplos, 1))  # 1 columna: la clase correspondiente (t -> "target")
    randomgen = np.random.default_rng()
    for n in range(cantidad_ejemplos):
        random_num = randomgen.uniform(-1,1)
        x[n] = random_num
        t[n] = pow(x[n],2)

    return x, t


def inicializar_pesos(n_entrada, n_capa_2, n_capa_3):
    randomgen = np.random.default_rng()

    w1 = 0.01 * randomgen.standard_normal((n_entrada, n_capa_2))
    b1 = 0.01 * randomgen.standard_normal((1, n_capa_2))

    w2 = 0.01 * randomgen.standard_normal((n_capa_2, n_capa_3))
    b2 = 0.01 * randomgen.standard_normal((1,n_capa_3))

    return {"w1": w1, "b1": b1, "w2": w2, "b2": b2}


def ejecutar_adelante(x, pesos):
    # Funcion de entrada (a.k.a. "regla de propagacion") para la primera capa oculta    
    z = x.dot(pesos["w1"]) + pesos["b1"]

    # Funcion de activacion ReLU para la capa oculta (h -> "hidden")
    h = np.maximum(0, z)

    # Salida de la red (funcion de activacion lineal). Esto incluye la salida de todas
    # las neuronas y para todos los ejemplos proporcionados
    y = h.dot(pesos["w2"]) + pesos["b2"]

    return {"z": z, "h": h, "y": y}


def clasificar(x, pesos):
    # Corremos la red "hacia adelante"
    resultados_feed_forward = ejecutar_adelante(x, pesos)
    
    # Buscamos la(s) clase(s) con scores mas altos (en caso de que haya mas de una con 
    # el mismo score estas podrian ser varias). Dado que se puede ejecutar en batch (x 
    # podria contener varios ejemplos), buscamos los maximos a lo largo del axis=1 
    # (es decir, por filas)
    
    
    max_scores = resultados_feed_forward["y"]

    # Tomamos el primero de los maximos (podria usarse otro criterio, como ser eleccion aleatoria)
    # Nuevamente, dado que max_scores puede contener varios renglones (uno por cada ejemplo),
    # retornamos la primera columna
    
    return max_scores 

# x: n entradas para cada uno de los m ejemplos(nxm)
# t: salida correcta (target) para cada uno de los m ejemplos (m x 1)
# pesos: pesos (W y b)
def train(x, t, pesos, learning_rate, epochs, tol, x_val, t_val, print_data):
    # Cantidad de filas (i.e. cantidad de ejemplos)
    m = np.size(x, 0)
    m_val = np.size(x_val, 0)
    
    #NEW Guardamos valores historicos de loss
    loss = []
    loss_val = []
    
    powers = np.zeros((m, 1))
    powers_val = np.zeros((m_val, 1))
    for j in range(m):
        powers[j] = 2
    for j in range(m_val):
        powers_val[j] = 2
    
    for i in range(epochs):
        # Ejecucion de la red hacia adelante
        resultados_feed_forward = ejecutar_adelante(x, pesos)
        y = resultados_feed_forward["y"]
        h = resultados_feed_forward["h"]
        z = resultados_feed_forward["z"]

        # NEW Ejecucion de la red con ejemplos de validacion
        resultados_feed_forward_val = ejecutar_adelante(x_val, pesos)
        y_val = resultados_feed_forward_val["y"]

        resta = t - y
        resta_val = t_val - y_val

        
        pot = np.power(resta, powers)

        pot_val = np.power(resta_val, powers_val)
        num = np.sum(pot)
        num_val = np.sum(pot_val)

        
        # d. Calculo de la funcion de perdida global. Solo se usa la probabilidad de la clase correcta, 
        #    que tomamos del array t ("target")
        loss.append(num/m)
        loss_val.append(num_val/m_val)
        
        
        # Mostramos solo cada 1000 epochs
        if i %1000 == 0 and print_data:
            print(f"--------EPOCH {i}--------")
            print("Train Set Loss:", loss[i])
            print("Validation Set Loss: ", loss_val[i])
            
        
        #NEW Precisión de clasificación
        if i % 1000 == 0 and print_data:
            resultados = clasificar(x, pesos)
            for objetivo, resultado in zip(t, resultados):
                resta = t - resultados
                powers = np.zeros((np.size(t), 1))
                for j in range(np.size(t)):
                    powers[j] = 2
                mse = np.sum(np.power(resta, powers))/np.size(t)
            print("MSE Train Set=", mse)
        
        #NEW Cross Validation
        if i%1000 == 0 and i>0:
            num = (loss_val[i] - loss_val[i-1000])/loss_val[i-1000]
            print("Loss change =", num)
            if num > tol:
                print("Early Stop")
                break
            
        # Extraemos los pesos a variables locales
        w1 = pesos["w1"]
        b1 = pesos["b1"]
        w2 = pesos["w2"]
        b2 = pesos["b2"]

        # Ajustamos los pesos: Backpropagation
        dL_dy = -2*resta/m

        dL_dw2 = h.T.dot(dL_dy)                         # Ajuste para w2
        dL_db2 = np.sum(dL_dy, axis=0, keepdims=True)   # Ajuste para b2

        dL_dh = dL_dy.dot(w2.T)
        
        dL_dz = dL_dh       # El calculo dL/dz = dL/dh * dh/dz. La funcion "h" es la funcion de activacion de la capa oculta,
        dL_dz[z <= 0] = 0   # para la que usamos ReLU. La derivada de la funcion ReLU: 1(z > 0) (0 en otro caso)

        dL_dw1 = x.T.dot(dL_dz)                         # Ajuste para w1
        dL_db1 = np.sum(dL_dz, axis=0, keepdims=True)   # Ajuste para b1
        
        
        # Aplicamos el ajuste a los pesos
        w1 += -learning_rate * dL_dw1
        b1 += -learning_rate * dL_db1
        w2 += -learning_rate * dL_dw2
        b2 += -learning_rate * dL_db2

        # Actualizamos la estructura de pesos
        # Extraemos los pesos a variables locales
        pesos["w1"] = w1
        pesos["b1"] = b1
        pesos["w2"] = w2
        pesos["b2"] = b2


def iniciar(numero_clases, numero_ejemplos, graficar_datos):
    valores = 5
    results = []
    k_fold = 5
    for l_rate_counter in range(valores):
        for neurona_counter in range(valores):
            avg = 0
            for k in range(k_fold):
                # Generamos datos
                x, t = generar_datos_clasificacion(numero_ejemplos, numero_clases)
                
                # NEW Generamos ejemplos para test
                x_test, t_test = generar_datos_clasificacion(int(numero_ejemplos/4), numero_clases)
                
                # NEW Generamos ejemplos para validacion
                x_val, t_val = generar_datos_clasificacion(int(numero_ejemplos/4), numero_clases)
            
                # Graficamos los datos si es necesario
                if graficar_datos:
                    # Parametro: "c": color (un color distinto para cada clase en t)
                    plt.figure()
                    plt.scatter(x, t)
                    plt.title("Set Training")
                    plt.figure()
                    plt.scatter(x_test, t_test)
                    plt.title("Set Test")
                    plt.figure()
                    plt.scatter(x_val, t_val)
                    plt.title("Set Validación")
                    plt.show()
      
    
                # Inicializa pesos de la red
                NEURONAS_CAPA_OCULTA = 20*(neurona_counter+1) + 1
                NEURONAS_ENTRADA = 1
                pesos = inicializar_pesos(n_entrada=NEURONAS_ENTRADA, n_capa_2=NEURONAS_CAPA_OCULTA, n_capa_3=numero_clases)
            
                # Entrena
                LEARNING_RATE= math.pow(10, -4+l_rate_counter)
                EPOCHS=5001
                CROSS_VALIDATION_TOLERANCE=0.05
                print(F"train {NEURONAS_CAPA_OCULTA}, {LEARNING_RATE}")
                train(x, t, pesos, LEARNING_RATE, EPOCHS, CROSS_VALIDATION_TOLERANCE, x_val, t_val, print_data=False)
                
                resultados = clasificar(x_test, pesos)
                for objetivo, resultado in zip(t_test, resultados):
                    resta = t_test - resultados
                    powers = np.zeros((np.size(t_test), 1))
                    for j in range(np.size(t_test)):
                        powers[j] = 2
                    mse = np.sum(np.power(resta, powers))/np.size(t_test)
                avg += mse
                print("MSE Test Set= ", mse)
                plt.figure()
                plt.scatter(x_test, resultados)
                plt.title("resultados")
            avg /= 5
            results.append(copy(avg))
    best = min(results)
    idx = results.index(best)
    neurona = idx%valores
    learning_rate = math.floor(idx/valores)
    print(f"best result {best}, index {idx}, learning_rate {math.pow(10, -4+learning_rate)}, neuronas capa oculta {20*(neurona+1) + 1}")

iniciar(numero_clases=1, numero_ejemplos=800, graficar_datos=False)