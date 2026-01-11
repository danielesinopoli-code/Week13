import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaAeroporti(self, e):
        try:
            min = int(self._view.txtNumCompagnieMinimo.value)

        except ValueError:
            self._view.create_alert("Inserisci un numero valido")

        self._model.buildGrafo(min)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"grafo: {self._model._grafo}"))

        self.popolaDD()

        self._view.update_page()


    def popolaDD(self):
        for n in self._model._nodi:
            self._view.ddAeroportoPartenza.options.append(ft.dropdown.Option(text=n.AIRPORT, key=n.ID))
            self._view.ddAeroportoArrivo.options.append(ft.dropdown.Option(text=n.AIRPORT, key=n.ID))

        self._view.btnAeroporticonnessi.disabled = False
        self._view.ddAeroportoPartenza.disabled = False
        self._view.ddAeroportoArrivo.disabled = False

        self._view.txtNumTratteMassimo.disabled = False
        self._view.btnCercaItinerario.disabled = False

        self._view.update_page()

        # Metodo chiamato quando l'utente cambia la selezione della Dropdown dell'aeroporto di partenza
    def readDDPartenza(self, e):
        idPartenza = int(self._view.ddAeroportoPartenza.value)
        # Memorizzo l'aeroporto selezionato nel model
        self._model._partenza = self._model._dizionarioAeroporti[idPartenza]
        print(f"Aeroporto partenza: {self._model._partenza}")

        # Metodo chiamato quando l'utente cambia la selezione della Dropdown dell'aeroporto di arrivo
    def readDDArrivo(self, e):
        idArrivo = int(self._view.ddAeroportoArrivo.value)
        # Memorizzo l'aeroporto selezionato nel model
        self._model._arrivo = self._model._dizionarioAeroporti[idArrivo]
        print(f"Aeroporto arrivo: {self._model._arrivo}")

    def handle_aeroportiConnessi(self, e):
        u = self._model._partenza   # Salvo la scelta dell dropdown
        print(u)
        if u is None:
            self._view.create_alert("Seleziona un aeroporto di partenza")

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Vicini di {self._model._partenza}"))
        viciniTuple = self._model.getSortedNeighbors(u) #Chiamo la funzione ch etrova i vicini ordinati
        for v in viciniTuple:
            self._view.txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}")) #Printo ID - Nome
        self._view.update_page()











    def handleAeroporticonnessi(self, e):
        u = self._model._partenza
        print(u)
        if u is None:
            self._view.create_alert("Seleziona un aeroporto di partenza")

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Vicini di {self._model._partenza}"))
        viciniTuple = self._model.getSortedNeighbors(u)
        for v in viciniTuple:
            self._view.txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
        self._view.update_page()



    def handleCercaItinerario(self, e):

        u = self._model._partenza
        v = self._model._arrivo

        # Posso verificare se il percorso esista (punto 1 dell'esercizio)
        percorso = self._model.findPath(u, v)

        self._view.txt_result.controls.clear()
        if percorso is None:
            self._view.txt_result.controls.append(ft.Text(f"Non esiste un percorso tra {u} e {v}"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Percorso da {u} a {v}"))
            for a in percorso:
                self._view.txt_result.controls.append(ft.Text(f"{a.ID} - {a.AIRPORT}"))
        self._view.update_page()

        # Posso cercare il percorso "migliore" (punto 2 dell'esercizio), ovvero il percorso
        # che massimizzi il numero totale di voli per ciacuna delle tratte del percorso individuato

        try:
            numTratteMassimo = int(self._view.txtNumTratteMassimo.value)
        except ValueError:
            self._view.create_alert("Inserisci un numero")
            return

        percorso_migliore, peso = self._model.findBestPath(u, v, numTratteMassimo)
        print(peso)
        print(percorso_migliore)
        self._view.txt_result.controls.append(ft.Text(f"\nPercorso migliore da {u} a {v}"))
        for a in percorso_migliore:
            self._view.txt_result.controls.append(ft.Text(f"{a.ID} - {a.AIRPORT}"))
        self._view.txt_result.controls.append(ft.Text(f"\nPeso: {peso}"))
        self._view.update_page() #
