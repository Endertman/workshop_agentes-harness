import json

from playwright.sync_api import sync_playwright

LEER_HISTORIAS = """
() => Array.from(document.querySelectorAll(".athing")).map((fila, i) => ({
  posicion: i + 1,
  id: fila.id,
  titulo: fila.querySelector(".titleline a")?.textContent ?? "",
  ya_votada: document.querySelector("#up_" + fila.id)?.classList.contains("nosee") ?? true,
}))
"""


class Navegador:
    def abrir(self):
        self.playwright = sync_playwright().start()
        chrome = self.playwright.chromium.connect_over_cdp("http://localhost:9222")
        self.pagina = chrome.contexts[0].new_page()
        input("Pestaña lista: acomoda las ventanas y presiona Enter para empezar...")

    def ir_a(self, url):
        self.pagina.goto(url, wait_until="domcontentloaded", timeout=15000)
        return f"Página abierta: {url}"

    def leer_texto(self):
        return self.pagina.inner_text("body")[:4000]

    def leer_historias(self):
        historias = self.pagina.evaluate(LEER_HISTORIAS)
        return json.dumps(historias, ensure_ascii=False, indent=2)

    def clic(self, selector):
        self.pagina.click(selector, timeout=10000)
        self.pagina.wait_for_load_state("domcontentloaded", timeout=10000)
        return f"Clic en {selector}, ahora en {self.pagina.url}"

    def cerrar(self):
        self.playwright.stop()
