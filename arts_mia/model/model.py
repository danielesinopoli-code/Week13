import copy

from arts_mia.database.DAO import DAO
import networkx as nx
from arts_mia.model.connessione import Connessione

class Model:
    def __init__(self):
        self._objects_list = []
        self._getObjects()
        # mi posso creare anche un dizionario di Object
        self._objects_dict = {} # è la idMap di Object
        for o in self._objects_list:
            self._objects_dict[o.object_id] = o
        # grafo semplice, non diretto ma pesato
        self._grafo = nx.Graph()

    def _getObjects(self):
        self._objects_list = DAO.readObjects()

    def buildGrafo(self):
        # nodi
        self._grafo.add_nodes_from(self._objects_list)
        # archi

        # MODO 1 (80k x 80k  query SQL, dove 80k sono i nodi)
        """
        for u in self._objects_list:
            for v in self._objects_list:
                DAO.readEdges(u, v) # da scrivere
        """

        # MODO 2 (usare una query sola per estrarre le connessioni)

        connessioni = DAO.readConnessioni(self._objects_dict)
        # leggo le connessioni dal DAO
        for c in connessioni:
            self._grafo.add_edge(c.o1, c.o2, peso = c.peso) # peso?

    def calcolaConnessa(self, id_nodo):
        nodo_sorgente = self._objects_dict[id_nodo]

        # Usando i successori
        successori = nx.dfs_successors(self._grafo, nodo_sorgente)
        print(f"Successori: {len(successori)}")
        #for nodo in successori:
        #    print(nodo)

        # Usando i predecessori (ma devo poi increm. di 1)
        prededessori = nx.dfs_predecessors(self._grafo, nodo_sorgente)
        print(f"Prededessori: {len(prededessori)}")

        # Ottenendo l'albero di visita
        albero = nx.dfs_tree(self._grafo, nodo_sorgente)
        print(f"Albero: {albero}")
        return len(albero.nodes)

    def getPercrosoMAssimo(self, id_oggetto, lunghezza):
        v_iniziale = self._objects_dict[id_oggetto]
        self._soluzioneMigliore = [] #Lista di nodi
        self._pesoMigliore =0

        parziale = [v_iniziale] #inserisco il primo nodo , quello di partenza
        self.ricorsione(parziale, lunghezza)

        return soluzioneMigliore, pesoMigliore


    def ricorsione(self, parziale, lunghezza):
        if len(parziale) ==  lunghezza:
            # Qui ho la soluzione
            if self.calcolaPeso(parziale) > self.pesoMigliore:
                self._pesoMigliore = self.calcolaPeso(parziale)
                self._soluzioneMigliore = copy.deepcopy(parziale)
            return
        #Altrimenti attivo la ricorsione
        for v in self._grafo.neighbors(parziale[-1]): #Vicini dell ultimo nodo aggiunto
            if v not in parziale and v.classification == parziale[0]:
                parziale.append(v)
                self.ricorsione(parziale, lunghezza)
                parziale.pop()




    def calcolaPeso(self,listaNodi):
        pesoTotale= 0
        for i in range(0,len(listaNodi)):
            u= listaNodi[i]
            v= listaNodi[i+1]
            pesoTotale += self._grafo[u][v]["peso"]
        return pesoTotale



