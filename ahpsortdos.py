#dado un valor actual y dos puntos de referencia, interpola el peso correspondiente
def interpolar(valoract: float, pr_bajo: tuple[float, float], pr_alto: tuple[float, float]) -> float:
    valor_bajo, peso_bajo = pr_bajo
    valor_alto, peso_alto = pr_alto

    diferencia_valores = valor_alto - valor_bajo
    diferencia_pesos = peso_alto - peso_bajo

    distancia_valor = valoract - valor_bajo

    proporcio_valor = distancia_valor / diferencia_valores

    peso_interpolado = peso_bajo + (proporcio_valor * diferencia_pesos)

    return peso_interpolado

#calcula la prioridad local de un valor dado puntos de referencia
def prioridad_local(valor: float, puntos: list[tuple[float, float]]) -> float:
    for i in range(len(puntos) - 1):#para cada par de pr
        punto_bajo = puntos[i]
        punto_alto = puntos[i + 1]

        if punto_bajo[0] <= valor <= punto_alto[0]:
            return interpolar(valor, punto_bajo, punto_alto)

    return -1

#calcula prioridad global agregando usando los pesos
def prioridad_global(prioridades: list[float], pesos: list[float]) -> float:
    total = 0.0

    for i in range(len(pesos)):
        total += prioridades[i]*pesos[i]

    return total

#dado un diccionario de provincias y sus valores, calcula la prioridad global de cada provincia usando los pr de los expertos y los pesos de los criterios
def calcular_provincias(provincias: dict[str, list[float]], puntos_expertos: list[list[tuple[float, float]]], pesos: list[float]) -> dict[str, float]:
    resultados = {}

    for provincia, valores in provincias.items():#para cada provincia
        prioridades = []

        for i in range(len(valores)):#para cada criterio
            valor = valores[i]

            minimo = puntos_expertos[i][0][0]#valor minimo
            maximo = puntos_expertos[i][-1][0]#valos maximo
            if valor < minimo: #se trunca para que no sobrepase los limites
                valor = minimo
            elif valor > maximo:
                valor = maximo

            prioridad = prioridad_local(valor, puntos_expertos[i])
            prioridades.append(prioridad)

        puntuacion = prioridad_global(prioridades, pesos)

        resultados[provincia] = puntuacion

    return resultados

#dado un diccionario de provincias y sus puntuaciones globales, clasifica cada provincia en alta, media o baja segun los limites dados
def clasificar_provincias(prioridad_clases: list[float], resultados: dict[str, float]) -> dict[float, str]:
    clases = ["Alta", "Media", "Baja"]
    clasificacion = {}

    limite_alta_media = (prioridad_clases[0] + prioridad_clases[1]) / 2
    limite_media_baja = (prioridad_clases[1] + prioridad_clases[2]) / 2

    for provincia, puntuacion in resultados.items():#para cada provincia

        if puntuacion >= limite_alta_media:
            grupo_actual = clases[0]
        elif puntuacion >= limite_media_baja:
            grupo_actual = clases[1]
        else:
            grupo_actual = clases[2]

        clasificacion[provincia] = [puntuacion, grupo_actual]

    return clasificacion