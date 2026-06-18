def desconto(v, p):
    """
    Aplica um desconto percentual p sobre o valor v e retorna o valor com o desconto.

    :param v: Valor original (float/int)
    :param p: Percentual de desconto (float/int, ex: 10 para 10%)
    :return: Valor com o desconto aplicado
    """
    return v * (1 - p / 100)
