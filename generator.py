'''
    Proyecto 2 - Investigacion de Operaciones
    Estudiante: Kevin Ledezma Jimenez
    Profesor: Carlos Gamboa Venegas
    II Semestre 2020
'''

#
#Input:
#    python3 generator.py W N minPeso maxPeso minBeneficio maxBeneficio minCantidad maxCantidad
#    donde
#    W = peso maximo de la mochila
#    N = cantidad maxima de objetos
#Output:
#    beneficio
#    articulo i, cantidad
#    articulo i+1, cantidad
#    .
#    .
#    .
#    articulo n, cantidad
#

import sys

#Variables globales
problema = 0
parametros = ""
nombre_archivo = ""

#Codigos posibles errores
POCOSPARAMETROS = -1
MUCHOSPARAMETROS = -2
ARCHIVONOENCONTRADO = -3
PROBLEMAINVALIDO = -4
ALGORITMOINVALIDO = -5


ERROR_ARCHIVO = "\nERROR: Parece que el archivo indicado no existe dentro de mi carpeta de ejecucion!!\n"
SINTAXIS_USO = "\nSintaxis: python3 generator.py PROBLEMA(1/2) ARCHIVO(nombre.txt) PARAMETROS (una sola instruccion, usar comillas)\n"

def problema1_mochila():
    print("Resuelvo el problema de la mochila")


#
#Sintaxis:
#python3 generator.py largoH1 largoH2
#
#♦♦♦SOLO UTILIZAR LETRAS A T C G♦♦♦
#
#
#
#Output:
#    Tabla de resultados [matriz]
#
#    Puntaje Final: -2
#    Hilera1: ATTGTGATC__C
#    Hilera2: _TTG_CATCGGC


def problema2_alineamiento():
    print("Resuelvo el problema de alineamiento de secuencias")

########################################################################################################################
'''
    Funcion principal de obtener los parametros
    desde la consola a las variables para 
    configurar los ejercicios
'''
def obtener_parametros():
    global problema, parametros, nombre_archivo
    '''
        Casos especiales de entrada
    '''
    # casos especiales de error
    if (len(sys.argv) < 4):
        print("Muchos argumentos recibidos: "+str(len(sys.argv))+"\n"+SINTAXIS_USO)
        sys.exit(POCOSPARAMETROS)

    if (len(sys.argv) > 4):
        print("Muchos argumentos recibidos: "+str(len(sys.argv))+"\n"+SINTAXIS_USO)
        sys.exit(MUCHOSPARAMETROS)

    #Se captura el parametro introducido en consola como configuracion de problema
    problema = int(sys.argv[1])

    #Verificamos que sea un valor permitido
    if (1 > problema or problema > 2):
        print("ERROR: Valor de problema invalido! Debe ser 1 o 2 \n"
              "Se recibio un "+str(problema))
        sys.exit(PROBLEMAINVALIDO)

    # Guardamos el nombre para el futuro archivo de texto
    nombre_archivo = sys.argv[2]

    #Guardamos en un arreglo los datos recibidos como parametros
    parametros = sys.argv[3].split(" ")

def main():
    #invocamos la obtencion de los datos
    obtener_parametros()
    print("Usando algoritmo: " + str(problema))
    print("Nombre deseado para el archivo " + str(nombre_archivo))
    print("Parametros obtenidos: ", parametros)


main()
'''
    Sintaxis
    python3 generator.py PROBLEMA ARCHIVO PARAMETROS
    
    Donde
    PROBLEMA es 1 (mochila) o 2 (alineamiento)
    ARCHIVO es el nombre donde se escribe la salida del ejercicio
    PARAMETROS todo lo requerido segun el ejercicio
'''