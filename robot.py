import random
import plotly.graph_objects as go
from baum import Baum

class Robot:
    def __init__(self, name, color, baum, start, steps_pro_kante=10):
        self.name = name
        self.color = color
        self.baum = baum
        self.start = start
        self.steps_per_edge = steps_pro_kante
        self.baum._berechne_positionen()
        self.positionen = baum.pos
        self.pfad = self.random_pfad()

    def random_pfad(self):
        import random
        pfad = [self.start]
        aktueller = self.start
        besucht = set([aktueller])
        while True:
            kinder = [k for k in self.baum.kanten.get(aktueller, []) if k not in besucht]
            if not kinder:
                break
            nächster = random.choice(kinder)
            pfad.append(nächster)
            besucht.add(nächster)
            aktueller = nächster
        return pfad

    def get_positions(self):
        # Gibt interpolierte Positionen entlang des Pfads zurück
        pos_liste = []
        for i in range(len(self.pfad) - 1):
            k1, k2 = self.pfad[i], self.pfad[i + 1]
            x1, y1 = self.positionen[k1]
            x2, y2 = self.positionen[k2]
            for s in range(self.steps_per_edge + 1):
                t = s / self.steps_per_edge
                xt = (1 - t) * x1 + t * x2
                yt = (1 - t) * y1 + t * y2
                pos_liste.append((xt, yt))
        return pos_liste
