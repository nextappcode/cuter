import flet as ft
import requests
import webbrowser

def shorten_url(long_url, custom_suffix):
    if long_url and (long_url.startswith("http://") or long_url.startswith("https://")):
        try:
            # Construir la URL de la API
            api_url = f"https://da.gd/s?url={long_url}"
            if custom_suffix:
                api_url += f"&shorturl={custom_suffix}"  # Agregar el sufijo personalizado

            response = requests.get(api_url)
            return response, None  # Devuelve el objeto de respuesta y None como mensaje de error
        except Exception as e:
            return None, f"Error: {str(e)}"  # Devuelve None y el mensaje de error
    else:
        return None, "Por favor, ingresa una URL válida que comience con http:// o https://."

def update_result_label(response, error_message, result_label, short_url_button, open_button, copy_button):
    if response is not None:
        if response.status_code == 200:
            short_url = response.text.strip()
            if short_url.startswith("http"):
                short_url_button.text = short_url
                short_url_button.visible = True
                result_label.value = "URL acortada:"
                copy_button.disabled = False
            else:
                result_label.value = "Error: " + short_url
                short_url_button.visible = False
                copy_button.disabled = True
        else:
            if "Short URL already taken" in response.text:
                result_label.value = "El sufijo personalizado ya está en uso. Elige uno diferente."
            else:
                result_label.value = f"Error al acortar la URL. Código: {response.status_code}, Mensaje: {response.text}"
            short_url_button.visible = False
            copy_button.disabled = True
    else:
        result_label.value = error_message
        short_url_button.visible = False
        copy_button.disabled = True
    
    result_label.update()
    short_url_button.update()
    copy_button.update()

def open_short_url(short_url):
    if short_url:
        webbrowser.open(short_url)  # Abre la URL en el navegador

def copy_short_url(e, short_url_button):
    if short_url_button.text:
        e.page.set_clipboard(short_url_button.text)
        e.page.snack_bar = ft.SnackBar(ft.Text("URL copiada al portapapeles"))
        e.page.snack_bar.open = True
        e.page.update()

def main(page):
    page.title = "Acortador de URL"
    page.window.icon_path = "assets/icon_windows.ico"
    page.window.width = 550  # Ajusta el ancho de la ventana
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    titulo_soft = ft.Text("Quieres acortar una URL? Hazlo aqui!", size=30, weight=ft.FontWeight.BOLD)
    url_input = ft.TextField(label="Ingresa la URL larga", width=400)
    custom_suffix_input = ft.TextField(label="Sufijo personalizado (opcional)", width=400)
    result_label = ft.Text("")  # Para mostrar el texto "URL acortada:"
    short_url_button = ft.TextButton(
        text="",
        on_click=lambda _: webbrowser.open(short_url_button.text),
        visible=False  # Inicialmente oculto
    )

    open_button = ft.ElevatedButton(
        "Abrir URL Acortada",
        on_click=lambda e: open_short_url(short_url_button.text),
        disabled=True
    )
    copy_button = ft.ElevatedButton(
        "Copiar URL",
        on_click=lambda e: copy_short_url(e, short_url_button),
        disabled=True
    )
    shorten_button = ft.ElevatedButton(
        "Acortar URL",
        on_click=lambda e: handle_shorten(
            url_input.value.strip(),
            custom_suffix_input.value.strip(),
            result_label,
            short_url_button,
            open_button,
            copy_button  # Pasar el botón de copiar para habilitarlo
        )
    )

    # Crear una columna para centrar el contenido
    column = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20  # Espaciado entre los elementos
    )

    # Agregar los elementos a la columna
    column.controls.extend([
        titulo_soft,
        url_input,
        custom_suffix_input,
        shorten_button,
        result_label,
        short_url_button,
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[copy_button]
        )
    ])

    # Agregar la columna a la página
    page.add(column)

def handle_shorten(long_url, custom_suffix, result_label, short_url_button, open_button, copy_button):
    response, error_message = shorten_url(long_url, custom_suffix)
    update_result_label(response, error_message, result_label, short_url_button, open_button, copy_button)
    result_label.page.update()

#if __name__ == "__main__":
#    ft.app(target=main,assets_dir="assets")
ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
