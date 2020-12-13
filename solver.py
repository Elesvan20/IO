'''
    Proyecto 2 - Investigacion de Operaciones
    Instituto Tecnologico de Costa Rica
    Estudiante: Kevin Ledezma Jimenez
    Profesor: Carlos Gamboa Venegas
    II Semestre 2020
'''
import sys

#Variables globales
problema = 0
algoritmo = 0

#Codigos posibles errores
POCOSPARAMETROS = -1
MUCHOSPARAMETROS = -2
ARCHIVONOENCONTRADO = -3

#Strings constantes
texto_ayuda = "\n========================Inicio de Mensaje de Ayuda========================\n" \
              "Comando para ejecutar el proyecto: \n " \
         "python3 solver.py [-h] PROBLEMA ALGORITMO ARCHIVO\n" \
         "Donde el parametro -h es opcional y PROBLEMA ALGORITMO ARCHIVO son obligatorios\n" \
         "Si -h es indicado, se muestra este mensaje junto a las instrucciones para ejecutar archivos\n" \
         "PROBLEMA es un valor de 1 o 2 indicando a resolver: el ejercicio 1 (contenedor) - ejercicio 2 (alineamiento) \n" \
         "ALGORITMO es un valor de 1 o 2 indicando el algoritmo a usar: 1 fuerza bruta - 2 programacion dinamica\n" \
         "ARCHIVO indica el archivo de entrada donde el programa toma los parametros del problema y procede a resolverlo con las configuraciones previas\n" \
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
          "NOTA: Siempre se ejecuta el metodo de scoring +1,-1,-2; Ademas, solo se utilizaran las letras A T C G\n" \
              "========================Fin de Mensaje de Ayuda========================\n"

error_archivo = "\nERROR: Parece que el archivo indicado no existe dentro de mi carpeta de ejecucion!!\n"
error_pocos_parametros = "\nError: Hacen falta parametros!\n Utilice el parametro -h para mostrar mas informacion\n"
error_muchos_parametros = "\nError: Se recibieron muchos parametros\n Utilice el parametro -h para mostrar mas informacion\n"
sintaxis_uso = "\nSintaxis: python3 solver.py [-h] PROBLEMA(1/2) ALGORITMO(1/2) ARCHIVO(nombre.txt)\n"

#Funcion recursiva para realizar el recorrido de mochila
def fuerza_bruta_auxiliar(mochila,valores,pesos,elementos):
    #Caso cuando no hay mas espacio en la mochila o bien, se acaban los elementos
    if (elementos == 0 or mochila == 0):
        return 0

    #Caso donde no tenemos espacio para este elemento
    if (pesos[elementos-1] > mochila):
        return fuerza_bruta_auxiliar(mochila, valores, pesos, elementos-1)

    #llamada recursiva sobre la lista
    else:
        return max(
                    #Caso agrego elemento a la mochila
                    valores[elementos-1] + fuerza_bruta_auxiliar(mochila-pesos[elementos-1],valores,pesos,elementos-1),

                    #Caso no agrego elemento a la mochila
                    fuerza_bruta_auxiliar(mochila,valores,pesos,elementos-1)
                )

'''
    Funcion encargada de modelar los datos
    para realizar la corrida de mochila
    siguiendo el algoritmo de fuerza bruta
'''
def fuerza_bruta(datos):
    print("Fuerza Bruta")
    mochila = int(datos[0][0])
    valores = []
    pesos = []

    #separar los items que nos dan
    for i in range(1,len(datos)):
        print(datos[i])
        #posicion 2 es la cantidad de items
        for j in range(int(datos[i][2])):
            pesos.append(int(datos[i][0]))
            valores.append(int(datos[i][1]))
    print("Mochila ",(mochila))
    print("arreglo de beneficio: ",valores)
    print("arreglo de pesos: ", pesos)

    return fuerza_bruta_auxiliar(mochila, valores, pesos, len(valores))

#Funcion auxiliar para el recorrido dinamico de la mochila
def programacion_dinamica_auxiliar(mochila,valores,pesos,elementos):

    #creamos la matriz a utilizar para el algoritmo
    matriz = [[0 for x in range(mochila + 1)] for x in range(elementos + 1)]

    #construccion de la matriz
    for i in range(elementos + 1):
        for j in range(mochila + 1):
            #Caso cuando no hay mas espacio en la mochila o bien, se acaban los elementos
            if i == 0 or j == 0:
                matriz[i][j] = 0

            #existe un elemento a ser agregado en la mochila
            elif pesos[i-1] <= j:
                matriz[i][j] = max(
                                # Caso agrego elemento a la mochila
                                valores[i - 1]+matriz[i-1][j-pesos[i-1]],

                                # Caso no agrego elemento a la mochila
                                matriz[i-1][j]
                                )
            #elemento no apto para mochila, avanzamos al siguiente
            else:
                matriz[i][j] = matriz[i-1][j]

    #regresamos el acumulado de la matriz
    return matriz[elementos][mochila]
