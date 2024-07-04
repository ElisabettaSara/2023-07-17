import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        for a in self._model.getAnno():
            self._view._ddyear.options.append(ft.dropdown.Option(a))

        for c in self._model.getColore():
            self._view._ddcolor.options.append(ft.dropdown.Option(c))





    def handle_graph(self, e):
        colore= self._view._ddcolor.value
        anno = self._view._ddyear.value
        self._model.creaGrafo(colore, anno)

        self._view.txtOut.controls.append(ft.Text(f"Numero nodi={self._model.getNumNodi()} e numero archi={self._model.getNumArchi()}"))
        arc, nodi = self._model.getArchiPM()
        for i in range(len(arc)):
            self._view.txtOut.controls.append(ft.Text(f"arco da {arc[i][0]} a {arc[i][1]}, peso = {arc[i][2]}"))
        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {nodi}"))

        self._view.btn_search.disabled=False
        for n in self._model.nodi:
            self._view._ddnode.options.append(ft.dropdown.Option(n))

        self._view.update_page()




    def handle_search(self, e):
        nodo = int(self._view._ddnode.value)

        self._model.searchPath(nodo)
        soluzione = len(self._model.bestSol)
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo{soluzione}"))
        self._view.update_page()
