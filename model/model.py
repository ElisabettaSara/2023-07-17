import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self.idMap={}
        self.nodi=[]
        self.distanzaMax=0
        self.bestSol=[]



    def searchPath(self, v0):
        parziale=[v0]
        pesi=[0]
        archi_visitati=[]
        self.ricorsione(parziale,pesi,archi_visitati)
        print(self.bestSol)



    def ricorsione(self, parziale,pesi,archi_visitati):
        last= parziale[-1]
        vicini = sorted(self._grafo[last], key=lambda x: self._grafo[last][x]['weight'])

        vicini_utilizzabili = []
        for v in vicini:
            if (last, v) not in archi_visitati and (v, last) not in archi_visitati and self._grafo[last][v]['weight'] >= max(pesi):
                vicini_utilizzabili.append(v)

        if len(vicini_utilizzabili) == 0:
            if len(archi_visitati)  > self.distanzaMax:
                self.distanzaMax = len(archi_visitati)
                self.bestSol=copy.deepcopy(archi_visitati)
            return

        for v in vicini_utilizzabili:
            pesi.append(self._grafo[last][v]['weight'])
            archi_visitati.append((last, v))
            parziale.append(v)

            self.ricorsione(parziale, pesi, archi_visitati)

            pesi.pop()
            archi_visitati.pop()
            parziale.pop()



    def getAnno(self):
        return DAO.getAnno()

    def getColore(self):
        return DAO.getColore()


    def creaGrafo(self, colore,anno):
        self._grafo.clear()
        self._grafo.add_nodes_from(DAO.getProdotti(colore))
        self.nodi=DAO.getProdotti(colore)

        # for n in DAO.getProdotti(colore):
        #     self.idMap[n.Product_number]=n
        #     self._grafo.add_node(n)

        for e in DAO.getEdges(colore, anno):
            #print(e)
            self._grafo.add_edge(e[0], e[1], weight=e[2])

    def getArchiPM(self):
        archi=[]
        for e in self._grafo.edges:
            archi.append((e[0],e[1],self._grafo[e[0]][e[1]]['weight']))

        ordinati = sorted(archi, key=lambda x: x[2], reverse=True)
        tre= ordinati[0:3]
        #print(tre)
        nodi=[]
        for i in range(len(tre)-1):
            for j in range(i+1, len(tre)):
                if tre[i][0] in tre[j]:
                    if tre[i][0] not in nodi:
                        nodi.append(tre[i][0])
                if tre[i][1] in tre[j]:
                    if tre[i][1] not in nodi:
                        nodi.append(tre[i][1])
        return tre, nodi








    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)