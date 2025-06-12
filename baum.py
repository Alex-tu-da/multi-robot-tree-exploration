

class Baum:
    def __init__(self):
        self.knoten = set()
        self.kanten = {}  # Eltern -> [Kinder]
        self.pos = {}         # Knotennummer -> (x, y)
        self.knoten_farben = {}


    def setze_farbe(self, knoten, farbe):
        self.knoten_farben[knoten] = farbe

    def getColor(self, knote):
        return self.knoten_farben.get(knote)

    def getKinder(self, knote):
        return self.kanten[knote]

    def finde_eltern(self, kind):
        for eltern, kinder in self.kanten.items():
            if kind in kinder:
                return eltern
        return None

    def füge_knoten_hinzu(self, knoten):
        self.knoten.add(knoten)
        if knoten not in self.kanten:
            self.kanten[knoten] = {}

    def füge_kante_hinzu(self, eltern, kind):
        self.füge_knoten_hinzu(eltern)
        self.füge_knoten_hinzu(kind)
        if eltern not in self.kanten:
            self.kanten[eltern] = {}
        self.kanten[eltern][kind] = 'g'

    def lösche_kante(self, eltern, kind):
        if eltern in self.kanten and kind in self.kanten[eltern]:
            self.kanten[eltern].remove(kind)


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




