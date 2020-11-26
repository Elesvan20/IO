'''
    Proyecto 2 - Investigacion de Operaciones
    Instituto Tecnologico de Costa Rica
    Estudiante: Kevin Ledezma Jimenez
    Profesor: Carlos Gamboa Venegas
    II Semestre 2020
'''
import sys

texto_ayuda = "========================Inicio de Mensaje de Ayuda========================\n" \
              "Comando para ejecutar el proyecto: \n " \
         "python3 solver.py [-h] PROBLEMA ALGORITMO ARCHIVO\n" \
         "Donde el parametro -h y PROBLEMA ALGORITMO ARCHIVO son obligatorios\n" \
         "Si -h es indicado, se muestra este mensaje junto a las instrucciones para ejecutar archivos\n" \
         "PROBLEMA es un valor de 1 o 2 indicando a resolver: el ejercicio 1 (contenedor) - ejercicio 2 (alineamiento) \n" \
         "ALGORITMO es un valor de 1 o 2 indicando el algoritmo a usar: 1 fuerza bruta - 2 programacion dinamica\n" \
         "ARCHIVO indica el archivo de entrada donde el programa toma los parametros del problema y procede a resolverlo con las configuraciones previas" \
         "Nota: Si no se indica un archivo, se ejecuta el problema predefinido en el sistema\n" \
         "=================================================================================\n" \
         "Tambien cuenta con un modulo generador de experimentos, cada experimento es una ejecucion configurable\n" \
         "Para ejecutar el generador, la instruccion es la siguiente:\n" \
              "python3 generator.py PROBLEMA ARCHIVO PARAMETROS\n" \
              "Donde:\n" \
              "PROBLEMA: Valor de 1 o 2 indica el problema de cual generar datos: 1-contenedor, 2-alineamiento\n" \
              "ARCHIVO: Nombre para el archivo de salida, donde se guardaran los datos (formato segun el ejercicio)\n" \
              "PARAMETROS: Parametros necesarios para cada problema, varian segun el problema" \
         "Para generar un experimento de tipo Mochila, la sintaxis es la siguiente: \n" \
         "python3 generator.py W N minPeso maxPeso minBeneficio maxBeneficio minCantidad maxCantidad\n" \
         "Donde:\n" \
              "W: Es el peso soportado por el contenedor\n" \
              "N: La cantidad de elementos\n" \
              "minPeso, maxPeso: Indica el valor minimo y maximo para asignar el peso aleatorio a los N elementos\n" \
              "minBeneficio, maxBeneficio: indica el valor minimo y maximo para asignar el beneficio aleatorio a los elementos \n" \
              "minCantidad, maxCantidad: Indica el valor mínimo y máximo para asignar la cantidad disponible de un elemento\n" \
         "=================================================================================\n" \
         "Para generar un experimento de tipo Hileras, la sintaxis es la siguiente: \n" \
              "python3 generator.py largoH1 largoH2\n" \
          "Donde:\n" \
              "largoH1 es el largo de la hilera1\n" \
              "largoH2 es el largo de la hilera2\n" \
          "NOTA: Siempre se ejecuta el metodo de scoring +1,-1,-2; Ademas, solo se utilizaran las letras A T C G" \
              "========================Fin de Mensaje de Ayuda========================\n"



def fuerza_bruta():
    print("Fuerza Bruta")


def programacion_dinamica():
    print("progra dinamica")


#
#    Obtiene los parametros del archivo indicado, en caso de recibir un archivo de entrada
#
#
def obtener_parametros():
    global texto_ayuda
    if (sys.argv[1] == "-h"):
        print(texto_ayuda)

def main():
    obtener_parametros()
    print("Hello World")

main()
'''
    Sintaxis
    python3 solver.py [-h] PROBLEMA ALGORITMO ARCHIVO
    
    python3 generator.py PROBLEMA ARCHIVO PARAMETROS
'''