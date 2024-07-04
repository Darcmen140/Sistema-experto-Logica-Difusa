import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Interfaz de Usuario
class InterfazUsuario:
    def __init__(self, calcular_callback):
        self.calcular_callback = calcular_callback
        self.root = tk.Tk()
        self.root.title("Recomendación de Ejercicio Diario - Sistema Difuso")

        tk.Label(self.root, text="Edad (0-100):").grid(row=0, column=0, padx=10, pady=5)
        self.entrada_edad = tk.Entry(self.root)
        self.entrada_edad.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="IMC (10-40):").grid(row=1, column=0, padx=10, pady=5)
        self.entrada_imc = tk.Entry(self.root)
        self.entrada_imc.grid(row=1, column=1, padx=10, pady=5)

        self.boton_calcular = tk.Button(self.root, text="Calcular", command=self.calcular)
        self.boton_calcular.grid(row=2, column=0, columnspan=2, pady=10)

        self.etiqueta_resultado = tk.Label(self.root, text="Ejercicio diario recomendado: ")
        self.etiqueta_resultado.grid(row=3, column=0, columnspan=2, pady=5)

    def calcular(self):
        edad_val = self.validar_entrada(self.entrada_edad.get(), 0, 100)
        imc_val = self.validar_entrada(self.entrada_imc.get(), 10, 40)
        if edad_val is not None and imc_val is not None:
            ejercicio_val = self.calcular_callback(edad_val, imc_val)
            self.etiqueta_resultado.config(text=f"Ejercicio diario recomendado: {ejercicio_val:.2f} minutos")

    @staticmethod
    def validar_entrada(entrada, min_val, max_val):
        try:
            valor = float(entrada)
            if valor < min_val or valor > max_val:
                raise ValueError
            return valor
        except ValueError:
            messagebox.showerror("Entrada inválida", f"Por favor, ingrese un valor entre {min_val} y {max_val}.")
            return None

    def ejecutar(self):
        self.root.mainloop()

# Motor de Inferencia
class MotorInferencia:
    def __init__(self):
        # Definir variables difusas
        self.edad = ctrl.Antecedent(np.arange(0, 101, 1), 'edad')
        self.imc = ctrl.Antecedent(np.arange(10, 41, 1), 'imc')
        self.ejercicio_diario = ctrl.Consequent(np.arange(0, 121, 1), 'ejercicio_diario')

        # Funciones de membresía para edad
        self.edad['joven'] = fuzz.trimf(self.edad.universe, [0, 0, 30])
        self.edad['adulto'] = fuzz.trimf(self.edad.universe, [20, 50, 80])
        self.edad['mayor'] = fuzz.trimf(self.edad.universe, [60, 100, 100])

        # Funciones de membresía para IMC
        self.imc['bajo'] = fuzz.trimf(self.imc.universe, [10, 10, 18.5])
        self.imc['normal'] = fuzz.trimf(self.imc.universe, [18.5, 24.9, 24.9])
        self.imc['alto'] = fuzz.trimf(self.imc.universe, [25, 40, 40])

        # Funciones de membresía para ejercicio diario
        self.ejercicio_diario['poco'] = fuzz.trimf(self.ejercicio_diario.universe, [0, 0, 30])
        self.ejercicio_diario['moderado'] = fuzz.trimf(self.ejercicio_diario.universe, [20, 60, 100])
        self.ejercicio_diario['mucho'] = fuzz.trimf(self.ejercicio_diario.universe, [80, 120, 120])

        # Reglas difusas
        rule1 = ctrl.Rule(self.edad['joven'] & self.imc['bajo'], self.ejercicio_diario['moderado'])
        rule2 = ctrl.Rule(self.edad['joven'] & self.imc['normal'], self.ejercicio_diario['mucho'])
        rule3 = ctrl.Rule(self.edad['joven'] & self.imc['alto'], self.ejercicio_diario['moderado'])
        rule4 = ctrl.Rule(self.edad['adulto'] & self.imc['bajo'], self.ejercicio_diario['moderado'])
        rule5 = ctrl.Rule(self.edad['adulto'] & self.imc['normal'], self.ejercicio_diario['moderado'])
        rule6 = ctrl.Rule(self.edad['adulto'] & self.imc['alto'], self.ejercicio_diario['poco'])
        rule7 = ctrl.Rule(self.edad['mayor'] & self.imc['bajo'], self.ejercicio_diario['poco'])
        rule8 = ctrl.Rule(self.edad['mayor'] & self.imc['normal'], self.ejercicio_diario['poco'])
        rule9 = ctrl.Rule(self.edad['mayor'] & self.imc['alto'], self.ejercicio_diario['poco'])

        # Sistema de control
        self.ejercicio_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
        self.ejercicio = ctrl.ControlSystemSimulation(self.ejercicio_ctrl)

    def evaluar(self, edad_val, imc_val):
        self.ejercicio.input['edad'] = edad_val
        self.ejercicio.input['imc'] = imc_val
        self.ejercicio.compute()
        return self.ejercicio.output['ejercicio_diario']

