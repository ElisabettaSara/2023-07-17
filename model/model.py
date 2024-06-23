import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.listYear = []
        self.listColor = []

        self.grafo = nx.Graph()
        self.nodes = []
        self.edges = []
        self.idMap = {}

        self._bestPath = []

        self.loadYear()
        self.loadColor()

    def getBestPath(self, v0):
        self._bestPath = []
        parziale = [v0]
        pesi = []
        archi_visitati = []
        self._ricorsione(parziale, pesi, archi_visitati)

        return self._bestPath

    def _ricorsione(self, parziale, pesi, archi_visitati):
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        vicini = sorted(self.grafo[parziale[-1]], key=lambda x: self.grafo[parziale[-1]][x]['weight'])

        for v in vicini:
            if (not pesi or self.grafo[parziale[-1]][v]['weight'] >= max(pesi)) and (parziale[-1], v) not in archi_visitati and (v, parziale[-1]) not in archi_visitati:
                pesi.append(self.grafo[parziale[-1]][v]['weight'])
                archi_visitati.append((parziale[-1], v))
                parziale.append(v)
                self._ricorsione(parziale, pesi, archi_visitati)
                pesi.pop()
                archi_visitati.pop()
                parziale.pop()
    def loadYear(self):
        self.listYear = DAO.getYears()

    def loadColor(self):
        self.listColor = DAO.getColors()

    def builGraph(self, colore, anno):
        self.grafo.clear()
        self.nodes = DAO.getNodes()
        self.grafo.add_nodes_from(self.nodes)
        for n in self.nodes:
            self.idMap[n.Product_number] = n

        self.edges = DAO.getConnection(self.idMap, colore, anno)
        for e in self.edges:
            self.grafo.add_edge(e[0], e[1], weight=e[2])

    def getGraphSize(self):
        return len(self.nodes), len(self.edges)

    def getBestProduct(self):
        tmp = sorted(self.edges, key=lambda x: x[2], reverse=True)[:3]
        count = {}
        for e in tmp:
            if e[0] not in count:
                count[e[0]] = 1
            else:
                count[e[0]] += 1

            if e[1] not in count:
                count[e[1]] = 1
            else:
                count[e[1]] += 1
        tmp2 = []
        for element in count:
            if count[element] > 1:
                tmp2.append(element.Product_number)

        return tmp, tmp2
