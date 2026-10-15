import anthropic
from dotenv import load_dotenv

load_dotenv()

MODELO = "claude-haiku-5-5"
cliente = anthropic.Anthropic()


def llamar_modelo(sistema, mensajes, herramientas):
    return cliente.messages.create(
        model=MODELO,
        max_tokens=16000,
        thinking={"type": "disabled"},
        system=sistema,
        tools=herramientas,
        messages=mensajes,
    )