'''
    Funcion encargada de modelar los datos
    para realizar la corrida de mochila
    siguiendo el algoritmo de programacion dinamica
'''
def programacion_dinamica(datos):
    mochila = int(datos[0][0])
    valores = []
    pesos = []

    #separar los items que nos dan
    for i in range(1,len(datos)):
        print(datos[i])
        #posicion 2 es la cantidad de items
        for j in range(int(datos[i][2])):
            pesos.append(int(datos[i][0]))
            valores.append(int(datos[i][1]))

    return programacion_dinamica_auxiliar(mochila, valores, pesos, len(pesos))

'''
CASO MOCHILA
    si -h es indicado, usar:
    PROBLEMA = sys.argv[2]  (INT)
    ALGORITMO = sys.argv[3] (STRING)
    ARCHIVO = sys.argv[4]   (STRING)

    si -h NO es indicado, usar
    PROBLEMA = sys.argv[1]  (INT)
    ALGORITMO = sys.argv[2] (STRING)
    ARCHIVO = sys.argv[3]   (STRING)
'''
def obtener_datos_mochila(despliegaH):

    if (despliegaH):
        # recupera los datos del archivo
        try:
            archivo = open(sys.argv[4])
            datos = archivo.read().strip()
            archivo.close()
        except FileNotFoundError:
            print(error_archivo)
            sys.exit(ARCHIVONOENCONTRADO)
        # elementos[0] seria el peso maximo del contenedor
        # los siguientes elementos serian los articulos
        elementos = []
        for line in datos.split('\n'):  # obtiene los datos del archivo
            elementos.append(line.split(","))
        return (elementos)
    else:
        try:
            # recupera los datos del archivo
            archivo = open(sys.argv[3])
            datos = archivo.read().strip()
            archivo.close()
        except FileNotFoundError:
            print(error_archivo)
            sys.exit(ARCHIVONOENCONTRADO)

        # elementos[0] seria el peso maximo del contenedor
        # los siguientes elementos serian los articulos
        elementos = []
        for line in datos.split('\n'):  # obtiene los datos del archivo
            elementos.append(line.split(","))
        return (elementos)

#    TODO
def obtener_datos_alineamiento(despliegaH):
    return "recuperar datos para ejercicio alineamiento"


'''
    Define la logica para
    obtener los parametros del archivo indicado    
'''
def obtener_parametros():
    global texto_ayuda
    global problema
    global algoritmo

    '''
        Casos especiales de entrada
    '''
    if (len(sys.argv) == 1):
        print("Error: Hacen falta parametros!\n Utilice el parametro -h para mostrar mas informacion")
        sys.exit(POCOSPARAMETROS)

    if (sys.argv[1] == "-h"):
        print(texto_ayuda)

        #casos especial de error
        if (len(sys.argv) < 5):
            print(sintaxis_uso)
            sys.exit(POCOSPARAMETROS)

        if (len(sys.argv) > 5):
            print(sintaxis_uso)
            sys.exit(MUCHOSPARAMETROS)

        #guardar globalmente el algoritmo a utilizar
        algoritmo = sys.argv[3]

        #condicional para recuperacion de datos
        if (sys.argv[2] == '1'):
            problema = 1    #indica que es problema de mochila
            return (obtener_datos_mochila(True))
        else:
            problema = 2    #indica que es problema de alineamiento
            return (obtener_datos_alineamiento(True))

    # casos especial de error
    if (len(sys.argv) < 4):
        print(error_pocos_parametros)
        sys.exit(POCOSPARAMETROS)
    if (len(sys.argv) > 4 and sys.argv[1] != "-h"):
        print(error_muchos_parametros)
        sys.exit(MUCHOSPARAMETROS)

    # Procesamiento directo una vez superado los casos especiales y sin usar -h

    # Guardar globalmente el algoritmo a utilizar
    algoritmo = sys.argv[2]

    # condicional para recuperacion de datos
    if (sys.argv[1] == '1'):
        problema = 1  # indica que es problema de mochila
        return (obtener_datos_mochila(False))
    else:
        problema = 2  # indica que es problema de alineamiento
        return (obtener_datos_alineamiento(False))

def main():
    datos = obtener_parametros()
    print("Ejecutando problema "+str(problema))
    print("Usando algoritmo: "+str(algoritmo))
    print("datos obtenidos: \n")
    print(datos)

    if (problema == 1): #Caso Mochila
        print("Valor algoritmo "+str(algoritmo))

        # Caso fuerza bruta
        if (algoritmo == '1'):
            fuerza_bruta(datos)

        # Caso programacion dinamica
        else:
            programacion_dinamica(datos)

    else:
        print("Caso alineamiento")



main()
'''
    Sintaxis
    python3 solver.py [-h] PROBLEMA ALGORITMO ARCHIVO
    
    python3 generator.py PROBLEMA ARCHIVO PARAMETROS
'''