import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        anni = self._model.listYear
        colori = self._model.listColor

        for a in anni:
            self._view._ddyear.options.append(ft.dropdown.Option(a))

        for c in colori:
            self._view._ddcolor.options.append(ft.dropdown.Option(c))

    def handle_graph(self, e):
        if self._view._ddyear.value is None:
            self._view.create_alert("Inserire un anno")
            return

        if self._view._ddcolor.value is None:
            self._view.create_alert("Inserire un colore")
            return

        self._model.builGraph(self._view._ddcolor.value, self._view._ddyear.value)
        nN, nE = self._model.getGraphSize()
        product, ripetuti = self._model.getBestProduct()
        self._view.txtOut.clean()
        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {nN}  Numero di archi: {nE}"))
        for e in product:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {e[0].Product_number} a {e[1].Product_number}, peso={e[2]}"))

        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono {ripetuti}"))

        prodotti = self._model.nodes
        for n in prodotti:
            self._view._ddnode.options.append(ft.dropdown.Option(n.Product_number))
        self._view.btn_search.disabled = False

        self._view.update_page()

    def handle_search(self, e):
        v0 = self._model.idMap[int(self._view._ddnode.value)]
        bestPath = self._model.getBestPath(v0)
        self._view.txtOut2.clean()
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo: {len(bestPath)-1}"))
        self._view.update_page()
