import os


def revisar_login(navegador):
    if not navegador.pide_login():
        return None

    usuario = os.getenv("HN_USERNAME")
    clave = os.getenv("HN_PASSWORD")
    if not usuario or not clave:
        return "[harness] Llegaste al login, pero faltan HN_USERNAME y HN_PASSWORD en .env"

    print("[harness] El agente llegó al login: inicio sesión por él")
    navegador.escribir("input[name='acct']", usuario)
    navegador.escribir("input[name='pw']", clave)
    navegador.clic("input[type='submit']")

    if navegador.pide_login():
        input("[harness] Hacker News no me dejó entrar (¿captcha?). Inicia sesión en el navegador y presiona Enter aquí...")

    if navegador.pide_login():
        return "[harness] No pude iniciar sesión. No sigas intentando votar."

    return "[harness] Inicié sesión por ti. Usa leer_historias para revisar si tu voto quedó; si no, vota de nuevo."
