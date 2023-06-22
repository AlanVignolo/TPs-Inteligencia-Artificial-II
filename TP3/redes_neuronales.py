import numpy as np
import matplotlib.pyplot as plt

# Generador basado en ejemplo del curso CS231 de Stanford: 
# CS231n Convolutional Neural Networks for Visual Recognition
# (https://cs231n.github.io/neural-networks-case-study/)
def generar_datos_clasificacion(cantidad_ejemplos, cantidad_clases,FACTOR_ANGULO,AMPLITUD_ALEATORIEDAD):
    # Calculamos la cantidad de puntos por cada clase, asumiendo la misma cantidad para cada 
    # una (clases balanceadas)
    n = int(cantidad_ejemplos / cantidad_clases)

    # Entradas: 2 columnas (x1 y x2)
    x = np.zeros((cantidad_ejemplos, 2))
    # Salida deseada ("target"): 1 columna que contendra la clase correspondiente (codificada como un entero)
    t = np.zeros(cantidad_ejemplos, dtype="uint8")  # 1 columna: la clase correspondiente (t -> "target")

    randomgen = np.random.default_rng()

    # Por cada clase (que va de 0 a cantidad_clases)...
    for clase in range(cantidad_clases):
        # Tomando la ecuacion parametrica del circulo (x = r * cos(t), y = r * sin(t)), generamos 
        # radios distribuidos uniformemente entre 0 y 1 para la clase actual, y agregamos un poco de
        # aleatoriedad
        radios = np.linspace(0, 1, n) + AMPLITUD_ALEATORIEDAD * randomgen.standard_normal(size=n)

        # ... y angulos distribuidos tambien uniformemente, con un desfasaje por cada clase
        angulos = np.linspace(clase * np.pi * FACTOR_ANGULO, (clase + 1) * np.pi * FACTOR_ANGULO, n)

        # Generamos un rango con los subindices de cada punto de esta clase. Este rango se va
        # desplazando para cada clase: para la primera clase los indices estan en [0, n-1], para
        # la segunda clase estan en [n, (2 * n) - 1], etc.
        indices = range(clase * n, (clase + 1) * n)

        # Generamos las "entradas", los valores de las variables independientes. Las variables:
        # radios, angulos e indices tienen n elementos cada una, por lo que le estamos agregando
        # tambien n elementos a la variable x (que incorpora ambas entradas, x1 y x2)
        x1 = radios * np.sin(angulos)
        x2 = radios * np.cos(angulos)
        x[indices] = np.c_[x1, x2]

        # Guardamos el valor de la clase que le vamos a asociar a las entradas x1 y x2 que acabamos
        # de generar
        t[indices] = clase

    return x, t

def generar_datos_alternativo(cantidad_ejemplos, cantidad_clases, FACTOR_ANGULO = 0.79, AMPLITUD_ALEATORIEDAD = 0.1):
    n = int(cantidad_ejemplos / cantidad_clases)
    x = np.zeros((cantidad_ejemplos, 2))
    t = np.zeros(cantidad_ejemplos, dtype="uint8") 

    randomgen = np.random.default_rng()

    for clase in range(cantidad_clases):
        # Generamos radios a partir de una distribución normal en lugar de una línea recta
        radios = randomgen.normal(loc=0.5, scale=0.1, size=n) + AMPLITUD_ALEATORIEDAD * randomgen.standard_normal(size=n)
        
        # Generamos ángulos a partir de una distribución uniforme en lugar de una línea recta
        angulos = randomgen.uniform(low=clase * np.pi * FACTOR_ANGULO, high=(clase + 1) * np.pi * FACTOR_ANGULO, size=n)
        
        indices = range(clase * n, (clase + 1) * n)

        x1 = radios * np.sin(angulos)
        x2 = radios * np.cos(angulos)
        x[indices] = np.c_[x1, x2]

        t[indices] = clase

    return x, t

def inicializar_pesos(n_entrada, n_capa_2, n_capa_3):
    randomgen = np.random.default_rng()

    w1 = 0.1 * randomgen.standard_normal((n_entrada, n_capa_2))
    b1 = 0.1 * randomgen.standard_normal((1, n_capa_2))

    w2 = 0.1 * randomgen.standard_normal((n_capa_2, n_capa_3))
    b2 = 0.1 * randomgen.standard_normal((1,n_capa_3))

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

