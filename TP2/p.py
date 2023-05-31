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
        f = logica_difusa(theta, v)
        y.append(theta)

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
    if theta <= -10*np.pi/180:
        posicion_NH = 1
        posicion_NL = 0
        posicion_ZE = 0
        posicion_PL = 0
        posicion_PH = 0
    elif theta <= -5*np.pi/180:
        posicion_NH = (-theta*180/np.pi - 5) / 5
        posicion_NL = 1 - posicion_NH
        posicion_ZE = 0
        posicion_PL = 0
        posicion_PH = 0
    elif theta <= 0:
        posicion_NH = 0
        posicion_NL = 0
        posicion_ZE = (-theta*180/np.pi) / 5
        posicion_PL = 1 - posicion_ZE
        posicion_PH = 0
    elif theta <= 5*np.pi/180:
        posicion_NH = 0
        posicion_NL = 0
        posicion_ZE = 0
        posicion_PL = (theta*180/np.pi) / 5
        posicion_PH = 1 - posicion_PL
    else:
        posicion_NH = 0
        posicion_NL = 0
        posicion_ZE = 0
        posicion_PL = 0
        posicion_PH = 1

    # Funciones de membresía de velocidad
    if omega <= -10:
        velocidad_NH = 1
        velocidad_NL = 0
        velocidad_ZE = 0
        velocidad_PL = 0
        velocidad_PH = 0
    elif omega <= -5:
        velocidad_NH = (-omega - 5) / 5
        velocidad_NL = 1 - velocidad_NH
        velocidad_ZE = 0
        velocidad_PL = 0
        velocidad_PH = 0
    elif omega <= 0:
        velocidad_NH = 0
        velocidad_NL = 0
        velocidad_ZE = (-omega) / 5
        velocidad_PL = 1 - velocidad_ZE
        velocidad_PH = 0
    elif omega <= 5:
        velocidad_NH = 0
        velocidad_NL = 0
        velocidad_ZE = 0
        velocidad_PL = (omega) / 5
        velocidad_PH = 1 - velocidad_PL
    else:
        velocidad_NH = 0
        velocidad_NL = 0
        velocidad_ZE = 0
        velocidad_PL = 0
        velocidad_PH = 1

    # Funciones de membresía de fuerza
    if omega <= -10:
        fuerza_NH = 1
        fuerza_NL = 0
        fuerza_ZE = 0
        fuerza_PL = 0
        fuerza_PH = 0
    elif omega <= -5:
        fuerza_NH = (-omega - 5) / 5
        fuerza_NL = 1 - fuerza_NH
        fuerza_ZE = 0
        fuerza_PL = 0
        fuerza_PH = 0
    elif omega <= 0:
        fuerza_NH = 0
        fuerza_NL = 0
        fuerza_ZE = (-omega) / 5
        fuerza_PL = 1 - fuerza_ZE
        fuerza_PH = 0
    elif omega <= 5:
        fuerza_NH = 0
        fuerza_NL = 0
        fuerza_ZE = 0
        fuerza_PL = (omega) / 5
        fuerza_PH = 1 - fuerza_PL
    else:
        fuerza_NH = 0
        fuerza_NL = 0
        fuerza_ZE = 0
        fuerza_PL = 0
        fuerza_PH = 1

    # Reglas difusas
    rules = []
    rules.append(min(posicion_NH, velocidad_NH))
    rules.append(min(posicion_NH, velocidad_NL))
    rules.append(min(posicion_NH, velocidad_ZE))
    rules.append(min(posicion_NH, velocidad_PL))
    rules.append(min(posicion_NH, velocidad_PH))
    rules.append(min(posicion_NL, velocidad_NH))
    rules.append(min(posicion_NL, velocidad_NL))
    rules.append(min(posicion_NL, velocidad_ZE))
    rules.append(min(posicion_NL, velocidad_PL))
    rules.append(min(posicion_NL, velocidad_PH))
    rules.append(min(posicion_ZE, velocidad_NH))
    rules.append(min(posicion_ZE, velocidad_NL))
    rules.append(min(posicion_ZE, velocidad_ZE))
    rules.append(min(posicion_ZE, velocidad_PL))
    rules.append(min(posicion_ZE, velocidad_PH))
    rules.append(min(posicion_PL, velocidad_NH))
    rules.append(min(posicion_PL, velocidad_NL))
    rules.append(min(posicion_PL, velocidad_ZE))
    rules.append(min(posicion_PL, velocidad_PL))
    rules.append(min(posicion_PL, velocidad_PH))
    rules.append(min(posicion_PH, velocidad_NH))
    rules.append(min(posicion_PH, velocidad_NL))
    rules.append(min(posicion_PH, velocidad_ZE))
    rules.append(min(posicion_PH, velocidad_PL))
    rules.append(min(posicion_PH, velocidad_PH))

    # Inferencia difusa - Máximo de la regla
    fuerza_NH = max(rules[0:2])
    fuerza_NL = max(rules[2:4])
    fuerza_ZE = max(rules[4:5] + rules[10:11] + rules[18:19] + rules[21:22])
    fuerza_PL = max(rules[8:9] + rules[13:15] + rules[17:18] + rules[19:21] + rules[23:24])
    fuerza_PH = max(rules[5:6] + rules[9:10] + rules[11:13] + rules[15:17] + rules[20:23] + rules[24:25])

    # Defuzzificación - Centroide
    fuerza_centroide = (fuerza_NH * (-10) + fuerza_NL * (-7.5) + fuerza_ZE * (-2.5) + fuerza_PL * 2.5 + fuerza_PH * 7.5) / (
            fuerza_NH + fuerza_NL + fuerza_ZE + fuerza_PL + fuerza_PH)

    return fuerza_centroide

simular(150, 0.01, 8, -0.9, 0)