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

def update_result_label(response, error_message, result_label, short_url_link, open_button):
    if response is not None:
        if response.status_code == 200:
            short_url = response.text.strip()  # La respuesta contiene la URL acortada
            if short_url.startswith("http"):  # Verificar que la respuesta sea una URL válida
                
                short_url_link.value = short_url  # Mostrar la URL acortada
                result_label.value = "URL acortada:"
                short_url_link.href = short_url  # Hacerla clicable
                short_url_link.target = "_blank"  # Abrir en nueva pestaña
                open_button.disabled = False  # Habilitar el botón para abrir la URL
            else:
                result_label.value = "Error: " + short_url  # Mensaje de error de da.gd
        else:
            if "Short URL already taken" in response.text:
                result_label.value = "El sufijo personalizado ya está en uso. Elige uno diferente."
            else:
                result_label.value = f"Error al acortar la URL. Código: {response.status_code}, Mensaje: {response.text}"
    else:
        result_label.value = error_message  # Muestra el mensaje de error

def open_short_url(short_url):
    if short_url:
        webbrowser.open(short_url)  # Abre la URL en el navegador

def copy_short_url(e, short_url_link):
    if short_url_link.value:
        e.page.set_clipboard(short_url_link.value)
        # Opcional: Mostrar una notificación de éxito
        e.page.snack_bar = ft.SnackBar(ft.Text("URL copiada al portapapeles"))
        e.page.snack_bar.open = True
        e.page.update()

def main(page):
    page.title = "Acortador de URL"
    page.window.icon_path = "assets/icon_windows.ico"
    page.window.width = 550  # Ajusta el ancho de la ventana
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    titulo_soft = ft.Text("Acortador de URL", size=30, weight=ft.FontWeight.BOLD)
    url_input = ft.TextField(label="Ingresa la URL larga", width=400)
    custom_suffix_input = ft.TextField(label="Sufijo personalizado (opcional)", width=400)
    result_label = ft.Text("")  # Para mostrar la URL acortada
    short_url_link = ft.Text("")  # Para mostrar la URL acortada como enlace

    open_button = ft.ElevatedButton(
        "Abrir URL Acortada",
        on_click=lambda e: open_short_url(short_url_link.value),
        disabled=True
    )
    copy_button = ft.ElevatedButton(
        "Copiar URL",
        on_click=lambda e: copy_short_url(e, short_url_link),
        disabled=True
    )
    shorten_button = ft.ElevatedButton(
        "Acortar URL",
        on_click=lambda e: handle_shorten(
            url_input.value.strip(),
            custom_suffix_input.value.strip(),
            result_label,
            short_url_link,
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
        short_url_link,
        # Crear una fila para los botones
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[open_button, copy_button]  # Botones en horizontal
        )
    ])

    # Agregar la columna a la página
    page.add(column)

def handle_shorten(long_url, custom_suffix, result_label, short_url_link, open_button, copy_button):
    response, error_message = shorten_url(long_url, custom_suffix)
    update_result_label(response, error_message, result_label, short_url_link, open_button)  # Actualiza el label y el enlace
    if response and response.status_code == 200 and short_url_link.value.startswith("http"):
        copy_button.disabled = False  # Habilitar el botón de copiar
    else:
        copy_button.disabled = True  # Deshabilitar si hay error
    result_label.page.update()  # Actualiza la interfaz

#if __name__ == "__main__":
#    ft.app(target=main,assets_dir="assets")
ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)