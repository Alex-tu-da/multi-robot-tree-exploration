import math
import random
import plotly.graph_objects as go
from gruppe import Gruppe


class MultiRobotSimulator:
    def __init__(self, baum, gruppe, ziel):
        self.baum = baum
        self.baum._berechne_positionen()


        self.gruppen = []
        self.gruppen.append(gruppe)

        self.graph = baum.kanten
        self.ziel = ziel


    ### Graph Methoden ###
    def getEltern(self, node):
        for eltern, kinder in self.graph.items():
            if node in kinder:
                return eltern
        return None  # steht außerhalb der Schleife

    def animate(self, steps_robot):

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

        # Statischer Hintergrund
        fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines',
                                 line=dict(color='black', width=2),
                                 hoverinfo='none'))
        fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text',
                                 marker=dict(size=20, color=color_node),
                                 text=node_text, textposition="top center"))

        # Initiale Positionen der Roboter
        for g in self.gruppen:
            fig.add_trace(go.Scatter(x=[g.x], y=[g.y], mode='markers+text',
                                     marker=dict(size=30, color=g.getColor()),
                                     text=[g.anzahl], textposition="middle center"))



        # Frames generieren
        frames = []
        ziel_erreicht = False
        t = 0
        while len(self.gruppen) != 0:
        #for i in range(100):

            frame_data = [
                go.Scatter(x=edge_x, y=edge_y, mode='lines',
                           line=dict(color='black', width=2)),
                go.Scatter(x=node_x, y=node_y, mode='markers+text',
                           marker=dict(size=20, color=color_node),
                           text=node_text, textposition="top center")
            ]

            grupp_akt = []
            for g in self.gruppen:

                # Robot an der Kreuzung
                if g.current == g.target:
                    kinder = {k: v for k, v in self.graph[g.current].items() if v != 'r'}

                    if color_node[g.current] == 'green':
                        print(g.current)

                    # Es gibt noch Pfade
                    if len(kinder) != 0:
                        color_node[g.current] = 'yellow'

                        # Es gibt nur ein Pfad
                        if len(kinder) == 1:
                            g.target = list(kinder.keys())[0]
                            grupp_akt.append(g)

                        # Es gibt mehrere Pfade
                        else:
                            kinder_g = [k for k, v in kinder.items() if v == 'g']

                            # Es gibt grüne Pfade
                            if len(kinder_g) != 0:

                                anzahlG = len(kinder_g)

                                # Es gibt 3 Pfade, aber 2 Roboter
                                if anzahlG == 3 and len(g.roboter) == 2:
                                    new_gruppen = [[] for _ in range(len(g.roboter))]

                                    for i, elem in enumerate(g.roboter):
                                        new_gruppen[i % anzahlG].append(elem)

                                    # Für jede neue Gruppe ein eigenes Ziel zuweisen
                                    for i in range(anzahlG):
                                        zufall = random.choice(kinder_g)
                                        kinder_g.remove(zufall)

                                        group = Gruppe(new_gruppen[i], g.current, node_x[g.current], node_y[g.current])
                                        group.target = zufall
                                        grupp_akt.append(group)

                                # Es gibt nur ein Robot
                                elif len(g.roboter) == 1:

                                    zufall = random.choice(kinder_g)
                                    kinder_g.remove(zufall)

                                    g.target = zufall
                                    grupp_akt.append(g)

                                # Normale Verteilung
                                else:

                                    new_gruppen = [[] for _ in range(anzahlG)]

                                    for i, elem in enumerate(g.roboter):
                                        new_gruppen[i % anzahlG].append(elem)

                                    # Für jede neue Gruppe ein eigenes Ziel zuweisen
                                    for i in range(anzahlG):
                                        zufall = random.choice(kinder_g)
                                        kinder_g.remove(zufall)

                                        group = Gruppe(new_gruppen[i], g.current, node_x[g.current], node_y[g.current])
                                        group.target = zufall
                                        grupp_akt.append(group)

                            # Es gibt nur gelbe Pfade
                            else:

                                kinder_y = [k for k, v in kinder.items() if v == 'y']
                                anzahlG = len(kinder_y)

                                # Es 3 Pfade, aber 2 Roboter
                                if anzahlG == 3 and len(g.roboter) == 2:
                                    new_gruppen = [[] for _ in range(len(g.roboter))]

                                    for i, elem in enumerate(g.roboter):
                                        new_gruppen[i % anzahlG].append(elem)

                                    # Für jede neue Gruppe ein eigenes Ziel zuweisen
                                    for i in range(anzahlG):
                                        zufall = random.choice(kinder_y)
                                        kinder_y.remove(zufall)

                                        group = Gruppe(new_gruppen[i], g.current, node_x[g.current], node_y[g.current])
                                        group.target = zufall
                                        grupp_akt.append(group)

                                # Es gibt nur ein Robot
                                elif len(g.roboter) == 1:

                                    zufall = random.choice(kinder_y)
                                    kinder_y.remove(zufall)

                                    g.target = zufall
                                    grupp_akt.append(g)

                                # Normale Verteilung
                                else:

                                    new_gruppen = [[] for _ in range(anzahlG)]

                                    for i, elem in enumerate(g.roboter):
                                        new_gruppen[i % anzahlG].append(elem)

                                    # Für jede neue Gruppe ein eigenes Ziel zuweisen
                                    for i in range(anzahlG):
                                        zufall = random.choice(kinder_y)
                                        kinder_y.remove(zufall)

                                        group = Gruppe(new_gruppen[i], g.current, node_x[g.current], node_y[g.current])
                                        group.target = zufall
                                        grupp_akt.append(group)

                    # Es gibt keine Pfade mehr
                    else:
                        # Kein Ziel -> zurück
                        if g.current != self.ziel:
                            eltern = self.getEltern(g.current)
                            g.target = eltern
                            self.graph[eltern][g.current] = 'r'
                            color_node[g.current] = 'red'
                            grupp_akt.append(g)
                        # Ziel!!!



                # Robot im Rohr
                else:
                    ziel_x, ziel_y = node_x[g.target], node_y[g.target]
                    g.x += (node_x[g.target]- node_x[g.current]) /steps_robot
                    g.y += (node_y[g.target] - node_y[g.current]) /steps_robot
                    if math.isclose(g.x, ziel_x, abs_tol=0.01) and math.isclose(g.y, ziel_y, abs_tol=0.01):
                        g.x = ziel_x
                        g.y = ziel_y
                        g.current = g.target

                    grupp_akt.append(g)


            # Plot die Gruppen
            x = []
            y = []
            anzahl = []
            for g in grupp_akt:
                x.append(g.x)
                y.append(g.y)
                anzahl.append(g.anzahl)
                if g == grupp_akt[-1]:
                    frame_data.append(go.Scatter(x=x, y=y, mode='markers+text',
                                             marker=dict(size=30, color=g.color),
                                             text=anzahl, textposition="middle center"))

            self.gruppen = grupp_akt


            frames.append(go.Frame(data=frame_data, name=f"f{t}"))
            t += 1

        # Slider
        steps = [{
            "label": f"{i}",
            "method": "animate",
            "args": [[f"f{i}"], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}]
        } for i in range(t)]

        fig.update_layout(
            title="Mehrere Roboter im Baum",
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            updatemenus=[{
                "type": "buttons",
                "buttons": [{
                    "label": "Start",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": 200, "redraw": True}, "fromcurrent": True}]
                }]
            }],
            sliders=[{
                "active": 0,
                "pad": {"t": 40},
                "steps": steps
            }],

        )
        fig.frames = frames
        fig.show()
