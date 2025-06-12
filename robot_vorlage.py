import random
import plotly.graph_objects as go
from baum import Baum

class Robot:
    def __init__(self, name, role, baum, start, ziel, steps_pro_kante=10):
        self.name = name
        self.color = 'black'
        self.baum = baum
        self.start = start
        self.ziel = ziel

        self.role = role

        self.current = self.start
        self.target = self.start
        self.x = 0
        self.y = 0

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

            # Hole alle Kinder von 'aktueller'
            kinder = []
            alle_kinder = self.baum.getKinder(aktueller)
            # Füge nur die Kinder hinzu, die noch nicht besucht wurden
            for k in alle_kinder:
                if k not in besucht:
                    kinder.append(k)

            if not kinder:

                if aktueller == self.ziel:
                    break
                else:
                    nächster = self.baum.finde_eltern(aktueller)
                    pfad.append(nächster)
                    aktueller = nächster



            elif len(kinder) == 1:
                nächster = kinder[0]
                pfad.append(nächster)
                besucht.add(nächster)
                aktueller = nächster
            else:
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
