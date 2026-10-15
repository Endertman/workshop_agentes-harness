MAX_ITERACIONES = 15


def revisar_limites(iteracion):
    if iteracion > MAX_ITERACIONES:
        return f"Límite: se alcanzó el máximo de {MAX_ITERACIONES} iteraciones"
    return None
