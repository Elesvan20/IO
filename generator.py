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
import random

#Variables globales
problema = 0
parametros = ""
nombre_archivo = ""

#Codigos posibles errores
POCOSPARAMETROS = -1
MUCHOSPARAMETROS = -2
ERRORPARAMETROS = -6
ARCHIVONOENCONTRADO = -3
PROBLEMAINVALIDO = -4
ALGORITMOINVALIDO = -5


ERROR_ARCHIVO = "\nERROR: Parece que el archivo indicado no existe dentro de mi carpeta de ejecucion!!\n"
SINTAXIS_USO = "\nSintaxis: python3 generator.py PROBLEMA(1/2) ARCHIVO(nombre.txt) PARAMETROS (una sola instruccion, usar comillas)\n"

#pequeña funcion, se encarga de guardar correctamente los datos en un archivo de texto
def guardar_en_archivo(configuraciones):

    archivoSalida = open(nombre_archivo, "w")
    archivoSalida.write(configuraciones)
    print("Guardado de datos en archivo "+nombre_archivo +" Exitoso!")


'''
    Funcion encargada de interpretar los argumentos en consola
    y generar una estructura compatible con mochila tanto fuerza bruta como con P.D.
'''
def problema1_mochila():

    #verificamos que hayan suficientes parametros antes de continuar
    if (len(parametros) != 8):
        print("Error! Se recibieron parametros incorrectos para crear la configuracion de la mochila\n"
              "Parametros recibidos: ")
        print(parametros)
        print("Cantidad de parametros: "+str(len(parametros)))
        sys.exit(POCOSPARAMETROS)

    #Conversion de los parametros a formato necesario
    peso = int(parametros[0])
    elementos = int(parametros[1])
    minPeso = int(parametros[2])
    maxPeso = int(parametros[3])
    minBeneficio = int(parametros[4])
    maxBeneficio = int(parametros[5])
    minCantidad = int(parametros[6])
    maxCantidad = int(parametros[7])

    texto_archivo = str(peso)+"\n"

    for i in range(elementos):
        texto_archivo += str(random.randint(minPeso, maxPeso))+","+str(random.randint(minBeneficio, maxBeneficio))+","+str(random.randint(minCantidad, maxCantidad))+"\n"

    print("Configuraciones finales: ")
    print(texto_archivo)
    guardar_en_archivo(texto_archivo)

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

'''
    Función encargada de producir hileras aleatorias
    y guardaras en el archivo de salida especificado
    compuesto solo de letras A T C G
    Las letras estan representadas por numeros aleatorios entre 0 y 3 respectivamente
    siendo estos los indices de un arreglo
'''
def problema2_alineamiento():

    #verificacion de parametros correctos
    if (len(parametros) != 2):
        print("Error: Ha ingresado una cantidad distinta a 2 hileras para procesar!")
        print("Cantidad de Hileras ingresadas: "+str(len(parametros)))
        sys.exit(ERRORPARAMETROS)

    largoH1 = int(parametros[0])
    largoH2 = int(parametros[1])
    hilera1 = ""
    hilera2 = ""
    letras = ["A","T","C","G"]
    formato = "1,-1,-2\n"

    #Se requieren dos ciclos debido a que puede haber discrepancia de longitudes para cada hilera
    for i in range(largoH1):
        # asigna la letra aleatoria a la hilera1
        numeroLetra = random.randint(0,3)
        hilera1 += str(letras[numeroLetra])

    for i in range(largoH2):
        # asigna la letra aleatoria a la hilera2
        numeroLetra = random.randint(0, 3)
        hilera2 += str(letras[numeroLetra])

    #Conformamos el string de salida
    formato +=hilera1+"\n"+hilera2

    #guardamos el string en un archivo de salida
    guardar_en_archivo(formato)

########################################################################################################################
'''
    Funcion principal de obtener los parametros
    desde la consola a las variables para 
    configurar los ejercicios
'''
def generador_obtener_parametros():
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
    nombre_archivo = sys.argv[2]+".txt"

    #Guardamos en un arreglo los datos recibidos como parametros
    parametros = sys.argv[3].split(" ")

def main():
    #invocamos la obtencion de los datos
    generador_obtener_parametros()
    print("Usando algoritmo: " + str(problema))
    print("Nombre deseado para el archivo " + str(nombre_archivo))
    print("Parametros obtenidos: ", parametros)

    if problema == 1:
        problema1_mochila()

    else:
        problema2_alineamiento()

main()
'''
    Sintaxis
    python3 generator.py PROBLEMA ARCHIVO PARAMETROS
    
    Donde
    PROBLEMA es 1 (mochila) o 2 (alineamiento)
    ARCHIVO es el nombre donde se escribe la salida del ejercicio
    PARAMETROS todo lo requerido segun el ejercicio
'''