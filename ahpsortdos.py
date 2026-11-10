#dado un valor actual y dos puntos de referencia, interpola el peso correspondiente
def interpolar(valoract: float, pr_bajo: tuple[float, float], pr_alto: tuple[float, float]):
    valor_bajo, peso_bajo = pr_bajo
    valor_alto, peso_alto = pr_alto

    diferencia_valores = valor_alto - valor_bajo
    diferencia_pesos = peso_alto - peso_bajo

    distancia_valor = valoract - valor_bajo

    proporcio_valor = distancia_valor / diferencia_valores

    peso_interpolado = peso_bajo + (proporcio_valor * diferencia_pesos)

    return peso_interpolado