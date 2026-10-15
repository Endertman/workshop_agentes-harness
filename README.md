# Taller: agentes y harness engineering

Endert Guerrero · Bemobi

---

## ¿Qué es un agente?

Un modelo de lenguaje, por sí solo, solo responde texto. Un **agente** es ese modelo con tres cosas más:

1. **Herramientas**: funciones que puede pedir que se ejecuten (abrir una página, leer un archivo, correr un cálculo).
2. **Un bucle**: el modelo pide una herramienta, ve el resultado y decide qué hacer después. Repite hasta terminar.
3. **Una tarea**: lo que le pedimos que haga.

```
tarea → modelo → ¿usa una herramienta? → resultado → modelo → ... → respuesta
```

## ¿Qué es un harness?

El **harness** es todo lo que rodea al modelo: las herramientas, la memoria de la conversación, los límites, las verificaciones. El modelo pone la "inteligencia"; el harness pone el control.

Una buena forma de recordarlo: **el harness es todo, menos el modelo**.

## ¿Qué es harness engineering?

Es la práctica de mejorar el entorno del agente en vez de "pedirle que lo haga mejor":

> Cada vez que el agente se equivoca, cambias el entorno para que no vuelva a cometer ese error.

Igual que en un laboratorio: si una medición sale mal, no le pides al instrumento que "se esfuerce más"; mejoras el montaje y agregas controles.

## Las tres piezas de un harness

| Pieza | Qué hace | Analogía en el laboratorio |
|---|---|---|
| **Contexto** | Decide qué información ve el modelo en cada paso | El cuaderno de laboratorio |
| **Límites** | Detienen al agente si se pasa (demasiados pasos, demasiada información) | Los topes de seguridad del equipo |
| **Verificación** | Revisa cada paso y el resultado final; si algo está mal, avisa o reintenta | Repetir la medición y compararla |

Los límites atrapan fallas de **forma** (el agente se quedó dando vueltas). La verificación atrapa fallas de **fondo** (el agente terminó, pero la respuesta es incorrecta). Necesitas ambas.

---

## La demo, paso a paso

La tarea del agente: entrar a Hacker News y votar por la historia mejor ubicada que aún no haya votado. Para lograrlo necesita usar un navegador real.

Cada rama agrega una pieza:

| Rama | Qué se agrega |
|---|---|
| `1` | Agente básico: herramientas + modelo + contexto + bucle |
| `2` | Límites: un máximo de iteraciones y el recorte del contexto |
| `3` | El harness: abre el entorno (el navegador), corre el bucle y lo cierra siempre |
| `4` | Verificación: el harness no le cree al modelo, revisa el navegador y reintenta si falló |
| `5` | Validación de cada paso: después de cada paso el harness revisa el navegador y, si el agente llegó al login, inicia sesión por él |
| `6` | Otro dominio, el mismo harness: el agente recomienda papers de arXiv y el harness verifica en la API de arXiv que existan y que el título coincida |
| `7` | RAG: el agente descarga los papers y responde con citas textuales; el harness verifica que cada cita salga de un fragmento que devolvió el RAG |

En las ramas 1 a 4 el agente dice "listo, voté", pero el voto no queda: Hacker News lo manda al login. Recién en la rama 4 el harness se da cuenta, y en la rama 5 lo arregla.

```sh
git checkout 1   # y luego 2, 3, 4, 5
```

## Archivos

Todo el código está en la carpeta `agente/`.

| Archivo | Desde la rama | Qué hace |
|---|---|---|
| `inicio.py` | 1 | El punto de partida: define la tarea |
| `herramientas.py` | 1 | Las herramientas del agente (abrir, leer, hacer clic) |
| `modelo.py` | 1 | La conexión con el modelo |
| `contexto.py` | 1 | Arma la conversación y recorta los mensajes viejos |
| `bucle.py` | 1 | El bucle: modelo → herramienta → resultado → modelo |
| `navegador.py` | 1 | El entorno: un navegador real |
| `limites.py` | 2 | Los límites que se revisan antes de cada paso |
| `harness.py` | 3 | Abre el entorno, corre el bucle, verifica y cierra |
| `verificar.py` | 4 | Revisa en el navegador si el voto quedó de verdad |
| `login.py` | 5 | Revisa cada paso e inicia sesión cuando hace falta |
| `arxiv.py` | 6 | El entorno nuevo: busca papers y consulta un ID en la API de arXiv (reemplaza a `navegador.py` y `login.py`) |
| `biblioteca.py` | 7 | El RAG: descarga los PDF, los corta en fragmentos y busca por similitud coseno |

## Cómo correrlo

Necesitas Python 3.10 o más nuevo y Google Chrome.