# Base de Conocimiento
class BaseConocimiento:
    def __init__(self):
        self.datos_usuario = []
        self.reglas = []

    def agregar_datos_usuario(self, datos):
        self.datos_usuario.append(datos)

    def agregar_regla(self, regla):
        self.reglas.append(regla)

# Módulo de Adquisición de Conocimiento
class AdquisicionConocimiento:
    def capturar_conocimiento(self):
        pass  # Implementación futura

    def editar_conocimiento(self):
        pass  # Implementación futura

    def validar_conocimiento(self):
        pass  # Implementación futura

# Módulo de Gestión del Sistema
class GestionSistema:
    def __init__(self):
        self.registro_actividades = []

    def registrar_actividad(self, actividad):
        self.registro_actividades.append(actividad)

    def diagnosticar_y_corregir(self):
        pass  # Implementación futura

# Programa principal
def main():
    base_conocimiento = BaseConocimiento()
    motor_inferencia = MotorInferencia()
    adquisicion_conocimiento = AdquisicionConocimiento()
    gestion_sistema = GestionSistema()

    def calcular(edad_val, imc_val):
        return motor_inferencia.evaluar(edad_val, imc_val)

    interfaz = InterfazUsuario(calcular)
    interfaz.ejecutar()


# Variables difusas
edad = np.arange(0, 101, 1)
imc = np.arange(10, 41, 1)
ejercicio_diario = np.arange(0, 121, 1)

# Funciones de membresía para edad
edad_joven = fuzz.trimf(edad, [0, 0, 30])
edad_adulto = fuzz.trimf(edad, [20, 50, 80])
edad_mayor = fuzz.trimf(edad, [60, 100, 100])

# Funciones de membresía para IMC
imc_bajo = fuzz.trimf(imc, [10, 10, 18.5])
imc_normal = fuzz.trimf(imc, [18.5, 25, 30])  # Ajustado para incluir 25
imc_alto = fuzz.trimf(imc, [25, 40, 40])  # Ajustado para incluir 25

# Funciones de membresía para ejercicio diario
ejercicio_poco = fuzz.trimf(ejercicio_diario, [0, 0, 30])
ejercicio_moderado = fuzz.trimf(ejercicio_diario, [20, 60, 100])
ejercicio_mucho = fuzz.trimf(ejercicio_diario, [80, 120, 120])

# Visualización
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 12))

# Edad
ax0.plot(edad, edad_joven, 'b', linewidth=1.5, label='Joven')
ax0.plot(edad, edad_adulto, 'g', linewidth=1.5, label='Adulto')
ax0.plot(edad, edad_mayor, 'r', linewidth=1.5, label='Mayor')
ax0.set_title('Funciones de Membresía para la Edad')
ax0.legend()

# IMC
ax1.plot(imc, imc_bajo, 'b', linewidth=1.5, label='Bajo')
ax1.plot(imc, imc_normal, 'g', linewidth=1.5, label='Normal')
ax1.plot(imc, imc_alto, 'r', linewidth=1.5, label='Alto')
ax1.set_title('Funciones de Membresía para el IMC')
ax1.legend()

# Ejercicio Diario
ax2.plot(ejercicio_diario, ejercicio_poco, 'b', linewidth=1.5, label='Poco')
ax2.plot(ejercicio_diario, ejercicio_moderado, 'g', linewidth=1.5, label='Moderado')
ax2.plot(ejercicio_diario, ejercicio_mucho, 'r', linewidth=1.5, label='Mucho')
ax2.set_title('Funciones de Membresía para el Ejercicio Diario')
ax2.legend()

# Mostrar gráficos
for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()
plt.show()


if __name__ == "__main__":
    main()
