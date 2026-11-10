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