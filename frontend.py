import flet as ft
import requests
import time
import threading

URL_BACKEND = "http://127.0.0.1:8000"

# ==========================================
# Paleta de Cores Extraída do seu Tailwind
# ==========================================
BG_COLOR = "#f2fbfe"
SURFACE_LOW = "#ecf5f8"

PRIMARY = "#00535b"
PRIMARY_CONTAINER = "#a9ece5"  # Usando o secondary-container do seu HTML para o ícone
ON_PRIMARY_CONTAINER = "#00504b"

ERROR = "#ba1a1a"
ERROR_CONTAINER = "#ffdad6"
ON_ERROR_CONTAINER = "#93000a"


def main(page: ft.Page):
    # Configurações gerais da página
    page.title = "PSAI AsthmaCare - Monitoring"
    page.bgcolor = BG_COLOR
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ==========================================
    # Top App Bar (Cabeçalho)
    # ==========================================
    page.appbar = ft.AppBar(
        title=ft.Text("PSAI", weight=ft.FontWeight.BOLD, color=PRIMARY, size=24),
        bgcolor=SURFACE_LOW,
        center_title=True,
        elevation=2,
    )

    # ==========================================
    # Elementos Visuais do Card Principal
    # ==========================================
    icone_status = ft.Icon(ft.Icons.MONITOR_HEART, color=PRIMARY, size=70)
    
    # Círculo central com sombra (imitando o pulse do HTML)
    container_icone = ft.Container(
        content=icone_status,
        width=130,
        height=130,
        bgcolor=PRIMARY_CONTAINER,
        border_radius=100,
        alignment=ft.Alignment.CENTER,
        border=ft.Border.all(4, BG_COLOR),
        shadow=ft.BoxShadow(
            spread_radius=0, 
            blur_radius=30, 
            color="rgba(0, 83, 91, 0.4)"
        ),
    )

    texto_status = ft.Text(
        "Status: Monitorando",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=PRIMARY,
        text_align=ft.TextAlign.CENTER,
    )
    
    texto_descricao = ft.Text(
        "Dispositivo ativo e coletando dados ambientais.",
        size=16,
        color=ft.Colors.BLUE_GREY_700,
        text_align=ft.TextAlign.CENTER,
    )

    # O Card "Bolha" central
    card_principal = ft.Container(
        content=ft.Column(
            [container_icone, ft.Container(height=10), texto_status, texto_descricao],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=SURFACE_LOW,
        border_radius=32,
        padding=40,
        width=380,
        border=ft.Border.all(1, "#dbe4e7"),
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK12),
        alignment=ft.Alignment.CENTER,
    )

    # ==========================================
    # Card de Emergência (Inicia Oculto)
    # ==========================================
    card_emergencia = ft.Container(
        visible=False,
        bgcolor=ERROR_CONTAINER,
        border_radius=24,
        padding=25,
        width=380,
        border=ft.Border.all(2, ERROR),
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.WARNING_ROUNDED, color=ON_ERROR_CONTAINER),
                ft.Text("PLANO DE AÇÃO ÁGIL", size=20, weight=ft.FontWeight.BOLD, color=ON_ERROR_CONTAINER),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(color=ERROR),
            ft.Text("1. Mantenha a calma e SENTE o paciente reto.", size=16, color=ON_ERROR_CONTAINER, weight=ft.FontWeight.W_500),
            ft.Text("2. Administre o inalador de resgate.", size=16, color=ON_ERROR_CONTAINER, weight=ft.FontWeight.W_500),
            ft.Text("3. Monitore a respiração. Espere 4 minutos.", size=16, color=ON_ERROR_CONTAINER, weight=ft.FontWeight.W_500),
            ft.Text("4. Se não melhorar, repita o inalador e chame 192.", size=16, color=ON_ERROR_CONTAINER, weight=ft.FontWeight.W_500),
        ])
    )

    # ==========================================
    # Lógica de Reset e Transição de Cores
    # ==========================================
    def reset_alarme(e):
        try:
            requests.post(f"{URL_BACKEND}/reset")
        except Exception:
            print("Erro ao tentar resetar no backend.")

        # Volta o design para o modo Normal (Azul/Verde Água)
        page.bgcolor = BG_COLOR
        card_principal.bgcolor = SURFACE_LOW
        card_principal.border = ft.Border.all(1, "#dbe4e7")
        container_icone.bgcolor = PRIMARY_CONTAINER
        container_icone.shadow = ft.BoxShadow(
            spread_radius=0, 
            blur_radius=30, 
            color="rgba(0, 83, 91, 0.4)"
        )
        icone_status.color = PRIMARY
        
        texto_status.value = "Status: Monitorando"
        texto_status.color = PRIMARY
        texto_descricao.value = "Dispositivo ativo e coletando dados ambientais."
        
        card_emergencia.visible = False
        btn_reset.visible = False
        page.update()

    btn_reset = ft.ElevatedButton(
        "Crise Resolvida - Voltar ao Normal",
        icon=ft.Icons.CHECK_CIRCLE,
        style=ft.ButtonStyle(
            bgcolor=PRIMARY,
            color=ft.Colors.WHITE,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=16),
        ),
        on_click=reset_alarme,
        visible=False,
        width=380
    )

    # ==========================================
    # Montagem da Tela
    # ==========================================
    # Envolvemos tudo em um Container para dar uma margem superior agradável
    conteudo_tela = ft.Container(
        content=ft.Column(
            [card_principal, card_emergencia, btn_reset],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=ft.Padding.only(top=40),
        alignment=ft.Alignment.CENTER
    )
    
    page.add(conteudo_tela)

    # ==========================================
    # Thread de Comunicação com o Backend
    # ==========================================
    def checar_status():
        session = requests.Session()
        while True:
            try:
                resposta = session.get(f"{URL_BACKEND}/status", timeout=2).json()
                if (
                    resposta["status"] == "EMERGÊNCIA"
                    and texto_status.value != "EMERGÊNCIA ACIONADA!"
                ):
                    # Altera o design inteiro para o modo Emergência (Vermelho)
                    page.bgcolor = "#fff5f5"
                    card_principal.bgcolor = ft.Colors.WHITE
                    card_principal.border = ft.Border.all(2, ERROR)
                    
                    container_icone.bgcolor = ERROR
                    container_icone.shadow = ft.BoxShadow(
                        spread_radius=0, 
                        blur_radius=40, 
                        color=ERROR
                    )
                    icone_status.color = ft.Colors.WHITE
                    
                    texto_status.value = "EMERGÊNCIA ACIONADA!"
                    texto_status.color = ON_ERROR_CONTAINER
                    texto_descricao.value = "Botão de pânico pressionado pelo paciente."
                    
                    card_emergencia.visible = True
                    btn_reset.visible = True
                    page.update()
            except Exception as e:
                pass  # Backend pode estar desligado
            time.sleep(0.5)

    threading.Thread(target=checar_status, daemon=True).start()

ft.run(main)