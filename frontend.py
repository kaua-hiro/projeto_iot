import flet as ft
import requests
import time
import threading

URL_BACKEND = "http://localhost:8000"

def main(page: ft.Page):
    page.title = "Monitoramento de Asma - Responsável"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Elementos Visuais
    icone_status = ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.GREEN, size=100)
    texto_status = ft.Text(
        "Status: Monitorando",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN
    )

    # Card de Primeiros Socorros (inicia invisível)
    card_emergencia = ft.Card(
        visible=False,
        content=ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("PLANO DE AÇÃO ÁGIL - ASMA", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
                ft.Text("1. Mantenha a calma e SENTE o paciente reto.", size=18),
                ft.Text("2. Administre o inalador de resgate (Ex: Salbutamol)", size=18),
                ft.Text("3. Monitore a respiração. Espere 4 minutos.", size=18),
                ft.Text("4. Se não melhorar, repita o inalador e chame a ambulância (192).", size=18),
            ])
        )
    )

    # Função para desativar o alarme
    def reset_alarme(e):
        try:
            requests.post(f"{URL_BACKEND}/reset")
        except Exception:
            print("Erro ao tentar resetar no backend.")

        page.bgcolor = ft.Colors.WHITE
        icone_status.color = ft.Colors.GREEN
        texto_status.value = "Status: Monitorando"
        texto_status.color = ft.Colors.GREEN
        card_emergencia.visible = False
        btn_reset.visible = False
        page.update()

    # Botão de Reset (inicia invisível)
    btn_reset = ft.ElevatedButton(
        "Crise Resolvida - Voltar ao Normal",
        on_click=reset_alarme,
        visible=False
    )

    # Adiciona os elementos à tela
    page.add(icone_status, texto_status, card_emergencia, btn_reset)

    # Função que roda em segundo plano checando o backend
    def checar_status():
        while True:
            try:
                resposta = requests.get(f"{URL_BACKEND}/status").json()
                if (
                    resposta["status"] == "EMERGÊNCIA"
                    and texto_status.value != "Status: EMERGÊNCIA - BOTÃO ACIONADO!"
                ):
                    page.bgcolor = ft.Colors.RED_50
                    icone_status.color = ft.Colors.RED
                    texto_status.value = "Status: EMERGÊNCIA - BOTÃO ACIONADO!"
                    texto_status.color = ft.Colors.RED
                    card_emergencia.visible = True
                    btn_reset.visible = True
                    page.update()
            except Exception as e:
                print(f"Erro na thread de checagem do frontend: {e}")
            time.sleep(1)

    # Inicia a checagem em paralelo
    threading.Thread(target=checar_status, daemon=True).start()

# ✅ Correção principal: ft.run(main) → ft.app(target=main)
ft.app(target=main)