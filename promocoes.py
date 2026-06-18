def desconto(v, p):
    """
    Aplica um desconto percentual p sobre o valor v e retorna o valor com o desconto.

    :param v: Valor original (float/int)
    :param p: Percentual de desconto (float/int, ex: 10 para 10%)
    :return: Valor com o desconto aplicado
    """
    return v * (1 - p / 100)


def preco_final(v, p):
    """
    Calcula o preço final de um produto aplicando um desconto percentual.

    :param v: Valor original do produto (float/int).
    :param p: Percentual de desconto (float/int, ex: 10 para 10%).
    :return: O preço final após a aplicação do desconto.
    """
    return desconto(v, p)


def desconto_progressivo(valor):
    """
    Aplica desconto progressivo para valores gastos superiores a R$ 500.

    O percentual cresce linearmente de 0% (em R$ 500) até 30% (em R$ 2000),
    permanecendo limitado a 30% para valores maiores.

    :param valor: Valor total gasto (float/int).
    :return: Valor final com o desconto progressivo aplicado.
    """
    VALOR_MINIMO = 500
    VALOR_TETO = 2000
    DESCONTO_MAXIMO = 30

    if valor <= VALOR_MINIMO:
        return valor

    percentual = (valor - VALOR_MINIMO) / (VALOR_TETO - VALOR_MINIMO) * DESCONTO_MAXIMO
    percentual = min(percentual, DESCONTO_MAXIMO)

    return desconto(valor, percentual)
