from ahp import media_geometrica, test_consistencia


def main():
    #Ejercicio 1: Calcular los pesos de los criterios y calcular validez (CR concistencia)
    #Reutilizare las funciones de la practica 5
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


if __name__ == "__main__":
    main()