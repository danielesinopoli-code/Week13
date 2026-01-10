import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.buildGrafo() # grafo costruito nel model
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"{self._model._grafo}"))
        self._view._btnCompConnessa.disabled = False
        self._view._btnCercaOggetti.disabled = False

        self._view.update_page()

    def handleCompConnessa(self,e):
        text_id = self._view._txtIdOggetto.value
        try:
            id = int(text_id)
            print(f"{id}")
            # se sono qui posso usare id per le operazioni seguenti
            numNodi = self._model.calcolaConnessa(id) # passo un id, non un oggetto
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Dim. componente connessa: {numNodi}"))
            self._view.update_page()
            #qui posso popolare la dropdowon _ddLunghezza

            for i in range(2, numNodi):
                self._view._ddLunghezza.options.append(ft.dropdown.Option(f"{i}"))
                self._view.update_page()



        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserisci un id valido"))
            self._view.update_page()


    def handleCercaOggetti(self,e ):
        id_oggetto= int(self._view._txtIdOggetto.value)
        lunghezza = int(self._view._ddLunghezza.value)
        percorsoMigliore, pesoMigliore = self._model.getPercorsoMAssimo(id_oggetto,lunghezza)
        print("finito")