Una sola vez, prepara el proyecto:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env               # completa tus claves (nunca subas .env a git)
```

Abre el Chrome que va a usar el agente y déjalo abierto. Es un Chrome aparte, con su propio perfil:

```sh
open -na "Google Chrome" --args --remote-debugging-port=9222 --user-data-dir="$HOME/chrome-taller"
```

Corre el agente. Cada vez abre una pestaña nueva en ese Chrome y espera un Enter para empezar:

```sh
git checkout 1                     # o la rama que quieras mostrar
python agente/inicio.py
```

Ese Chrome recuerda la sesión de Hacker News. Si ya iniciaste sesión, en las ramas 1 a 4 el voto sí funcionará: muéstralas antes de iniciar sesión, o cierra sesión antes de repetirlas.

Para cambiar de modelo, edita `MODELO` en `agente/modelo.py`.

## Rama 6: el oráculo de arXiv

`bucle.py`, `contexto.py`, `limites.py` y `modelo.py` no cambian. Solo cambian el entorno (`arxiv.py`), las herramientas y el verificador. Eso es lo que se lleva de un dominio a otro.

La tarea: recomendar 3 papers sobre P vs NP con el formato `- [arXiv:ID] Título`. El verificador consulta cada ID en arXiv y compara el título. Si falla, el harness reintenta y esta vez le dice al modelo **por qué** falló (en la rama 4 reintentaba a ciegas). No le dice el título real: el modelo lo copiaría sin buscar.

No necesita Chrome ni claves de Hacker News, solo `ANTHROPIC_API_KEY`:

```sh
git checkout 6
pip install -r requirements.txt
python agente/inicio.py
```

Para la demo, pon `CON_BUSQUEDA = False` en `agente/inicio.py`. El agente responde de memoria, inventa IDs o títulos y la verificación falla. Con `True` busca y pasa.

## Rama 7: RAG con citas verificadas

La rama 6 atrapa papers inventados. La 7 atrapa algo más sutil: **un paper real al que se le atribuye algo que no dice**.

### Qué es un RAG

RAG (*Retrieval-Augmented Generation*) significa buscar primero y generar después. Para el agente es una herramienta más, igual que hacer clic en Hacker News. Hay tres familias de búsqueda, y las tres son vectores:

| Tipo | Vector de cada texto | Encuentra | Falla con |
|---|---|---|---|
| **Disperso** (BM25) | Una dimensión por palabra del vocabulario; casi todas en cero | Términos exactos, siglas, nombres (`Razborov`, `ΛCDM`) | Sinónimos y paráfrasis |
| **Denso** (embeddings) | Unas cientos de dimensiones aprendidas; todas con valor | Significado, paráfrasis | Términos exactos raros |
| **Híbrido** | Los dos, y se combinan los rankings | Lo mejor de ambos | Es más complejo |

Esta rama usa **vectores densos**. Cada fragmento de cada paper es una fila de una matriz `M` (N fragmentos × 256 dimensiones), con filas normalizadas. Buscar es una multiplicación matriz-vector:

```python
puntajes = M @ q   # q: la pregunta como vector unitario → similitud coseno con cada fragmento
```

No hay base de datos vectorial: con decenas de papers, la búsqueda exacta sobra. Los embeddings los calcula [model2vec](https://github.com/MinishLab/model2vec) (`potion-base-8M`, ~30 MB), sin GPU ni torch.

### Qué verifica el harness

Las citas tienen el formato `- [arXiv:ID] "cita textual" — explicación`. Para cada una, el verificador revisa los pasos del intento y exige que el texto aparezca **en un fragmento que `consultar_rag` devolvió para ese mismo paper**. Si el agente no usó el RAG, no hay fragmentos y la verificación falla. Así el harness **obliga** a usar el RAG sin tener que pedírselo al modelo.

El verificador compara solo letras y números, así que tolera lo que el PDF rompe: espacios dentro de palabras, `’` frente a `'`, superíndices aplanados (`P^NP` sale como `P NP`). También acepta elipsis (`A ... B`). Las fórmulas no tienen arreglo: al pasar el PDF a texto, la notación se rompe (`MA eA E ̸⊆P A/poly`) y, si el modelo la reescribe bien, la cita ya no es textual. Por eso la tarea pide citar prosa. Lo que nunca pasa es una paráfrasis presentada como cita, que es justo lo que se busca atrapar.

```sh
git checkout 7
pip install -r requirements.txt
python agente/inicio.py
```

La primera vez se descargan el modelo de embeddings y los PDF (`papers/`, ignorada por git). Córrelo una vez antes del taller para que la demo no dependa de la red.

### Lo que el harness no puede hacer

arXiv está lleno de "pruebas" de P = NP y de P ≠ NP (busca la de Norbert Blum, de 2017, y lo que pasó después). El harness verifica que la cita sea **fiel a la fuente**, no que la fuente **tenga razón**. Si el agente cita textualmente una prueba equivocada, la verificación pasa. El harness te da trazabilidad; decidir qué es verdad sigue siendo trabajo del científico.

---

## ¿Y en investigación científica?

La misma idea sirve para un agente que lee datos de un experimento, ajusta un modelo y reporta un resultado. El harness es lo que te deja confiar en ese resultado: verifica que el agente realmente usó los datos, que las unidades tienen sentido y que el ajuste es bueno, en vez de aceptar un número inventado.