def clasificar(x, pesos,tipo):
    # Corremos la red "hacia adelante"
    resultados_feed_forward = ejecutar_adelante(x, pesos)
    
    # Buscamos la(s) clase(s) con scores mas altos (en caso de que haya mas de una con 
    # el mismo score estas podrian ser varias). Dado que se puede ejecutar en batch (x 
    # podria contener varios ejemplos), buscamos los maximos a lo largo del axis=1 
    # (es decir, por filas)
    if tipo == "regresion":
        max_scores = resultados_feed_forward["y"]
        return max_scores
    else:
        max_scores = np.argmax(resultados_feed_forward["y"], axis=1)

        # Tomamos el primero de los maximos (podria usarse otro criterio, como ser eleccion aleatoria)
        # Nuevamente, dado que max_scores puede contener varios renglones (uno por cada ejemplo),
        # retornamos la primera columna
        return max_scores[:, 0]

# x: n entradas para cada uno de los m ejemplos(nxm)
# t: salida correcta (target) para cada uno de los m ejemplos (m x 1)
# pesos: pesos (W y b)
def train(x, t, pesos, learning_rate, epochs,validation_data):
    j=0
    patience=50  ###
    tolerance=1e-4  ###
        # Variables para el control de overfitting
    best_loss = np.inf ###
    epochs_without_improvement = 0  ###

    # Listas para almacenar loss y accuracy en cada epoch
    loss_history = []   ###
    accuracy_history = []   ###
    
     # Cantidad de filas (i.e. cantidad de ejemplos)
    m = np.size(x, 0) 

    for i in range(epochs+1):
        # Ejecucion de la red hacia adelante
        resultados_feed_forward = ejecutar_adelante(x, pesos)
        y = resultados_feed_forward["y"]
        h = resultados_feed_forward["h"]
        z = resultados_feed_forward["z"]

        # LOSS
        # a. Exponencial de todos los scores
        exp_scores = np.exp(y)

        # b. Suma de todos los exponenciales de los scores, fila por fila (ejemplo por ejemplo).
        #    Mantenemos las dimensiones (indicamos a NumPy que mantenga la segunda dimension del
        #    arreglo, aunque sea una sola columna, para permitir el broadcast correcto en operaciones
        #    subsiguientes)
        sum_exp_scores = np.sum(exp_scores, axis=1, keepdims=True)

        # c. "Probabilidades": normalizacion de las exponenciales del score de cada clase (dividiendo por 
        #    la suma de exponenciales de todos los scores), fila por fila
        p = exp_scores / sum_exp_scores

        # d. Calculo de la funcion de perdida global. Solo se usa la probabilidad de la clase correcta, 
        #    que tomamos del array t ("target")

        loss = (1 / m) * np.sum( -np.log( p[range(m), t] ))
        
        # Para esto necesito calcular el numero de aciertos/ cantidad de ejemplos(m)
        clases_predichas = np.argmax(y, axis=1) # Por cada fila me devuelve la posicion del maximo que a su vez es la clase predicha
        aciertos = np.sum(clases_predichas == t)
        precision = aciertos / m

        # Guardamos los valores de loss y accuracy en cada epoch
        loss_history.append(loss)   ###
        accuracy_history.append(precision*100)  ###

        # Verificar si loss ha empeorado
        if loss > best_loss + tolerance: ###
            epochs_without_improvement += 1 ###
        else:
            best_loss = loss    ###
            epochs_without_improvement = 0  ###
       
        # Mostramos solo cada 1000 epochs
        if i %1000 == 0:
            print(f"epoch: {i}, Loss: {loss}, Precisión: {precision}")
        
        # Detener el entrenamiento si loss no mejora durante 'patience' epochs consecutivos
        if epochs_without_improvement >= patience:
            #print("Deteniendo el entrenamiento debido a falta de mejora en loss.")  ###
            if j == 0:
                print(f"epoch: {i}, Loss: {loss}, Precisión: {precision}")
                detencion_temprana_loss = loss  ###
                detencion_temprana_accuracy = precision*100  ###
                detencion_temprana_epoch = i  ###
            break
            j += 1

        # Extraemos los pesos a variables locales
        w1 = pesos["w1"]
        b1 = pesos["b1"]
        w2 = pesos["w2"]
        b2 = pesos["b2"]

        # Ajustamos los pesos: Backpropagation
        dL_dy = p                # Para todas las salidas, L' = p (la probabilidad)...
        dL_dy[range(m), t] -= 1  # ... excepto para la clase correcta
        dL_dy /= m

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

    fig1 = plt.figure()
    ax = fig1.subplots(2, 1)    ###
    # Generar el gráfico de loss vs epoch
    ax[0].plot(range(len(loss_history)), loss_history, color='blue', label='Loss',linewidth=1.5)    ###
    ax[0].hlines( best_loss,xmin=0,xmax=10000, color='red', label=f"Detencion = {round(best_loss,4)}",linewidth=1)    ###
    ax[0].hlines( best_loss+tolerance,xmin=0,xmax=10000, color='Orange', label='Detencion - Tolerance',linewidth=1)    ###
    ax[0].vlines(detencion_temprana_epoch,ymin=0,ymax=1, color='red', label=f"Detencion = {round(detencion_temprana_epoch)}",linewidth=1)    ###
    ax[0].vlines(detencion_temprana_epoch-patience,ymin=0,ymax=1, color='Orange', label='Detencion + Patience',linewidth=1)    ###
    ax[0].legend()   ###
    ax[0].set_xlabel('Epoch', loc='right') ###
    ax[0].set_ylabel('Loss', loc='top')  ###
    ax[0].set_title('Loss vs Epoch')  ###
    ax[0].grid(True)   ###
    
    # Generar el gráfico de accuracy vs epoch
    ax[1].plot(range(len(accuracy_history)), accuracy_history, label='Accuracy',linewidth=1.5)    ###
    ax[1].hlines(detencion_temprana_accuracy,xmin=0,xmax=10000, color='red', label=f"Accuracy = {round(detencion_temprana_accuracy,3)} %",linewidth=1)    ###
    ax[1].vlines(detencion_temprana_epoch,ymin=0,ymax=1, color='red', label=f"Detencion = {round(detencion_temprana_epoch)}",linewidth=1)    ###
    ax[1].legend()   ###
    ax[1].set_xlabel('Epoch', loc='right') ###
    ax[1].set_ylabel('Accuracy', loc='top')  ###
    ax[1].set_title('Accuracy vs Epoch')  ###
    
    ax[1].grid(True)   ###

    plt.tight_layout()  ###
    plt.show(block=True)  ###

