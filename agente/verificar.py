import json
import re


def verificar_voto(navegador, pasos):
    ids_votados = []
    for paso in pasos:
        if paso["herramienta"] == "clic":
            encontrado = re.search(r"up_(\d+)", paso["entrada"].get("selector", ""))
            if encontrado:
                ids_votados.append(encontrado.group(1))

    if not ids_votados:
        return False, "El agente nunca hizo clic en una flecha de voto"

    navegador.ir_a("https://news.ycombinator.com")
    historias = json.loads(navegador.leer_historias())
    for historia in historias:
        if historia["id"] in ids_votados and historia["ya_votada"]:
            return True, f"La historia {historia['id']} quedó votada"

    return False, "El agente hizo clic, pero el voto no quedó registrado"
