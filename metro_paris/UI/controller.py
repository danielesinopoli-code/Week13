import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self,e):
        self._model.creaGrafo()

        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"{self._model._grafo}"))
        for u, v, data in self._model._grafo.edges(data=True):
            tempo_perc = data["tempo"]
            self._view.lst_result.controls.append(ft.Text(f"{u} -> {v}, Tempo percorrenza: {tempo_perc}"))

        self._view._btnCalcola.disabled=False
        self._view._btnPercorsoMinimo.disabled=False
        self._view.update_page()


    def handleCercaRaggiungibili(self,e):
        idStazPartenza = int(self._view._ddStazPartenza.value)
        print(f"{idStazPartenza}")
        ris = self._model.getRaggiungibili(idStazPartenza)

        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Fermate raggiungibili da {self._model._dizionario_fermate[idStazPartenza]}"))
        for v in ris:
            self._view.lst_result.controls.append(ft.Text(f"{v}"))
        self._view.update_page()


    def handlePercorsoMinimo(self, e):
        idStazPartenza = int(self._view._ddStazPartenza.value)
        print(f"{idStazPartenza}")
        idStazArrivo = int(self._view._ddStazArrivo.value)
        print(f"{idStazArrivo}")

        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(
            ft.Text(f"Percorso minimo {self._model._dizionario_fermate[idStazPartenza]} -> {self._model._dizionario_fermate[idStazArrivo]}"))
        costo, percorso = self._model.getPercorsoMinimo(idStazPartenza, idStazArrivo)
        for fermata in percorso:
            self._view.lst_result.controls.append(ft.Text(f"{fermata}"))

        self._view.lst_result.controls.append(ft.Text(f"Costo: {costo}"))
        self._view.update_page()


    def populate_dropdown(self,dd):
        self._model.getAllFermate()
        #Le fermate le trovo nel model, in _lista_fermate

        for fermata in self._model._lista_fermate:
            dd.options.append(ft.dropdown.Option(key=fermata.id_fermata,
                                                 text=fermata.nome))