def train_test_split(x, t, test_size):
    # Cantidad de filas (i.e. cantidad de ejemplos)
    m = np.size(x, 0) 

    # Cantidad de ejemplos para el set de test
    test_examples = int(m * test_size)

    # Indices de los ejemplos para el set de test
    test_indices = np.random.choice(m, test_examples, replace=False)

    # Indices de los ejemplos para el set de entrenamiento
    train_indices = np.delete(np.arange(m), test_indices)

    # Set de test
    x_test = x[test_indices]
    t_test = t[test_indices]

    # Set de entrenamiento
    x_train = x[train_indices]
    t_train = t[train_indices]

    return x_train, x_test, t_train, t_test

def iniciar(numero_clases, graficar_datos,x,t):
    # Establecer la semilla asegurar que el código produzca los mismos resultados cada vez que se ejecuta
    np.random.seed(42)

    # Division aleatoria de los datos de entrenamiento y los de test    
    x_train, x_test, t_train, t_test = train_test_split(x, t, test_size=0.3)

    # Normalizar los datos
    x_train = (x_train - np.mean(x_train, axis=0)) / np.std(x_train, axis=0)    ###
    x_test = (x_test - np.mean(x_test, axis=0)) / np.std(x_test, axis=0)    ###

    # Graficamos los datos si es necesario
    if graficar_datos:
        # Parametro: "c": color (un color distinto para cada clase en t)
        plt.scatter(x[:, 0], x[:, 1], c=t)
        plt.show()

    # Inicializa pesos de la red
    NEURONAS_CAPA_OCULTA = 100
    NEURONAS_ENTRADA = 2
    pesos = inicializar_pesos(n_entrada=NEURONAS_ENTRADA, n_capa_2=NEURONAS_CAPA_OCULTA, n_capa_3=numero_clases)

    # Entrena
    LEARNING_RATE=1
    EPOCHS=10000
    train(x_train, t_train, pesos, LEARNING_RATE, EPOCHS,validation_data=(x_test, t_test))

    # Test
    resultados_feed_forward = ejecutar_adelante(x_test, pesos)
    y_test = resultados_feed_forward["y"]
    
    clases_predichas = np.argmax(y_test, axis=1) # Por cada fila me devuelve la posicion del maximo que a su vez es la clase predicha
    aciertos = np.sum(clases_predichas == t_test)
    precision = aciertos / np.size(x_test, 0)
    print("Precision: ", precision)

