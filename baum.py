import plotly.graph_objects as go

class Baum:
    def __init__(self):
        self.knoten = set()
        self.kanten = dict()  # Eltern -> [Kinder]
        self.pos = {}         # Knotennummer -> (x, y)

    def getKinder(self, knote):
        return self.kanten[knote]

    def füge_knoten_hinzu(self, knoten):
        self.knoten.add(knoten)
        if knoten not in self.kanten:
            self.kanten[knoten] = []

    def füge_kante_hinzu(self, eltern, kind):
        self.füge_knoten_hinzu(eltern)
        self.füge_knoten_hinzu(kind)
        self.kanten[eltern].append(kind)

    def zeige_baumstruktur(self, aktueller_knoten=None, ebene=0):
        if aktueller_knoten is None:
            kinder = {k for l in self.kanten.values() for k in l}
            wurzel = (self.knoten - kinder).pop()
            aktueller_knoten = wurzel
        print("  " * ebene + f"- {aktueller_knoten}")
        for kind in self.kanten.get(aktueller_knoten, []):
            self.zeige_baumstruktur(kind, ebene + 1)

    def _berechne_positionen(self):
        self.pos = {}

        def dfs(knoten, x, y, dx):
            self.pos[knoten] = (x, y)
            kinder = self.kanten.get(knoten, [])
            n = len(kinder)
            for i, kind in enumerate(kinder):
                offset = (i - (n - 1) / 2) * dx
                dfs(kind, x + offset, y - 1, dx / 2)

        # Wurzel finden
        kinder = {k for l in self.kanten.values() for k in l}
        wurzel = (self.knoten - kinder).pop()
        dfs(wurzel, 0, 0, 4)

    def finde_pfad(self, start, ziel):
        pfad = []
        gefunden = False

        def dfs(knoten, current_path):
            nonlocal gefunden
            if gefunden:
                return
            current_path.append(knoten)
            if knoten == ziel:
                pfad.extend(current_path)
                gefunden = True
                return
            for kind in self.kanten.get(knoten, []):
                dfs(kind, current_path)
            current_path.pop()

        dfs(start, [])
        return pfad

    def plot(self):
        self._berechne_positionen()
        edge_x = []
        edge_y = []
        for eltern, kinder in self.kanten.items():
            for kind in kinder:
                x0, y0 = self.pos[eltern]
                x1, y1 = self.pos[kind]
                edge_x += [x0, x1, None]
                edge_y += [y0, y1, None]

        node_x = [self.pos[k][0] for k in self.knoten]
        node_y = [self.pos[k][1] for k in self.knoten]
        node_text = [str(k) for k in self.knoten]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            mode='lines',
            line=dict(color='black', width=2),
            hoverinfo='none'
        ))

        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            marker=dict(size=20, color='lightblue'),
            text=node_text,
            textposition='top center',
            hoverinfo='text'
        ))

        fig.update_layout(
            title="Baumstruktur",
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white'
        )
        fig.show()
