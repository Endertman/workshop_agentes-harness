import json
import re
import unicodedata

CITAS_PEDIDAS = 2
MIN_PALABRAS = 8  # una cita de 2 palabras ("the proof") aparece en cualquier paper
CITA = re.compile(r'\[arXiv:(\d{4}\.\d{4,5})(?:v\d+)?\][^"“\n]*["“]([^"”\n]+)["”]')


def leer_citas(respuesta):
    return CITA.findall(respuesta)


# Solo letras y números: el PDF parte palabras ("com plexity"), cambia comillas (’ por ')
# y aplana superíndices (P^NP queda "P NP"); el modelo arregla todo eso al citar
def normalizar(texto):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", texto).lower())


# Acepta elipsis ("A ... B"): cada trozo tiene que estar en el fragmento, en orden
def esta_en(cita, texto):
    posicion = 0
    for trozo in re.split(r"\[?(?:\.\.\.|…)\]?", cita):
        trozo = normalizar(trozo)
        if trozo:
            posicion = texto.find(trozo, posicion)
            if posicion == -1:
                return False
            posicion += len(trozo)
    return True


def fragmentos_consultados(pasos):
    fragmentos = []
    for paso in pasos:
        if paso["herramienta"] == "consultar_rag" and paso["resultado"].startswith("["):
            fragmentos += [(f["arxiv_id"], normalizar(f["texto"])) for f in json.loads(paso["resultado"])]
    return fragmentos


def verificar_citas(respuesta, pasos):
    citas = leer_citas(respuesta)
    if len(citas) < CITAS_PEDIDAS:
        return False, f'Se pidieron {CITAS_PEDIDAS} citas con el formato [arXiv:ID] "cita textual" y hay {len(citas)}'

    # Si la cita salió de un fragmento del RAG, el paper existe: el fragmento se bajó de arXiv
    fragmentos = fragmentos_consultados(pasos)
    errores = []
    for arxiv_id, cita in citas:
        if len(cita.split()) < MIN_PALABRAS:
            errores.append(f'la cita de arXiv:{arxiv_id} es muy corta (mínimo {MIN_PALABRAS} palabras): "{cita}"')
        elif not any(id_ == arxiv_id and esta_en(cita, texto) for id_, texto in fragmentos):
            errores.append(f'la cita de arXiv:{arxiv_id} no está textual en ningún fragmento que te devolvió consultar_rag para ese paper (¿la parafraseaste o reescribiste una fórmula?): "{cita}"')
    if errores:
        return False, "; ".join(errores)

    return True, f"Las {len(citas)} citas salen textualmente de fragmentos que devolvió el RAG"


if __name__ == "__main__":
    fragmento = {"arxiv_id": "1708.03486", "similitud": 0.5, "texto": "But until now, no one could prove a super-linear lower bound f or the non- monotone com plexity"}
    pasos = [{"herramienta": "consultar_rag", "entrada": {}, "resultado": json.dumps([fragmento])}]
    cita = '- [arXiv:1708.03486] “no one could prove a super-linear lower bound for the non- monotone complexity” — explicación'

    assert leer_citas(cita) == [("1708.03486", "no one could prove a super-linear lower bound for the non- monotone complexity")]
    assert verificar_citas(cita + "\n" + cita, pasos)[0]
    assert not verificar_citas(cita.replace("1708.03486", "1109.5531") * 2, pasos)[0]       # otro paper
    assert esta_en("no one could prove ... the non-monotone complexity", fragmento_normalizado := normalizar(fragmento["texto"]))
    assert not esta_en("the non-monotone complexity ... no one could prove", fragmento_normalizado)  # orden invertido
    assert normalizar("where P^NP has") == normalizar("whereP NP has")
    assert normalizar("(STOC ’08, ToCT ’09)") == normalizar("(STOC '08, ToCT '09)")
    assert not verificar_citas((cita + "\n") * 2, [])[0]                                    # no usó el RAG
    assert not verificar_citas('- [arXiv:1708.03486] "no one could prove anything at all here ok"\n' * 2, pasos)[0]  # inventada
    print("ok")
