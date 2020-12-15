'''
    Proyecto 2 - Investigacion de Operaciones
    Instituto Tecnologico de Costa Rica
    Estudiante: Kevin Ledezma Jimenez
    Profesor: Carlos Gamboa Venegas
    II Semestre 2020
'''
import sys
import time

#Variables globales
problema = 0
algoritmo = 0
GAP_PENALTY = -2
MATCH = 1
MISSMATCH = -1
mejor_hilera1 = ""
mejor_hilera2 = ""
tiempo_inicio = 0

#Codigos posibles errores
POCOSPARAMETROS = -1
MUCHOSPARAMETROS = -2
ARCHIVONOENCONTRADO = -3
PROBLEMAINVALIDO = -4
ALGORITMOINVALIDO = -5
ERRORMEMORIA = -6

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
ERROR_ARCHIVO = "\nERROR: Parece que el archivo indicado no existe dentro de mi carpeta de ejecucion!!\n"
ERROR_POCOS_PARAMETROS = "\nError: Hacen falta parametros!\n Utilice el parametro -h para mostrar mas informacion\n"
ERROR_MUCHOS_PARAMETROS = "\nError: Se recibieron muchos parametros\n Utilice el parametro -h para mostrar mas informacion\n"
SINTAXIS_USO = "\nSintaxis: python3 solver.py [-h] PROBLEMA(1/2) ALGORITMO(1/2) ARCHIVO(nombre.txt)\n"


#Pequeña funcion auxiliar para imprimir matrices de manera "ordenada"
def imprimirMatriz(matriz):
    for i in range(len(matriz)):
        print(matriz[i])

#funcion auxiliar para separar strings en caracteres
def split(string):
    return [char for char in string]

#======================================================================================================================

#Funcion recursiva para realizar el recorrido de mochila
def mochila_fuerza_bruta_auxiliar(mochila, valores, pesos, elementos):
    #Caso cuando no hay mas espacio en la mochila o bien, se acaban los elementos
    if (elementos == 0 or mochila == 0):
        return 0

    #Caso donde no tenemos espacio para este elemento
    if (pesos[elementos-1] > mochila):
        return mochila_fuerza_bruta_auxiliar(mochila, valores, pesos, elementos - 1)

    #llamada recursiva sobre la lista
    else:
        return max(
                    #Caso agrego elemento a la mochila
            valores[elementos-1] + mochila_fuerza_bruta_auxiliar(mochila - pesos[elementos - 1], valores, pesos, elementos - 1),

                    #Caso no agrego elemento a la mochila
                    mochila_fuerza_bruta_auxiliar(mochila, valores, pesos, elementos - 1)
                )

'''
    Funcion encargada de modelar los datos
    para realizar la corrida de mochila
    siguiendo el algoritmo de fuerza bruta
'''
def mochila_fuerza_bruta(datos):
    print("Fuerza Bruta")
    mochila = int(datos[0][0])
    valores = []
    pesos = []

    #separar los items que nos dan
    for i in range(1,len(datos)):
        #posicion 2 es la cantidad de items
        for j in range(int(datos[i][2])):
            pesos.append(int(datos[i][0]))
            valores.append(int(datos[i][1]))

    return mochila_fuerza_bruta_auxiliar(mochila, valores, pesos, len(valores))

#Funcion auxiliar para el recorrido dinamico de la mochila
def mochila_programacion_dinamica_auxiliar(mochila, valores, pesos, elementos):

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
    #imprimirMatriz(matriz)
    #regresamos el acumulado de la matriz
    return matriz[elementos][mochila]
'''
    Funcion encargada de modelar los datos
    para realizar la corrida de mochila
    siguiendo el algoritmo de programacion dinamica
'''
def mochila_programacion_dinamica(datos):
    mochila = int(datos[0][0])
    valores = []
    pesos = []

    #separar los items que nos dan
    for i in range(1,len(datos)):
        #posicion 2 es la cantidad de items
        for j in range(int(datos[i][2])):
            pesos.append(int(datos[i][0]))
            valores.append(int(datos[i][1]))

    return mochila_programacion_dinamica_auxiliar(mochila, valores, pesos, len(pesos))

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
    lineas = []
    if (despliegaH):
        # recupera los datos del archivo
        try:
            archivo = open(sys.argv[4])
            datos = archivo.read().strip()
            archivo.close()
        except FileNotFoundError:
            print(ERROR_ARCHIVO+archivo)
            sys.exit(ARCHIVONOENCONTRADO)

        # los siguientes elementos serian los articulos
        for line in datos.split('\n'):  # obtiene los datos del archivo
            lineas.append(line.split(","))
        return (lineas)
    else:
        try:
            # recupera los datos del archivo
            archivo = open(sys.argv[3])
            datos = archivo.read().strip()
            archivo.close()
        except FileNotFoundError:
            print(ERROR_ARCHIVO+archivo)
            sys.exit(ARCHIVONOENCONTRADO)

        # los siguientes elementos serian los articulos
        for line in datos.split('\n'):  # obtiene los datos del archivo
            lineas.append(line.split(","))
        return (lineas)