def generar_datos_regresion(cantidad_ejemplos, cantidad_clases):

    # Calculamos la cantidad de puntos por cada clase, asumiendo la misma cantidad para cada 
    # una (clases balanceadas)
    # Entradas: 2 columnas (x1 y x2)
    x = np.zeros((cantidad_ejemplos, 1))
    # Salida deseada ("target"): 1 columna que contendra la clase correspondiente (codificada como un entero)
    t = np.zeros((cantidad_ejemplos, 1))  # 1 columna: la clase correspondiente (t -> "target")
    randomgen = np.random.default_rng()
    for n in range(cantidad_ejemplos):
        random_num = randomgen.uniform(-10,10)
        x[n] = random_num
        t[n] = pow(x[n],2)

    return x, t

def inicializar_pesos_MSE(n_entrada, n_capa_2, n_capa_3):
    randomgen = np.random.default_rng()

    w1 = 0.01 * randomgen.standard_normal((n_entrada, n_capa_2))
    b1 = 0.01 * randomgen.standard_normal((1, n_capa_2))

    w2 = 0.01 * randomgen.standard_normal((n_capa_2, n_capa_3))
    b2 = 0.01 * randomgen.standard_normal((1,n_capa_3))

    return {"w1": w1, "b1": b1, "w2": w2, "b2": b2}

def train_MSE(x, t, pesos, learning_rate, epochs, tol, x_val, t_val):
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
        if i %1000 == 0:
            print(f"epoch: {i}, Loss: {loss[i]}, Validation Set Loss: {loss_val[i]}")
        
        #NEW Precisión de clasificación
        if i % 1000 == 0:
            resultados = clasificar(x, pesos,"regresion")
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
        dL_dh = np.dot(dL_dy, w2.T)
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

def iniciar_MSE(numero_clases, numero_ejemplos, graficar_datos,x,t):
    
    # NEW Generamos ejemplos para test
    x_test, t_test = generar_datos_regresion(int(numero_ejemplos/4), numero_clases)
    
    # NEW Generamos ejemplos para validacion
    x_val, t_val = generar_datos_regresion(int(numero_ejemplos*3/4), numero_clases)

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
    NEURONAS_CAPA_OCULTA = 100
    NEURONAS_ENTRADA = 1
    pesos = inicializar_pesos(n_entrada=NEURONAS_ENTRADA, n_capa_2=NEURONAS_CAPA_OCULTA, n_capa_3=numero_clases)

    # Entrena
    LEARNING_RATE=0.001
    EPOCHS=20001
    CROSS_VALIDATION_TOLERANCE=0.05
    train_MSE(x, t, pesos, LEARNING_RATE, EPOCHS, CROSS_VALIDATION_TOLERANCE, x_val, t_val)
    
    resultados = clasificar(x_test, pesos,"regresion")
    for objetivo, resultado in zip(t_test, resultados):
        resta = t_test - resultados
        powers = np.zeros((np.size(t_test), 1))
        for j in range(np.size(t_test)):
            powers[j] = 2
        mse = np.sum(np.power(resta, powers))/np.size(t_test)
    print("MSE Test Set= ", mse)
    plt.figure()
    plt.scatter(x_test, resultados[:,3], c="red")
    plt.title("resultados")

# Inicialización y entrenamiento de la red
numero_clases = 4
numero_ejemplos = 1000

x, t = generar_datos_clasificacion(numero_ejemplos, numero_clases, 0.79, 0.1)
#iniciar(numero_clases, graficar_datos=False, x=x, t=t)

x1, t1 = generar_datos_clasificacion(numero_ejemplos, numero_clases, 0.9, 0.15)
iniciar(numero_clases, graficar_datos=False, x=x1, t=t1)

x2, t2 = generar_datos_alternativo(numero_ejemplos, numero_clases)
iniciar(numero_clases, graficar_datos=False, x=x2, t=t2)    

x3, t3 = generar_datos_regresion(numero_ejemplos, numero_clases)
#iniciar_MSE(numero_clases, numero_ejemplos, graficar_datos=False, x=x3, t=t3)

fig2 = plt.figure()
ax1 = fig2.subplots(3, 1)

ax1[0].scatter(x[:, 0], x[:, 1], c=t, cmap='viridis')
ax1[0].set_title('Datos generados por función original')
ax1[0].legend()   
ax1[0].grid(True)

ax1[1].scatter(x1[:, 0], x1[:, 1], c=t1, cmap='viridis')
ax1[1].set_title('Datos generados por función modificada')
ax1[1].legend()
ax1[1].grid(True)

ax1[2].scatter(x2[:, 0], x2[:, 1], c=t2, cmap='viridis')
ax1[2].set_title('Datos generados por nueva función')
ax1[2].legend()
ax1[2].grid(True)

plt.tight_layout()
plt.show(block=True)