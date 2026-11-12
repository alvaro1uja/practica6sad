from ahp import pesosporautovalor, test_consistencia
from ahpsortdos import prioridad_global, prioridad_local, calcular_provincias, clasificar_provincias, mostrar_clasificacion
from openpyxl import load_workbook
import csv

def exportar_clasificacion(nombre_archivo, clasificacion):
    equivalencias = {
        "Alicante/Alacant": "Alacant/Alicante",
        "Castellón/Castelló": "Castelló/Castellón",
        "Valencia/València": "València/Valencia",
        "Coruña (A)": "A Coruña",
        "Coruña, A": "A Coruña",
        "Balears (Illes)": "Illes Balears",
        "Balears, Illes": "Illes Balears",
        "Rioja (La)": "La Rioja",
        "Rioja, La": "La Rioja",
    }

    with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["provincia", "puntuacion", "grupo"])

        for provincia, resultado in clasificacion.items():
            nombre_mapa = equivalencias.get(provincia, provincia)
            escritor.writerow([nombre_mapa, resultado[0], resultado[1]])

def main():
    #Ejercicio 1: Calcular los pesos de los criterios y calcular validez (CR concistencia)
    print("Ejercicio 1")
    #Reutilizare algunas funciones de la practica 5
    #Orden: crimenes, robos, vehiculos, orden publico y drogas
    matriz = [[1, 5, 3, 7, 3],
            [1/5, 1, 3, 1/2, 1/4],
            [1/3, 1/3, 1, 1/5, 1/5],
            [1/7, 2, 5, 1, 1/5],
            [1/3, 4, 5, 5, 1]]
    pesos = pesosporautovalor(matriz)
    test = test_consistencia(matriz)

    print("Pesos:", pesos)
    print("CR:", test["CR"], "Aceptable?:", test["aceptable"])
    print()

    #ahora calculo las prioridades globales de los perfiles centrales
    cp1 = [0.277, 0.261, 0.138, 0.259, 0.262]
    cp2 = [0.058, 0.075, 0.063, 0.066, 0.070]
    cp3 = [0.029, 0.032, 0.040, 0.034, 0.035]

    prioridad_global_cp1 = prioridad_global(cp1, pesos)
    prioridad_global_cp2 = prioridad_global(cp2, pesos)
    prioridad_global_cp3 = prioridad_global(cp3, pesos)
    lista_cps = [prioridad_global_cp1, prioridad_global_cp2, prioridad_global_cp3]

    print("Prioridad global cp1:", prioridad_global_cp1)
    print("Prioridad global cp2:", prioridad_global_cp2)
    print("Prioridad global cp3:", prioridad_global_cp3)
    print()

    #ahora cargamos los pr de los expertos
    expertos_pares_crimenes = [(0, 0.336), (20, 0.277), (41.2, 0.132), (82.4, 0.086), (100, 0.058), (123.6, 0.032), (160, 0.029), (164.8, 0.026), (206, 0.023)]
    expertos_pares_robos = [(0, 0.32), (5000, 0.261), (50914.4, 0.139), (95000, 0.075), (101828.8, 0.074), (152743.2, 0.047), (180000, 0.032), (203657.6, 0.031), (254572, 0.022)]
    expertos_pares_vehiculos = [(0, 0.459), (5000, 0.138), (7025.4, 0.124), (14050.8, 0.069), (19000, 0.063), (21076.2, 0.048), (27000, 0.04), (28101.6, 0.034), (35127, 0.026)]
    expertos_pares_orden_publico = [(0, 0.308), (300, 0.259), (764.8, 0.149), (1529.6, 0.071), (1800, 0.066), (2294.4, 0.06), (2500, 0.034), (3059.2, 0.032), (3824, 0.023)]
    expertos_pares_drogas = [(0, 0.385), (300, 0.262), (321.6, 0.112), (600, 0.07), (643.2, 0.062), (900, 0.035), (964.8, 0.033), (1286.4, 0.023), (1608, 0.018)]
    lista_global_expertos=[expertos_pares_crimenes, expertos_pares_robos, expertos_pares_vehiculos, expertos_pares_orden_publico, expertos_pares_drogas]

    #cargamos los datos de las provincias
    provincias = {"Almeria": [23, 17284, 2101, 387, 267],
                "Cadiz": [61, 26571, 3945, 722, 818],
                "Cordoba": [20, 14508, 1691, 219, 148],
                "Granada": [32, 19139, 2299, 368, 622],
                "Huelva": [8, 11222, 1409, 156, 139],
                "Jaen": [17, 7548, 718, 175, 129],
                "Malaga": [58, 46137, 6377, 830, 934],
                "Sevilla": [86, 52849, 9662, 716, 415]}

    #calculamos las prioridades globales de cada provincia
    resultados = calcular_provincias(provincias, lista_global_expertos, pesos)
    clasificacion = clasificar_provincias(lista_cps, resultados)
    print("Prioridades globales de cada provincia SIN NORMALIZAR POR HABITANTES")
    for provincia, resultado in clasificacion.items():
        print(provincia, round(resultado[0], 4), resultado[1])
    

    #Ejercicio 2
    #ahora repetir pero con los datos normalizados por los habitantes de cada provincia
    print()
    print("###############################")
    print()
    print("Ejercicio 2")
    habitantes = {
                "Almeria": 731792,
                "Cadiz": 1245960,
                "Cordoba": 776789,
                "Granada": 921338,
                "Huelva": 525835,
                "Jaen": 627190,
                "Malaga": 1695651,
                "Sevilla": 1947852}
    #primero se normalizan
    provincias_normalizadas = {}
    for provincia, valores in provincias.items():
        tasasnorm=[]
        for valor in valores:
            tasaact = valor/habitantes[provincia]*10000
            tasasnorm.append(tasaact)
        provincias_normalizadas[provincia] = tasasnorm

    #introducimos los pr de los expertos normalizados
    expertos_pares_crimenes_norm = [(0, 0.34), (0.10, 0.13), (0.20, 0.09), (0.26, 0.05), (0.30, 0.03), (0.34, 0.03), (0.39, 0.03), (0.41, 0.03), (0.49, 0.02)]
    expertos_pares_robos_norm = [(0, 0.32), (56.59, 0.14), (113.18, 0.07), (169.77, 0.05), (194.29, 0.04), (215.32, 0.03), (226.35, 0.03), (261.32, 0.03), (282.94, 0.02)]
    expertos_pares_vehiculos_norm = [(0, 0.46), (9.96, 0.12), (19.93, 0.07), (22.95, 0.06), (28.44, 0.05), (29.89, 0.05), (36.20, 0.04), (39.85, 0.03), (49.82, 0.03)]
    expertos_pares_orden_publico_norm = [(0, 0.31), (1.17, 0.15), (2.33, 0.07), (2.87, 0.07), (3.50, 0.06), (3.86, 0.05), (4.66, 0.03), (5.32, 0.03), (5.83, 0.02)]
    expertos_pares_drogas_norm = [(0, 0.39), (1.36, 0.11), (2.06, 0.09), (2.73, 0.06), (3.23, 0.05), (4.09, 0.03), (5.45, 0.02), (6.25, 0.02), (6.81, 0.02)]
    puntos_normalizados = [expertos_pares_crimenes_norm, expertos_pares_robos_norm, expertos_pares_vehiculos_norm, expertos_pares_orden_publico_norm, expertos_pares_drogas_norm]
    
    #cargamos los perfiles centrales normalizados
    cp1_norm = [0.05, 0.04, 0.06, 0.07, 0.09]
    cp2_norm = [0.03, 0.03, 0.05, 0.05, 0.05]
    cp3_norm = [0.03, 0.03, 0.04, 0.03, 0.02]

    global_cp1_norm = prioridad_global(cp1_norm, pesos)
    global_cp2_norm = prioridad_global(cp2_norm, pesos)
    global_cp3_norm = prioridad_global(cp3_norm, pesos)
    lista_cps_norm = [global_cp1_norm, global_cp2_norm, global_cp3_norm]

    #calculamos las prioridades globales de cada provincia de nuevo
    resultados_norm = calcular_provincias(provincias_normalizadas, puntos_normalizados, pesos)
    clasificacion_norm = clasificar_provincias(lista_cps_norm, resultados_norm)
    print("Prioridades globales de cada provincia normalizadas por habitantes")
    for provincia, resultado in clasificacion_norm.items():
        print(provincia, round(resultado[0], 4), resultado[1])
    
    print()

    #Ejercicio 3
    #repetir el proceso pero ahora con los datos del excel de toda espana 2017
    print()
    print("###############################")
    print()
    
    print("Ejercicio 3")
    #primero abrimos el excel y cargamos sus datos en un diccionario
    archivo = load_workbook("Datos_nacionales_2017_por_10000_ES.xlsx", data_only=True)
    hoja = archivo.active

    provincias_espana = {}
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        provincia = fila[0]
        valores = list(fila[1:6])
        provincias_espana[provincia] = valores

    archivo.close()

    #ahora cargamos los pr de los expertos
    expertos_pares_crimenes_ej3 = [(0, 0.336), (0.15, 0.132), (0.30, 0.086), (0.44, 0.032), (0.59, 0.026), (0.74, 0.023)]
    expertos_pares_robos_ej3 = [(0, 0.32), (81.29, 0.139), (162.59, 0.074), (243.88, 0.047), (325.17, 0.031), (406.46, 0.022)]
    expertos_pares_vehiculos_ej3 = [(0, 0.459), (10.80, 0.124), (21.59, 0.069), (32.39, 0.048), (43.19, 0.034), (53.98, 0.026)]
    expertos_pares_orden_publico_ej3 = [(0, 0.308), (1.18, 0.149), (2.35, 0.071), (3.53, 0.06), (4.70, 0.032), (5.88, 0.023)]
    expertos_pares_drogas_ej3 = [(0, 0.385), (1.36, 0.112), (2.73, 0.062), (4.09, 0.033), (5.45, 0.023), (6.81, 0.018)]
    expertos_pares_ej3 = [expertos_pares_crimenes_ej3, expertos_pares_robos_ej3, expertos_pares_vehiculos_ej3, expertos_pares_orden_publico_ej3, expertos_pares_drogas_ej3]

    #ahora cargamos los perfiles centrales
    cp1_ej3 = [0.125, 0.101, 0.229, 0.067, 0.109]
    cp2_ej3 = [0.099, 0.068, 0.109, 0.061, 0.089]
    cp3_ej3 = [0.061, 0.042, 0.051, 0.036, 0.061]

    prglobal_cp1_ej3 = prioridad_global(cp1_ej3, pesos)
    prglobal_cp2_ej3 = prioridad_global(cp2_ej3, pesos)
    prglobal_cp3_ej3 = prioridad_global(cp3_ej3, pesos)
    lista_cps_ej3 = [prglobal_cp1_ej3, prglobal_cp2_ej3, prglobal_cp3_ej3]

    #ahora calculamos las prioridades globales de cada provincia de nuevo
    resultados_2017 = calcular_provincias(provincias_espana, expertos_pares_ej3, pesos)
    clasificacion_2017 = clasificar_provincias(lista_cps_ej3, resultados_2017)
    mostrar_clasificacion(clasificacion_2017)

    #Ejercicio 4
    #repetimos con los datos del excel de 2023
    print()
    print("###############################")
    print()
    print("Ejercicio 4")
    #primero cargo los datos del excel a un diccionario
    archivo = load_workbook("Datos_nacionales_2023_por_10000_ES.xlsx", data_only=True)
    hoja = archivo["Datos 2023"]

    provincias_2023 = {}
    for fila in hoja.iter_rows(min_row=2, values_only=True):#para cada fila
        provincia = fila[0]

        #Igualo nombres como "Palmas, Las" y "Palmas (Las)"
        if ", " in provincia:
            partes = provincia.split(", ")
            provincia = partes[0] + " (" + partes[1] + ")"

        valores = list(fila[7:12])#solo tomamos los normalizados por poblacion
        provincias_2023[provincia] = valores
    archivo.close()

    #calculamos las prioridades y clasificamos las provincias de 2023 usando los mismos pr de los expertos y los mismos perfiles centrales que ej3
    resultados_2023 = calcular_provincias(provincias_2023, expertos_pares_ej3, pesos)
    clasificacion_2023 = clasificar_provincias(lista_cps_ej3, resultados_2023)
    mostrar_clasificacion(clasificacion_2023)
    
    #comparamos la clasificacion de 2017 y 2023 para ver si ha cambiado
    print("Comparativa de clasificaciones entre 2017 y 2023")
    print("Provincia | Seguridad 2017 | Seguridad 2023")

    clases = ["Alta", "Media", "Baja"]
    matriz_cambios = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  

    for provincia, resultado in clasificacion_2017.items():
        grupo_2017 = resultado[1]
        grupo_2023 = clasificacion_2023[provincia][1]

        print(provincia, "|", grupo_2017, "|", grupo_2023)

        fila = clases.index(grupo_2017)
        columna = clases.index(grupo_2023)
        matriz_cambios[fila][columna] += 1

    print()
    print("Filas: 2017, Columnas: 2023")
    print("Grupo | Alta | Media | Baja")

    for i in range(len(clases)):
        print(clases[i], "|", matriz_cambios[i][0], "|", matriz_cambios[i][1], "|", matriz_cambios[i][2])


    #exportar las clasificaciones de 2017 y 2023
    exportar_clasificacion("clasificacion_2017.csv", clasificacion_2017)
    exportar_clasificacion("clasificacion_2023.csv", clasificacion_2023)

if __name__ == "__main__":
    main()