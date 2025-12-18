import copy

import networkx as nx
from flight_delays.database.DAO import DAO

class Model:
    def __init__(self):
        # Costruisco lista e dizionario dei nodi (oggetti Airport)
        self._listaAeroporti = DAO.getAllAirports()
        self._dizionarioAeroporti = {}
        for a in self._listaAeroporti:
            self._dizionarioAeroporti[a.ID] = a

        # Variabili per la gestione del grafo
        self._grafo = nx.Graph()
        self._nodi = []
        self._archi = []

        # Aeroporti selezionati dalla dropdown
        self._partenza = None
        self._arrivo = None

        # Ricorsione, soluzione/percorso migliore e miglior costo (valore della funz. obiettivo)
        self._bestPath = []
        self._bestWeight = 0


    def buildGraph(self, min):
        # NODI
        self._nodi = DAO.getNodes(min, self._dizionarioAeroporti)
        self._grafo.add_nodes_from(self._nodi)
        # ARCHI

        # Versione sviluppata in aula che usa la query più semplice che non
        # aggrega vola A->B e B->A; l'aggregazione (somma) viene gestita in
        # Python sommando il peso degli archi, grazie al fatto che il grafo
        # è non orientato
        """
        connessioni = DAO.getEdges(self._dizionarioAeroporti)
        for c in connessioni:
            if c.aPartenza in self._grafo and c.aArrivo in self._grafo:
                if self._grafo.has_edge(c.aPartenza, c.aArrivo):
                    self._grafo[c.aPartenza][c.aArrivo]["weight"] += c.voli
                else:
                    self._grafo.add_edge(c.aPartenza, c.aArrivo, weight=c.voli)
        """
        # Versione che utilizza una query più complessa, che somma i pesi
        # per archi A->B e B->A, non è puù necessario farlo in Python
        connessioni = DAO.getEdgesConQueryComplessa(self._dizionarioAeroporti)
        for c in connessioni:
            if c.aPartenza in self._grafo and c.aArrivo in self._grafo:
                self._grafo.add_edge(c.aPartenza, c.aArrivo, weight=c.voli)


    def getSortedNeighbors(self, v0):
        vicini = self._grafo.neighbors(v0)
        viciniTuple = []
        for v in vicini:
            viciniTuple.append((v, self._grafo[v0][v]["weight"]))
            viciniTuple.sort(key = lambda x: x[1], reverse = True)
        return viciniTuple

    def findPath(self, u, v):
        print(f"Percorso tra {u} e {v}")
        connessa = nx.node_connected_component(self._grafo, u)
        if v in connessa:
            print("Il percorso esiste")
            # Un modo per cercare il percorso è usare Dijkstra, che ritorna peraltro quello minimo (peso)
            """
            percorso = nx.dijkstra_path(self._grafo, u, v)
            print(percorso)
            return percorso
            """
            # Oppure si può usare una visita, BFS, percorso più corto (num. archi) , DFS più lungo (num. archi)
            albero = nx.bfs_tree(self._grafo, u)
            if v in albero:
                percorso = [v]
            while percorso[-1] != u:
                percorso.append(list(albero.predecessors(percorso[-1]))[0])
            print(percorso)
            return percorso

        else:
            print("Il percorso NON esiste")
            return None


    def findBestPath(self, v0, v1, t):
        self._bestPath = []
        self._bestObjFun = 0

        parziale = [v0]

        self._ricorsione(parziale, v1, t)

        return self._bestPath, self._bestWeight

    def _ricorsione(self, parziale, target, t):
        # Verificare che parziale sia una possibile soluzione
            # Verificare se parziale sia meglio di best
            # Esco

        if self.computePathWeight(parziale) > self._bestWeight and parziale[-1] == target:
            self._bestWeight = self.computePathWeight(parziale)
            self._bestPath = copy.deepcopy(parziale)

        if len(parziale) == t+1:
            return

        # Posso ancora aggiungere nodi
            # Prendo i vicini e provo ad aggiungere
            # Ricorsione
        for n in self._grafo.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, target, t)
                parziale.pop()


    def computePathWeight(self, listOfNodes):
        totalWeight = 0
        for i in range(0, len(listOfNodes)-1):
            totalWeight += self._grafo[listOfNodes[i]][listOfNodes[i+1]]["weight"]

        return totalWeight
