from ahp import media_geometrica, test_consistencia
from ahpsortdos import prioridad_global


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
    pesos = media_geometrica(matriz)
    test = test_consistencia(matriz)

    print("Pesos:", pesos)
    print("CR:", test["CR"], "Aceptable?:", test["aceptable"])

    #ahora calculo las prioridades globales de los perfiles centrales
    cp1 = [0.277, 0.261, 0.138, 0.259, 0.262]
    cp2 = [0.058, 0.075, 0.063, 0.066, 0.070]
    cp3 = [0.029, 0.032, 0.040, 0.034, 0.035]

    prioridad_global_cp1 = prioridad_global(cp1, pesos)
    prioridad_global_cp2 = prioridad_global(cp2, pesos)
    prioridad_global_cp3 = prioridad_global(cp3, pesos)

    print("Prioridad global cp1:", prioridad_global_cp1)
    print("Prioridad global cp2:", prioridad_global_cp2)
    print("Prioridad global cp3:", prioridad_global_cp3)

    limite_alta_media = (prioridad_global_cp1 + prioridad_global_cp2) / 2
    limite_media_baja = (prioridad_global_cp2 + prioridad_global_cp3) / 2

    expertos_pares_crimenes = [(0, 0.336), (20, 0.277), (41.2, 0.132), (82.4, 0.086), (100, 0.058), (123.6, 0.032), (160, 0.029), (164.8, 0.026), (206, 0.023)]
    expertos_pares_robos = [(0, 0.32), (5000, 0.261), (50914.4, 0.139), (95000, 0.075), (101828.8, 0.074), (152743.2, 0.047), (180000, 0.032), (203657.6, 0.031), (254572, 0.022)]
    expertos_pares_vehiculos = [(0, 0.459), (5000, 0.138), (7025.4, 0.124), (14050.8, 0.069), (19000, 0.063), (21076.2, 0.048), (27000, 0.04), (28101.6, 0.034), (35127, 0.026)]
    expertos_pares_orden_publico = [(0, 0.308), (300, 0.259), (764.8, 0.149), (1529.6, 0.071), (1800, 0.066), (2294.4, 0.06), (2500, 0.034), (3059.2, 0.032), (3824, 0.023)]
    expertos_pares_drogas = [(0, 0.385), (300, 0.262), (321.6, 0.112), (600, 0.07), (643.2, 0.062), (900, 0.035), (964.8, 0.033), (1286.4, 0.023), (1608, 0.018)]

    

if __name__ == "__main__":
    main()