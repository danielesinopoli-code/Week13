import networkx as nx
from geopy.distance import geodesic

from metro_paris.database.DAO import DAO

class Model:
    def __init__(self):
        self._lista_fermate = []
        self._dizionario_fermate = {}
        self._grafo = None

    def getRaggiungibili(self, idStazPartenza):
        fermataPartenza = self._dizionario_fermate[idStazPartenza]

        edges = nx.bfs_edges(self._grafo, fermataPartenza) # Archi del grafo di visita da fermataPartenza
        visited_nodes = []
        for u, v in edges:
            visited_nodes.append(v)
        return visited_nodes

    def getPercorsoMinimo(self, idStazPartenza, idStazArrivo):

        vSource = self._dizionario_fermate[idStazPartenza]
        vTarget = self._dizionario_fermate[idStazArrivo]

        costo, percorso = nx.single_source_dijkstra(self._grafo, vSource, vTarget,weight='tempo')

        return costo, percorso


    def getAllFermate(self):
        fermate = DAO.readAllFermate()
        self._lista_fermate = fermate
        # Mi sono costruito un dizionario di fermate, con chiave
        # l'id_fermata e valore l'oggetto fermata corrispondente
        for fermata in self._lista_fermate:
            self._dizionario_fermate[fermata.id_fermata] = fermata


    def creaGrafo(self):
        #self._grafo = nx.MultiDiGraph() # Posso avere più archi tra due nodi
        self._grafo = nx.DiGraph()  # Senza archi multipli tra due nodi
        for fermata in self._lista_fermate:
            self._grafo.add_node(fermata)
        # PRIMO MODO DI AGGIUNGERE GLI ARCHI, CON 619*619 QUERY SQL
        """
        for u in self._grafo: # Per ognuno dei 619 nodi
            for v in self._grafo: # Per ognuno dei possbili nodi connessi
                risultato = DAO.existsConnessioneTra(u, v)
                if(len(risultato) > 0): # C'è almeno una connessione
                    self._grafo.add_edge(u, v) # Creo l'arco
                    print(f"Aggiunto arco tra {u} e {v}")
        """

        # SECONDO MODO, CON 619 QUERY A CERCARE I NODI VICINI
        """
        conta = 0
        for u in self._grafo:
            connessioniAVicini = DAO.searchViciniAFermata(u)
            for connessione in connessioniAVicini:
                fermataArrivo = self._dizionario_fermate[connessione.id_stazA]
                self._grafo.add_edge(u, fermataArrivo)
                print(f"Aggiunto arco tra {u} e {fermataArrivo}")
                print(len(self._grafo.edges()))
        """

        # TERZO MODO, CON UNA QUERY SOLA CHE ESTRAE IN UN COLPO SOLO TUTTE LE CONN.
        """
        listaConnessioni = DAO.readAllConnessioni()
        for c in listaConnessioni:
            u_nodo = self._dizionario_fermate[c.id_stazP]
            v_nodo = self._dizionario_fermate[c.id_stazA]
            self._grafo.add_edge(u_nodo, v_nodo)
            print(f"Aggiunto arco tra {u_nodo} e {v_nodo}")
        """

        # COSTRUISCO UN GRAFO PESATO
        """
        listaConnessioni = DAO.readAllConnessioni()
        for c in listaConnessioni:
            u_nodo = self._dizionario_fermate[c.id_stazP]
            v_nodo = self._dizionario_fermate[c.id_stazA]
            #print(f"{self._grafo[u_nodo][v_nodo]}")
            if self._grafo.has_edge(u_nodo, v_nodo):
                self._grafo[u_nodo][v_nodo]["peso"] += 1
            else:
                self._grafo.add_edge(u_nodo, v_nodo, peso=1)

            print(f"Aggiunto arco tra {u_nodo} e {v_nodo}, peso: {self._grafo[u_nodo][v_nodo]}")
        """
        # COSTRUISCO UN MULTI-GRAFO NEL QUALE IL PESO DEGLI ARCHI E' IL T. PERCORR.
        """
        listaConnessioni = DAO.readAllConnessioni()
        for c in listaConnessioni:
            u_nodo = self._dizionario_fermate[c.id_stazP]
            v_nodo = self._dizionario_fermate[c.id_stazA]
            punto_u = (u_nodo.coordX, u_nodo.coordY)
            punto_v = (v_nodo.coordX, v_nodo.coordY)
            distanza = geodesic(punto_u, punto_v).km
            velocita = DAO.readVelocita(c._id_linea)
            tempo_perc = distanza / velocita * 60 # Tempo percorrenza in min.
            print(f"Distanza: {distanza}, velocità: {velocita}, tempo_perc: {tempo_perc}")
            self._grafo.add_edge(u_nodo, v_nodo, tempo = tempo_perc)
        """
        # COSTRUISCO UN GRAFO (NON MULTI) NEL QUALE IL PESO DEGLI ARCHI E' IL T. PERCORR.
        listaConnessioni = DAO.readAllConnessioni()
        for c in listaConnessioni:
            u_nodo = self._dizionario_fermate[c.id_stazP]
            v_nodo = self._dizionario_fermate[c.id_stazA]
            punto_u = (u_nodo.coordX, u_nodo.coordY)
            punto_v = (v_nodo.coordX, v_nodo.coordY)
            distanza = geodesic(punto_u, punto_v).km
            velocita = DAO.readVelocita(c._id_linea)
            tempo_perc = distanza / velocita * 60 # Tempo percorrenza in min.
            print(f"Distanza: {distanza}, velocità: {velocita}, tempo_perc: {tempo_perc}")
            if (self._grafo.has_edge(u_nodo, v_nodo)):  # Se l'arco c'è già
                # Verifico se il tempo di percorrenza appena calcolato è minore di
                # di quello associato all'arco già presente, se così aggiorno
                if (self._grafo[u_nodo][v_nodo]["tempo"]>tempo_perc):
                    self._grafo[u_nodo][v_nodo]["tempo"] = tempo_perc
            else:  # Altrimenti lo aggiungo
                self._grafo.add_edge(u_nodo, v_nodo, tempo=tempo_perc)

        print(self._grafo)


