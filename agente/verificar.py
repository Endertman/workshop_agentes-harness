import re
from difflib import SequenceMatcher

import arxiv

# simplified: solo IDs nuevos (2403.01234); los viejos (math/0601001) no se reconocen
CITAS_PEDIDAS = 3
CITA = re.compile(r"\[arXiv:(\d{4}\.\d{4,5})(?:v\d+)?\]\s*(.+)")


def leer_citas(respuesta):
    return [(arxiv_id, titulo.strip(" *\"")) for arxiv_id, titulo in CITA.findall(respuesta)]


def parecidos(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= 0.8


def verificar_citas(respuesta, pasos):
    citas = leer_citas(respuesta)
    if len(citas) < CITAS_PEDIDAS:
        return False, f"Se pidieron {CITAS_PEDIDAS} citas con el formato [arXiv:ID] Título y hay {len(citas)}"

    for arxiv_id, titulo in citas:
        titulo_real = arxiv.obtener(arxiv_id)
        if titulo_real is None:
            return False, f"arXiv:{arxiv_id} no existe"
        if not parecidos(titulo, titulo_real):
            # No revela el título real: el modelo lo copiaría en el reintento sin haber buscado
            return False, f'arXiv:{arxiv_id} existe, pero no se titula "{titulo}"'

    return True, f"Las {len(citas)} citas existen en arXiv y los títulos coinciden"


if __name__ == "__main__":
    citas = leer_citas('- [arXiv:1708.03486v3] **On the Approximation Method and the P versus NP Problem**\n- nada aquí')
    assert citas == [("1708.03486", "On the Approximation Method and the P versus NP Problem")], citas
    assert parecidos("On the approximation method and the P vs NP problem", "On the Approximation Method and the P versus NP Problem")
    assert not parecidos("A proof that P = NP", "On the Approximation Method and the P versus NP Problem")
    print("ok")
