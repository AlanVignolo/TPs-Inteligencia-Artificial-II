import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

CONSTANTE_M = 2  # Masa del carro
CONSTANTE_m = 1  # Masa de la pertiga
CONSTANTE_l = 1  # Longitud dela pertiga

def simular(t_max, delta_t, theta_0, v_0, a_0):
    theta = (theta_0 * np.pi) / 180
    v = v_0
    a = a_0

    # Simular
    z = []
    y = []
    x = np.arange(0, t_max, delta_t)

    f = 0
    for t in x:
        a = calcula_aceleracion(theta, v, f)
        z.append(v)
        v = v + a * delta_t
        theta = theta + v * delta_t + a * np.power(delta_t, 2) / 2
        if theta == 0:
            break
        f = logica_difusa(theta, v)
        y.append(theta*180/np.pi)

    fig, ax = plt.subplots()
    fig, az = plt.subplots()
    ax.plot(x, y)
    az.plot(x, z)

    ax.set(xlabel='time (s)', ylabel='theta', title='Delta t = ' + str(delta_t) + " s")
    ax.grid()


    plt.show()


# Calcula la aceleracion en el siguiente instante de tiempo dado el angulo y la velocidad angular actual, y la fuerza ejercida
def calcula_aceleracion(theta, v, f):
    numerador = constants.g * np.sin(theta) + np.cos(theta) * ((-f - CONSTANTE_m * CONSTANTE_l * np.power(v, 2) * np.sin(theta)) / (CONSTANTE_M + CONSTANTE_m))
    denominador = CONSTANTE_l * (4 / 3 - (CONSTANTE_m * np.power(np.cos(theta), 2) / (CONSTANTE_M + CONSTANTE_m)))
    return numerador / denominador

def logica_difusa(theta, omega):
    # Funciones de membresía de posición

    theta = theta*180/np.pi

    if theta <= -10:
        posicion_NH = 1
        posicion_NL = 0
        posicion_ZE = 0
        posicion_PL = 0
        posicion_PH = 0
    elif theta <= -5:
        posicion_NH = (-theta - 5) / 5
        posicion_NL = 1 - posicion_NH
        posicion_ZE = 0
        posicion_PL = 0
        posicion_PH = 0
    elif theta <= 0:
        posicion_NH = 0
        posicion_NL = (-theta) / 5
        posicion_ZE = 1 - posicion_NL
        posicion_PL = 0
        posicion_PH = 0
    elif theta <= 5:
        posicion_NH = 0
        posicion_NL = 0
        posicion_ZE = (-theta+5) / 5
        posicion_PL = 1 - posicion_ZE
        posicion_PH = 0
    elif theta <=10:
        posicion_NH = 0
        posicion_NL = 0
        posicion_ZE = 0
        posicion_PL = ((-theta)+10) / 5
        posicion_PH = 1 - posicion_PL
    else:
        posicion_NH = 0
        posicion_NL = 0
        posicion_ZE = 0
        posicion_PL = 0
        posicion_PH = 1

    # Funciones de membresía de velocidad
    if omega <= -5:
        velocidad_NH = 1
        velocidad_NL = 0
        velocidad_ZE = 0
        velocidad_PL = 0
        velocidad_PH = 0
    elif omega <= -2.5:
        velocidad_NH = (-omega - 2.5) / 2.5
        velocidad_NL = 1 - velocidad_NH
        velocidad_ZE = 0
        velocidad_PL = 0
        velocidad_PH = 0
    elif omega <= 0:
        velocidad_NH = 0
        velocidad_NL = (-omega) / 2.5
        velocidad_ZE = 1 - velocidad_NL
        velocidad_PL = 0
        velocidad_PH = 0
    elif omega <= 2.5:
        velocidad_NH = 0
        velocidad_NL = 0
        velocidad_ZE = (-omega+2.5) / 2.5
        velocidad_PL = 1 - velocidad_ZE
        velocidad_PH = 0
    elif omega <= 5:
        velocidad_NH = 0
        velocidad_NL = 0
        velocidad_ZE = 0
        velocidad_PL = (-omega+5) / 2.5
        velocidad_PH = 1 - velocidad_PL
    else:
        velocidad_NH = 0
        velocidad_NL = 0
        velocidad_ZE = 0
        velocidad_PL = 0
        velocidad_PH = 1

    # Reglas difusas
    rules = []

    #RESULTADO F = NH

    rules.append(np.fmin(posicion_NH, velocidad_NH))
    rules.append(np.fmin(posicion_NH, velocidad_NL))
    rules.append(np.fmin(posicion_NL, velocidad_NH))
    rules.append(np.fmin(posicion_NL, velocidad_NL))
    rules.append(np.fmin(posicion_NH, velocidad_ZE))
    rules.append(np.fmin(posicion_ZE, velocidad_NH))

    #RESULTADO F = NL
    rules.append(np.fmin(posicion_NL, velocidad_ZE))
    rules.append(np.fmin(posicion_ZE, velocidad_NL))
    rules.append(np.fmin(posicion_PL, velocidad_NH))
    rules.append(np.fmin(posicion_NH, velocidad_PL))

    #RESULTADO F = ZE
    rules.append(np.fmin(posicion_NH, velocidad_PH))
    rules.append(np.fmin(posicion_NL, velocidad_PL))    
    rules.append(np.fmin(posicion_ZE, velocidad_ZE))
    rules.append(np.fmin(posicion_PH, velocidad_NH))
    rules.append(np.fmin(posicion_PL, velocidad_NL))
    
    #RESULTADO F = PL
    rules.append(np.fmin(posicion_ZE, velocidad_PL))
    rules.append(np.fmin(posicion_PH, velocidad_NL))
    rules.append(np.fmin(posicion_PL, velocidad_ZE))
    rules.append(np.fmin(posicion_NL, velocidad_PH))

    #RESULTADO F = PH
    rules.append(np.fmin(posicion_ZE, velocidad_PH))    
    rules.append(np.fmin(posicion_PH, velocidad_ZE))
    rules.append(np.fmin(posicion_PH, velocidad_PL))
    rules.append(np.fmin(posicion_PH, velocidad_PH))
    rules.append(np.fmin(posicion_PL, velocidad_PH))
    rules.append(np.fmin(posicion_PL, velocidad_PL))

    # Inferencia difusa - Máximo 
    fuerza_NH = max (rules[0:5])
    fuerza_NL = max(rules[6:9])
    fuerza_ZE = max(rules[10:14])
    fuerza_PL = max(rules[15:18])
    fuerza_PH = max(rules[19:24])

    aux = fuerza_NH + fuerza_NL + fuerza_ZE + fuerza_PL + fuerza_PH

    # Desborrozificacion
    fuerza_centroide = (fuerza_NH * (-100) + fuerza_NL * (-50) + fuerza_ZE * (0) + fuerza_PL * 50 + fuerza_PH * 100) / aux

    return fuerza_centroide

simular(10, 0.01, 9.5, -3, 0)