#======================================================================================================================
#funcion auxiliar para devolver una lista de permutaciones sin repeticiones, dado un string
def permutaciones(lista):
    permas = [[]]
    for i in lista:
        nueva_perma = []
        for perma in permas:
            for j in range(len(perma) + 1):
                nueva_perma.append(perma[:j] + [i] + perma[j:])
                # evita la duplicacion
                if j < len(perma) and perma[j] == i: break
        permas = nueva_perma
    return permas


#Funcion auxiliar que calcular el puntaje de dos strings siguiendo el scoring y lo retorna
def calcular_puntaje(subhilera1, subhilera2):

    puntaje = 0
    for i in range(len(subhilera1)):

        if subhilera1[i] == "*" or subhilera2[i] == "*":
            puntaje += GAP_PENALTY
        elif subhilera1[i] == subhilera2[i]:
            puntaje += MATCH
        else:
            print("MISSMATCH -1")

    return puntaje

'''
    Funcion encargada de cruzar todas las posibles combinaciones
    entre ambas listas, recordando cual es el mejor puntaje y devolviendolo
    como valor de retorno
'''
def cruzar_listas(listas1, listas2):
    global mejor_hilera1, mejor_hilera2

    #ponemos un negativo grande para que sea sobreescrito siempre
    mayor_puntaje = -10000

    #ciclo para recorrer ambas listas
    for i in range(len(listas1)):
        for j in range(len(listas2)):

            puntaje_calculado = calcular_puntaje(listas1[i], listas2[j])

            #mantendremos este print ya que sirve bastante para visualizar los datos de la corrida
            #print("Puntaje obtenido de la corrida "+listas1[i] + " "+listas2[j] + " es: "+str(puntaje_calculado))

            #caso especial de la primera asignacion
            if (mayor_puntaje == -10000):
                mayor_puntaje = puntaje_calculado
                mejor_hilera1 = str(listas1[i])
                mejor_hilera2 = str(listas2[j])

            #verificamos si tenemos nuevo mejor match
            elif (puntaje_calculado > mayor_puntaje):
                mejor_hilera1 = str(listas1[i])
                mejor_hilera2 = str(listas2[j])
                mayor_puntaje = puntaje_calculado

    return mayor_puntaje

'''
    Funcion encargada de realizar el recorrido de alineamiento en fuerza bruta
'''
def alineamiento_fuerza_bruta(datos):
    global tiempo_inicio

    #se ponen en mayusculas para evitar incongruencias a la hora de comparar caracteres
    hilera1 = datos[1][0].upper()
    hilera2 = datos[2][0].upper()

    lenh1 = len(hilera1)
    lenh2 = len(hilera2)
    diferencia = lenh1 + lenh2

    hilera1 += ("*"*abs(diferencia - lenh1))
    hilera2 += ("*" * abs(diferencia - lenh2))
    print("Listas ingresadas: ")
    print(hilera1)
    print(hilera2)

    #Se agrega manejo de excepcion ya que se sabe, que el algoritmo es lento en casos muy grandes
    try:
        lista_permutaciones_hilera1 = (list(map(lambda x: "".join(x), permutaciones(hilera1))))[-diferencia:]
        lista_permutaciones_hilera2 = (list(map(lambda x: "".join(x), permutaciones(hilera2))))[-diferencia:]
    except MemoryError as error:
        print("Las hileras son demasiado grandes y ya me quedé sin memoria!!")
        print("MEMORY ERROR")
        print("¡Programa Finalizado!\nSegundos transcurridos", (time.time() - tiempo_inicio))
        sys.exit(ERRORMEMORIA)

    print("Listas permutadas obtenidas:")
    print(lista_permutaciones_hilera1)
    print(lista_permutaciones_hilera2)

    mejor_puntaje = cruzar_listas(lista_permutaciones_hilera1, lista_permutaciones_hilera2)
    return(mejor_puntaje)

