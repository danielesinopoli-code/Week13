import flet as ft


class View():
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("Flight Delays", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW with some controls
        self.txtNumCompagnieMinimo = ft.TextField( label="Num compagnie minimo", width=250)
        self.btnAnalizzaAeroporti = ft.ElevatedButton(text="Analizza aeroporti", on_click=self._controller.handle_analizzaAeroporti)
        row1 = ft.Row([self.txtNumCompagnieMinimo, self.btnAnalizzaAeroporti],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        self.ddAeroportoPartenza = ft.Dropdown(label="Aeroporto partenza", width = 250)
        self.ddAeroportoArrivo = ft.Dropdown(label="Aeroporto arrivo", width = 250)
        self.btnAeroportiConnessi = ft.ElevatedButton(text="Aeroporti connessi", width = 150, on_click=self._controller.handle_aeroportiConnessi)
        row2 = ft.Row([self.ddAeroportoPartenza, self.ddAeroportoArrivo, self.btnAeroportiConnessi],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self.txtNumTratteMassimo = ft.TextField( label="Num tratte minimo", width=250)
        self.btnAnalizzaAeroporti = ft.ElevatedButton(text="Cerca itinerario", on_click=self._controller.handle_cercaItinerario)
        row3 = ft.Row([self.txtNumTratteMassimo, self.btnAnalizzaAeroporti],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)


        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
