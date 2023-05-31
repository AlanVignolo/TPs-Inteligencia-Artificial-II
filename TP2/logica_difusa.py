import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import math

CONSTANTE_M = 2 # Masa del carro
CONSTANTE_m = 1 # Masa de la pertiga
CONSTANTE_l = 1 # Longitud dela pertiga
pi = math.pi
# Simula el modelo del carro-pendulo.
# Parametros:
#   t_max: tiempo maximo (inicia en 0)
#   delta_t: incremento de tiempo en cada iteracion
#   theta_0: Angulo inicial (grados)
#   v_0: Velocidad angular inicial (radianes/s)
#   a_0: Aceleracion angular inicial (radianes/s2)
def simular(t_max, delta_t, theta_0, v_0, a_0):
  theta = (theta_0 * np.pi) / 180
  v = v_0
  a = a_0

  # Simular
  z = []
  y = []
  x = np.arange(0, t_max, delta_t)

  f = 0
  ## Creo que aca es donde tengo que meter a logica difusa para que calcule la fuerza 
  ## por cada valor de theta y omega que haya
  for t in x:
    a = calcula_aceleracion(theta, v, f)
    z.append(v)
    v = v + a * delta_t
    theta = theta + v * delta_t + a * np.power(delta_t, 2) / 2
    f = LogicaDifusa(theta, v)
    y.append(theta)

  fig, ax = plt.subplots()
  fig, az = plt.subplots()
  ax.plot(x, y)
  az.plot(x,z)

  ax.set(xlabel='time (s)', ylabel='theta', title='Delta t = ' + str(delta_t) + " s")
  ax.grid()
  
  plt.show()


# Calcula la aceleracion en el siguiente instante de tiempo dado el angulo y la velocidad angular actual, y la fuerza ejercida
def calcula_aceleracion(theta, v, f):
    numerador = constants.g * np.sin(theta) + np.cos(theta) * ((-f - CONSTANTE_m * CONSTANTE_l * np.power(v, 2) * np.sin(theta)) / (CONSTANTE_M + CONSTANTE_m))
    denominador = CONSTANTE_l * (4/3 - (CONSTANTE_m * np.power(np.cos(theta), 2) / (CONSTANTE_M + CONSTANTE_m)))
    return numerador / denominador

def LogicaDifusa(theta, omega):
  posicion = ctrl.Antecedent(np.arange(-pi/30, pi/30, 0.01), 'posicion')
  velocidad = ctrl.Antecedent(np.arange(-10, 11, 1), 'velocidad')
  fuerza = ctrl.Consequent(np.arange(-10, 11, 1), 'fuerza')

  posicion['NH'] = fuzz.trimf(posicion.universe, [-pi/30, -pi/30, -pi/60])
  posicion['NL'] = fuzz.trimf(posicion.universe, [-pi/30, -pi/60, 0])
  posicion['ZE'] = fuzz.trimf(posicion.universe, [-pi/60, 0, pi/60])
  posicion['PL'] = fuzz.trimf(posicion.universe, [0, pi/60, pi/30])
  posicion['PH'] = fuzz.trimf(posicion.universe, [pi/60, pi/30, pi/30])

  velocidad['NH'] = fuzz.trimf(velocidad.universe, [-10, -10, -5])
  velocidad['NL'] = fuzz.trimf(velocidad.universe, [-10, -5, 0])
  velocidad['ZE'] = fuzz.trimf(velocidad.universe, [-5, 0, 5])
  velocidad['PL'] = fuzz.trimf(velocidad.universe, [0, 5, 10])
  velocidad['PH'] = fuzz.trimf(velocidad.universe, [5, 10, 10])

  fuerza['NH'] = fuzz.trimf(fuerza.universe, [-10, -10, -5])
  fuerza['NL'] = fuzz.trimf(fuerza.universe, [-10, -5, 0])
  fuerza['ZE'] = fuzz.trimf(fuerza.universe, [-5, 0, 5])
  fuerza['PL'] = fuzz.trimf(fuerza.universe, [0, 5, 10])
  fuerza['PH'] = fuzz.trimf(fuerza.universe, [5, 10, 10])

  rule1 = ctrl.Rule(posicion['NH'] & velocidad['NH'], fuerza['NH'])
  rule2 = ctrl.Rule(posicion['NH'] & velocidad['NL'], fuerza['NH'])
  rule3 = ctrl.Rule(posicion['NH'] & velocidad['ZE'], fuerza['NL'])
  rule4 = ctrl.Rule(posicion['NH'] & velocidad['PL'], fuerza['NL'])
  rule5 = ctrl.Rule(posicion['NH'] & velocidad['PH'], fuerza['ZE'])
  rule6 = ctrl.Rule(posicion['NL'] & velocidad['NH'], fuerza['NL'])
  rule7 = ctrl.Rule(posicion['NL'] & velocidad['NL'], fuerza['NL'])
  rule8 = ctrl.Rule(posicion['NL'] & velocidad['ZE'], fuerza['NH'])
  rule9 = ctrl.Rule(posicion['NL'] & velocidad['PL'], fuerza['ZE'])
  rule10 = ctrl.Rule(posicion['NL'] & velocidad['PH'], fuerza['PH'])
  rule11 = ctrl.Rule(posicion['ZE'] & velocidad['NH'], fuerza['PL'])
  rule12 = ctrl.Rule(posicion['ZE'] & velocidad['NL'], fuerza['NH'])
  rule13 = ctrl.Rule(posicion['ZE'] & velocidad['ZE'], fuerza['ZE'])
  rule14 = ctrl.Rule(posicion['ZE'] & velocidad['PL'], fuerza['PL'])
  rule15 = ctrl.Rule(posicion['ZE'] & velocidad['PH'], fuerza['PL'])
  rule16 = ctrl.Rule(posicion['PL'] & velocidad['NH'], fuerza['NL'])
  rule17 = ctrl.Rule(posicion['PL'] & velocidad['NL'], fuerza['ZE'])
  rule18 = ctrl.Rule(posicion['PL'] & velocidad['ZE'], fuerza['NH'])
  rule19 = ctrl.Rule(posicion['PL'] & velocidad['PL'], fuerza['PH'])
  rule20 = ctrl.Rule(posicion['PL'] & velocidad['PH'], fuerza['NH'])
  rule21 = ctrl.Rule(posicion['PH'] & velocidad['NH'], fuerza['ZE'])
  rule22 = ctrl.Rule(posicion['PH'] & velocidad['NL'], fuerza['PL'])
  rule23 = ctrl.Rule(posicion['PH'] & velocidad['ZE'], fuerza['NL'])
  rule24 = ctrl.Rule(posicion['PH'] & velocidad['PL'], fuerza['PL'])
  rule25 = ctrl.Rule(posicion['PH'] & velocidad['PH'], fuerza['PL'])

  sistema_ctrl = ctrl.ControlSystem([
      rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9,
      rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17,
      rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25
      ])
  sistema = ctrl.ControlSystemSimulation(sistema_ctrl)

  sistema.input['posicion'] = theta
  sistema.input['velocidad'] = omega
  sistema.compute()

  return sistema.output['fuerza']

simular(10, 0.01, -5, -0.9, 0)