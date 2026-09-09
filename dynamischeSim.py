import math
import random
import numpy as np
import plotly.graph_objects as go
from gruppe1 import Gruppe1, isVereinen, vereinen
from collections import defaultdict
from robot1 import Robot1
from zielRobot import zielRobot

class dynamischeSim:
    def __init__(self, baum, anzahl_rob, ziel, max_steps, obPrint):
        self.baum = baum
        self.baum._berechne_positionen()
        self.graph = baum.kanten
        self.gruppen = []
        if anzahl_rob:
            self.gruppen = [Gruppe1(anzahl_rob, 'Head', 0, 1)]
        self.ziel_robot = zielRobot(ziel, self.baum.pos[ziel][0], self.baum.pos[ziel][1])
        self.max_steps = max_steps
        self.ende = False
        self.obPrint = obPrint
        self.fig, self.edge_x, self.edge_y, self.node_x, self.node_y, self.color_node, self.node_text = self.create_base_figure()

    ### Methoden ###
    ### Hilfsmethoden
    def create_base_figure(self):
        edge_x, edge_y = [], []
        for eltern, kinder in self.baum.kanten.items():
            for kind in kinder:
                x0, y0 = self.baum.pos[eltern]
                x1, y1 = self.baum.pos[kind]
                edge_x += [x0, x1, None]
                edge_y += [y0, y1, None]

        node_x = [self.baum.pos[k][0] for k in self.baum.knoten]
        node_y = [self.baum.pos[k][1] for k in self.baum.knoten]
        color_node = [self.baum.getColor(k) or 'green' for k in self.baum.knoten]
        node_text = [str(k) for k in self.baum.knoten]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y, mode='lines',
            line=dict(color='black', width=2),
            hoverinfo='none'
        ))
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y, mode='markers+text',
            marker=dict(size=20, color=color_node),
            text=node_text, textposition="top center"
        ))

        return fig, edge_x, edge_y, node_x, node_y, color_node, node_text
    def getEltern(self, node):
        for eltern, kinder in self.graph.items():
            if node in kinder:
                return eltern
        return None  # steht außerhalb der Schleife
    def knote_color(self, color, eltern, g):
        if color == 'r':
            self.graph[eltern][g.current] = 'r'
            self.color_node[g.current] = 'red'
        elif color == 's':
            self.graph[eltern][g.current] = 's'
            self.color_node[g.current] = 'black'
        elif color == 'y':
            self.graph[eltern][g.current] = 'y'
            self.color_node[g.current] = 'yellow'

    ### Robot Methoden
    def pfad_finden(self, start, ziel):
        start1 = start

        ergebnis1 = []
        ergebnis2 = [ziel]
        eltern = {}

        for parent, kinder in self.graph.items():
            for child in kinder:
                eltern[child] = parent

        while start in eltern:
            parent = eltern[start]
            ergebnis1.append(parent)
            start = parent

        while ziel in eltern:
            parent = eltern[ziel]
            ergebnis2.append(parent)
            ziel = parent

        if start1 in ergebnis2:
            idx = ergebnis2.index(start1)
            ergebnis = ergebnis2[:idx]
            ergebnis = ergebnis[::-1]
            return ergebnis

        ergebnis = []
        for i in ergebnis1:
            ergebnis.append(i)
            if i in ergebnis2:
                idx = ergebnis2.index(i)
                neue_elemente = ergebnis2[:idx][::-1]  # Umkehren
                # Nur Elemente hinzufügen, die noch nicht in ergebnis1 sind:
                for elem in neue_elemente:
                    ergebnis.append(elem)
                break  # nur beim ersten Vorkommen ausführen
        return ergebnis
    def abstandRR(self, zR, R):
        return np.sqrt((zR.getPosition()[0] - R.getPosition()[0]) ** 2
                          + (zR.getPosition()[1] - R.getPosition()[1]) ** 2)
    def abstandRKR(self, zR, R):
        return (np.sqrt((zR.getPosition()[0] - self.node_x[zR.target]) ** 2
                          + (zR.getPosition()[1] - self.node_y[zR.target]) ** 2) +
                np.sqrt((R.getPosition()[0] - self.node_x[zR.target]) ** 2
                          + (R.getPosition()[1] - self.node_y[zR.target]) ** 2))
    def move(self, g, steps_robot):
        r = g.roboter[0]
        ziel_x, ziel_y = self.node_x[g.target], self.node_y[g.target]
        if math.isclose(r.x, ziel_x, abs_tol=0.01) and math.isclose(r.y, ziel_y, abs_tol=0.01):
            r.x = ziel_x
            r.y = ziel_y
            g.current = g.target
            g.static = True
        else:
            r.x += (self.node_x[g.target] - self.node_x[g.current]) / steps_robot
            r.y += (self.node_y[g.target] - self.node_y[g.current]) / steps_robot
            g.static = False
        for i in range(len(g.roboter) - 1):
            g.roboter[i + 1].x = g.roboter[0].x
            g.roboter[i + 1].y = g.roboter[0].y
    def newAmpel(self, g, gruppen_akt, eltern):
        ampel = Gruppe1([g.roboter.pop()], 'Ampel', g.current, g.target)
        gruppen_akt.append(ampel)
    def vereinen(self):
        for g in self.gruppen:
            for gr in self.gruppen:
                if isVereinen(g, gr):
                    vereinen(g, gr)
                    self.gruppen.remove(gr)

    def bewegung(self, zier_knote, steps_robot):
        gruppen_akt = []
        for g in self.gruppen:
            if zier_knote is not None:
                pfad = self.pfad_finden(g.current, zier_knote)
                g.role = 'Head'
                if g.static:
                    g.pfad = pfad
                else:
                    if g.target in pfad:
                        g.pfad = pfad
                    else:
                        pfad.insert(0, g.current)
                        g.zurueckFahren()
                        g.pfad = pfad
                    if g.pfad:
                        g.target = g.pfad.pop(0)

            if g.target != g.current:
                self.move(g, steps_robot)
                gruppen_akt.append(g)
            else:
                if g.pfad:
                    g.target = g.pfad.pop(0)
                    gruppen_akt.append(g)
                else:
                    kinder = list({k: v for k, v in self.graph[g.current].items() if v != 'r'})
                    eltern = self.getEltern(g.current)

                    if self.color_node[g.current] == 'green' and kinder:
                        self.newAmpel(g, gruppen_akt, eltern)

                    if g.role != 'Ampel':
                        # Wenn Kinder gibt
                        if kinder:
                            gruppen_akt += self.verteilen(kinder, g)
                        # Wenn keine Kinder mehr sind
                        else:
                            self.knote_color('r', eltern, g)
                            g.target = eltern
                            gruppen_akt.append(g)
                    else:
                        if self.color_node[g.current] == 'red':
                            g.role = 'Head'
                            g.target = eltern
                        gruppen_akt.append(g)
        return gruppen_akt
    def verteilen(self, kinder, g):
        gruppen_akt = []
        k = len(kinder)  # Anzahl der Listen
        listen = defaultdict(list)
        for idx, obj in enumerate(g.roboter):
            listen[idx % k].append(obj)
        for i in range(k):
            if listen[i]:
                gruppen_akt.append(Gruppe1(listen[i], 'Head', g.current, kinder.pop()))
        return gruppen_akt

    def bewegung1(self, zier_knote, steps_robot, anzahlVonRobotern):
        gruppen_akt = []

        for g in self.gruppen:
            if zier_knote is not None:
                pfad = self.pfad_finden(g.current, zier_knote)
                if g.static:
                    g.pfad = pfad
                else:
                    if g.target in pfad:
                        g.pfad = pfad
                    else:
                        pfad.insert(0, g.current)
                        g.zurueckFahren()
                        g.pfad = pfad
                    if g.pfad:
                        g.target = g.pfad.pop(0)

            if g.target != g.current:
                self.move(g, steps_robot)
                gruppen_akt.append(g)
            else:
                if g.pfad:
                    g.target = g.pfad.pop(0)
                    gruppen_akt.append(g)
                else:
                    kinder = list({k: v for k, v in self.graph[g.current].items() if v != 'r' and v != 's'})
                    eltern = self.getEltern(g.current)

                    if kinder:
                        self.knote_color('y', eltern, g)
                        if len(g.roboter) > anzahlVonRobotern:
                            self.newAmpel(g, gruppen_akt, eltern)
                    if self.color_node[g.current] == 'black':
                        g.target = eltern
                        gruppen_akt.append(g)

                    elif g.role != 'Ampel':
                        # Wenn Kinder gibt
                        if kinder:
                            gruppen_akt += self.verteilen1(kinder, g)
                        # Wenn keine Kinder mehr sind
                        else:
                            self.knote_color('r', eltern, g)
                            g.target = eltern
                            gruppen_akt.append(g)
                    else:

                        kinder1 = list({k1: v1 for k1, v1 in self.graph[g.current].items() if v1 == 'r'})

                        if kinder1:
                            for i in kinder1:
                                anzahl1 = self.teilbaum_info(i)
                                if anzahl1[0] == anzahl1[1]:

                                    self.graph[g.current][i] = 's'
                                    self.color_node[i] = 'black'

                        kinder2 = list({k1: v1 for k1, v1 in self.graph[g.current].items() if v1 != 's'})

                        if not kinder2:

                            self.graph[eltern][g.current] = 's'
                            self.color_node[g.current] = 'black'

                            g.target = eltern
                        elif len(kinder2) == 1:
                            g.target = kinder2[0]
                            self.alleKnotenGelb(g.target, g.current, g.target, 'g')
                        elif len(kinder2) == len(kinder1):
                            self.alleKnotenGelb(g.current, eltern, g.current, 'y')


                        if g.current == g.target:

                            for i in self.gruppen:
                                if i != g and i.role == 'Ampel' and i.current == g.current:
                                    g.role = 'Head'


                        gruppen_akt.append(g)

        return gruppen_akt
    def verteilen1(self, kinder, g):
        gruppen_akt = []
        k = len(kinder)  # Anzahl der Listen
        listen = defaultdict(list)
        for idx, obj in enumerate(g.roboter):
            listen[idx % k].append(obj)
        for i in range(k):
            if listen[i]:
                gruppen_akt.append(Gruppe1(listen[i], 'Head', g.current, kinder.pop()))
        return gruppen_akt

    def bewegungSnace(self, steps_robot, anzahlVonRobotern):
        gruppen_akt = []

        for g in self.gruppen:

            if g.target != g.current:
                self.move(g, steps_robot)
                gruppen_akt.append(g)
            else:

                kinder = list({k: v for k, v in self.graph[g.current].items() if v != 'r' and v != 's'})
                eltern = self.getEltern(g.current)

                if kinder:
                    self.knote_color('y', eltern, g)

                gruppen_akt.append(g)

        return gruppen_akt




    def alleKnotenGelb(self, knote, eltern, haupt, color):
        if self.color_node[knote] != 'black':

            if color == 'y':
                self.graph[eltern][knote] = 'y'
                self.color_node[knote] = 'yellow'
            elif color == 'g':
                self.graph[eltern][knote] = 'g'
                self.color_node[knote] = 'green'

        kinder = list({k for k, v in self.graph[knote].items()})

        if kinder:
            for k in kinder:
                self.alleKnotenGelb(k, knote, haupt, color)
    def teilbaum_info(self, startknoten):
        def dfs(knoten, tiefe):
            nonlocal max_tiefe, knotenanzahl
            knotenanzahl += 1
            max_tiefe = max(max_tiefe, tiefe)
            for kind in self.graph.get(knoten, []):
                dfs(kind, tiefe + 1)

        max_tiefe = 0
        knotenanzahl = 0
        dfs(startknoten, 1)
        return knotenanzahl, max_tiefe


    ### Ziel Robot Methoden
    def moveZ(self, ziel_robot, steps_robot):
        r = ziel_robot
        ziel_x, ziel_y = self.node_x[ziel_robot.target], self.node_y[ziel_robot.target]
        if math.isclose(r.x, ziel_x, abs_tol=0.01) and math.isclose(r.y, ziel_y, abs_tol=0.01):
            r.x = ziel_x
            r.y = ziel_y
            ziel_robot.current = ziel_robot.target

        else:
            r.x += (self.node_x[ziel_robot.target] - self.node_x[ziel_robot.current]) / steps_robot
            r.y += (self.node_y[ziel_robot.target] - self.node_y[ziel_robot.current]) / steps_robot

    ### Animation
    def animate(self, steps_robot, anzahl_sim, statisches_ziel):
        self.color_node[0] = 'black'
        frames = []

        # Initial Ziel-Robot
        self.fig.add_trace(go.Scatter(x=[self.ziel_robot.x], y=[self.ziel_robot.y], mode='markers+text',
                                 marker=dict(size=20, color=self.ziel_robot.color),
                                 text=[''], textposition="middle center"))

        # Initiale Positionen der Roboter
        if self.gruppen:
            for r in self.gruppen[0].roboter:
                self.fig.add_trace(go.Scatter(x=[r.x], y=[r.y], mode='markers+text',
                                     marker=dict(size=20, color='white'),
                                     text=[len(self.gruppen[0].roboter)], textposition="middle center"))

        # Variablen
        detection = 1
        anzahlVonRobotern = 2

        # Konstanten
        t = 0
        obPrint = False

        while not self.ende:
            print()
            frame_data = [
                go.Scatter(x=self.edge_x, y=self.edge_y, mode='lines',
                           line=dict(color='black', width=2)),
                go.Scatter(x=self.node_x, y=self.node_y, mode='markers+text',
                           marker=dict(size=20, color=self.color_node),
                           text=self.node_text, textposition="top center")
            ]



            # Zielrobot bewegen und plazieren
            if not self.ziel_robot.gefangen:

                if self.ziel_robot.inGefahr:
                    print(f"Ziel-Robot ist im Gefahr! Zw. Knote {self.ziel_robot.current} und {self.ziel_robot.target}")
                    self.ziel_robot.zurueckFahren(self.node_x, self.node_y)

                if self.ziel_robot.current != self.ziel_robot.target:
                    print(f"Ziel-Robot bewegt sich zum Knoten {self.ziel_robot.target}.")
                    self.moveZ(self.ziel_robot, steps_robot)
                else:
                    kinder = list(self.graph[self.ziel_robot.current].keys())
                    eltern = self.getEltern(self.ziel_robot.current)
                    if eltern != 0:
                        kinder.append(eltern)

                    kinder = [x for x in kinder if x not in self.ziel_robot.kill_knoten]

                    if kinder:
                        print(f"Ziel-Robot ist am Knoten {self.ziel_robot.current} und wählt {kinder}.")
                        self.ziel_robot.target = random.choice(kinder)
                    else:
                        self.ziel_robot.gefangen = True
                        self.ende = True


                frame_data.append(go.Scatter(x=[self.ziel_robot.x], y=[self.ziel_robot.y], mode='markers+text',
                                             marker=dict(size=20, color=self.ziel_robot.color)))

            # Gruppen an selben Knoten vereinen
            self.vereinen()

            # Ziel identifizieren
            zier_knote = None
            for g in self.gruppen:

                abstand = self.abstandRR(self.ziel_robot, g)
                if (self.ziel_robot.target == g.current and g.static) and abstand < detection:
                    zier_knote = self.ziel_robot.current
                    self.ziel_robot.inGefahr = True
                    obPrint = True
                    print(f"Zielrobot wurde von Statik-Robot aus die Knote {g.current} am {zier_knote} gefunden!")
                elif g.current == self.ziel_robot.target and g.target == self.ziel_robot.current and abstand < detection:
                    zier_knote = self.ziel_robot.current
                    self.ziel_robot.inGefahr = True
                    obPrint = True
                    print(f"Zielrobot wurde am Pfad zu Knote {zier_knote} von Robot gefunden, der von Knote {g.current} zur Knote {g.target} fuhrte!")
                elif (self.ziel_robot.target == self.ziel_robot.current == g.target ) and abstand < detection:
                    zier_knote = self.ziel_robot.current
                    self.ziel_robot.inGefahr = True
                    obPrint = True
                    print(f"Zielrobot wurde von Robot am Knote {zier_knote} gefunden, der von Konte {g.current} zur Knote {g.target} fuhrte!")
                elif self.ziel_robot.target == g.target and self.abstandRKR(self.ziel_robot, g) < detection:
                    zier_knote = self.ziel_robot.target
                    self.ziel_robot.inGefahr = True
                    obPrint = True
                    print(f"Zielrobot wurde von Robot am {zier_knote} gefunden, der von Konte {g.current} zur Knote {g.target} fuhrte!")

            # Gruppen werden bewegt
            self.gruppen = self.bewegung1(zier_knote, steps_robot, anzahlVonRobotern)



            # Gruppen werden platziert und Print
            for g in self.gruppen:
                for r in g.roboter:
                    frame_data.append(go.Scatter(x=[r.x], y=[r.y], mode='markers+text',
                                                 marker=dict(size=20, color=r.color),
                                                 text=[len(g.roboter)], textposition="middle center"))
            for i in self.gruppen:
                p = f"Step {t}: Gruppe von {len(i.roboter)} Roboter mit {i.role}-Role! "
                if i.role == 'Head' and i.static:
                    p += f"Gruppe/Robot stehen am Knote {i.current}."
                elif i.role == 'Head' and not i.static:
                    p += f"Gruppe/Robot bewegen von Knoten {i.current} zum Knoten {i.target}."
                elif i.role == 'Ampel':
                    p += f"Robot steht am Knoten {i.current}."
                else:
                    print("Noch was!")
                print(p)
            frames.append(go.Frame(data=frame_data, name=f"f{t}"))
            t += 1
            if t > self.max_steps:
                print("Die maximale Zeit wurde überschritten!!!")
                break

        # Slider
        steps = [{
            "label": f"{i}",
            "method": "animate",
            "args": [[f"f{i}"], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}]
        } for i in range(t)]
        self.fig.update_layout(
            title="Mehrere Roboter im Baum",
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            updatemenus=[{
                "type": "buttons",
                "buttons": [{
                    "label": "Start",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}]
                }]
            }],
            sliders=[{
                "active": 0,
                "pad": {"t": 40},
                "steps": steps
            }],

        )

        self.fig.frames = frames


        if self.obPrint:
            self.fig.show()
        else:
            if obPrint:
                self.fig.show()
            else:
                print("Nicht gefangen!")