'''
    Funcion encarga de obtener los datos del archivo de texto
    y retornarlos en un arreglo para su posterior uso
'''
def obtener_datos_alineamiento(despliegaH):
    lineas = []
    # Caso donde se despliega ayuda
    if (despliegaH):
        # recupera los datos del archivo
        try:
            archivo = open(sys.argv[4])
            datos = archivo.read().strip()
            archivo.close()
        except FileNotFoundError:
            print(ERROR_ARCHIVO+archivo)
            sys.exit(ARCHIVONOENCONTRADO)

        # los siguientes elementos serian los articulos
        for line in datos.split('\n'):  # obtiene los datos del archivo
            lineas.append(line.split(","))
        return (lineas)

    # Caso no se despliega ayuda
    else:
        try:
            # recupera los datos del archivo
            archivo = open(sys.argv[3])
            datos = archivo.read().strip()
            archivo.close()
        except FileNotFoundError:
            print(ERROR_ARCHIVO+archivo)
            sys.exit(ARCHIVONOENCONTRADO)

        # los siguientes elementos serian las hileras
        for line in datos.split('\n'):  # obtiene los datos del archivo
            lineas.append(line.split(","))
        return (lineas)


#======================================================================================================================
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
            print(SINTAXIS_USO)
            sys.exit(POCOSPARAMETROS)

        if (len(sys.argv) > 5):
            print(SINTAXIS_USO)
            sys.exit(MUCHOSPARAMETROS)

        #guardar globalmente el algoritmo a utilizar
        algoritmo = int(sys.argv[3])

        #condicional para recuperacion de datos
        if (sys.argv[2] == "1"):
            problema = 1    #indica que es problema de mochila
            return (obtener_datos_mochila(True))
        elif sys.argv[2] == "2":
            problema = 2    #indica que es problema de alineamiento
            return (obtener_datos_alineamiento(True))
        else:
            print("Error: No se ha seleccionado un problema valido a ejecutar (1-2)\n"
                  "valor recibido: " + str(sys.argv[2]))
            sys.exit(PROBLEMAINVALIDO)

    # casos especial de error
    if (len(sys.argv) < 4):
        print(ERROR_POCOS_PARAMETROS)
        sys.exit(POCOSPARAMETROS)
    if (len(sys.argv) > 4 and sys.argv[1] != "-h"):
        print(ERROR_MUCHOS_PARAMETROS)
        sys.exit(MUCHOSPARAMETROS)

    # Procesamiento directo una vez superado los casos especiales y sin usar -h

    # Guardar globalmente el algoritmo a utilizar
    algoritmo = int(sys.argv[2])

    # condicional para recuperacion de datos
    if (sys.argv[1] == "1"):
        problema = 1  # indica que es problema de mochila
        return (obtener_datos_mochila(False))
    elif sys.argv[1] == "2":
        problema = 2  # indica que es problema de alineamiento
        return (obtener_datos_alineamiento(False))
    else:
        print("Error: No se ha seleccionado un problema valido a ejecutar (1-2)\n"
              "valor recibido: " + str(sys.argv[1]))
        sys.exit(PROBLEMAINVALIDO)


def main():
    global problema, algoritmo, mejor_hilera1, mejor_hilera2
    datos = obtener_parametros()
    #print("Ejecutando problema "+str(problema))
    #print("Usando algoritmo: "+str(algoritmo))
    #print("datos obtenidos: ", datos)

    # Caso Mochila
    if (problema == 1):

        # Caso fuerza bruta
        if (algoritmo == 1):
            print("Ejecutando Fuerza Bruta para Mochila")
            print("Resultado: ", mochila_fuerza_bruta(datos))

        # Caso programacion dinamica
        elif (algoritmo == 2):
            print("Ejecutando Programacion Dinamica para Mochila")
            print("Resultado: ", mochila_programacion_dinamica(datos))

        # Contencion algoritmo invalido
        else:
            print("Se ha recibido una opcion de algoritmo invalida (1-2)\n"
                  "Algoritmo recibido: ", str(algoritmo))
            sys.exit(ALGORITMOINVALIDO)

    elif (problema == 2):
        if (algoritmo == 1):
            print("Caso alineamiento fuerza bruta")
            print("Resultado: \n"+str(alineamiento_fuerza_bruta(datos)))
            print("Hileras:")
            print(mejor_hilera1)
            print(mejor_hilera2)
        else:
            print("Caso alineamiento Progra dinamica")

    else:
        print("Error: No se ha seleccionado un problema valido a ejecutar (1-2)\n"
              "valor recibido: " + str(problema))
        sys.exit(PROBLEMAINVALIDO)


#cronometro para calcular la ejecucion del proyecto
tiempo_inicio = time.time()
main()
print("¡Programa Finalizado!\nSegundos transcurridos", (time.time() - tiempo_inicio))