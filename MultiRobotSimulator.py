import math
import random
from collections import defaultdict

import plotly.graph_objects as go

from gruppe import Gruppe


class MultiRobotSimulator:
    """Simuliert eine Gruppe von Robotern, die einen Baum-Graphen ausgehend von
    der Wurzel erkundet, bis eine (Teil-)Gruppe den Zielknoten `ziel` erreicht
    oder `max_steps` überschritten wird. Erzeugt am Ende eine Plotly-Animation.
    """

    def __init__(self, baum, gruppe, ziel, statistic, max_steps, obPrint, durchfaellePrint):
        self.baum = baum
        self.baum._berechne_positionen()
        self.gruppen = []
        if gruppe is not None:
            self.gruppen.append(gruppe)
        self.graph = baum.kanten
        self.ziel = ziel

        self.max_steps = max_steps
        self.obPrint = obPrint
        self.durchfaellePrint = durchfaellePrint
        self.statistic = statistic

    ### Graph-Methoden ###
    def getEltern(self, node):
        for eltern, kinder in self.graph.items():
            if node in kinder:
                return eltern
        return None  # steht außerhalb der Schleife

    ### Bewegung ###
    def move(self, g, node_x, node_y, steps_robot):
        ziel_x, ziel_y = node_x[g.target], node_y[g.target]
        g.x += (node_x[g.target] - node_x[g.current]) / steps_robot
        g.y += (node_y[g.target] - node_y[g.current]) / steps_robot
        if math.isclose(g.x, ziel_x, abs_tol=0.01) and math.isclose(g.y, ziel_y, abs_tol=0.01):
            g.x = ziel_x
            g.y = ziel_y
            g.current = g.target

    ### Plot-Aufbau ###
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

    ### Gruppen-Logik ###
    def _merge_groups_at_same_position(self):
        """Fasst Gruppen zusammen, die sich auf derselben Kante (current -> target)
        befinden. Wandelt eine zusammengefasste Gruppe in eine wartende
        Kopf-Gruppe ('WHead') um, sobald an einer 'WAmpel' nur noch ein Pfad
        übrig ist."""
        gruppen_neu = []
        gruppen_map = defaultdict(list)
        for g in self.gruppen:
            gruppen_map[(g.current, g.target)].append(g)

        for gruppen in gruppen_map.values():
            if len(gruppen) == 1:
                gruppen_neu.append(gruppen[0])
                continue

            zusammengefasst = Gruppe([], gruppen[0].current, gruppen[0].x, gruppen[0].y)
            hat_whead = any(g.role == 'WHead' for g in gruppen)
            for g in gruppen:
                kinder = {k: v for k, v in self.graph[g.current].items() if v != 'r'}
                if hat_whead and g.role == 'Ampel':
                    g.role = 'WAmpel'
                if len(kinder) == 1 and g.role == 'WAmpel':
                    zusammengefasst.roboter += g.roboter
                    zusammengefasst.anzahl = len(zusammengefasst.roboter)
                    zusammengefasst.role = 'WHead'
                elif len(kinder) > 0:
                    if g.role in ('Ampel', 'WAmpel'):
                        gruppen_neu.append(g)
                    else:
                        zusammengefasst.roboter += g.roboter
                        zusammengefasst.anzahl = len(zusammengefasst.roboter)
                else:
                    zusammengefasst.roboter += g.roboter
                    zusammengefasst.anzahl = len(zusammengefasst.roboter)
            gruppen_neu.append(zusammengefasst)

        return gruppen_neu

    def _verteile_gruppe(self, g, ziel_kandidaten, node_x, node_y):
        """Verteilt die Roboter von g zufällig auf die gegebenen Ziel-Kandidaten
        (Kind-Knoten). Bei genau einem Roboter bleibt g eine einzelne Gruppe und
        bekommt nur ein zufälliges Ziel zugewiesen."""
        ziel_kandidaten = list(ziel_kandidaten)
        anzahl_ziele = len(ziel_kandidaten)

        if len(g.roboter) == 1:
            g.target = random.choice(ziel_kandidaten)
            return [g]

        # Sonderfall: 3 mögliche Pfade, aber nur 2 Roboter -> jeder Roboter
        # bekommt sein eigenes Ziel, ein Pfad bleibt in diesem Schritt unbesucht.
        anzahl_teilgruppen = len(g.roboter) if anzahl_ziele == 3 and len(g.roboter) == 2 else anzahl_ziele
        aufteilungen = [[] for _ in range(anzahl_teilgruppen)]
        for i, roboter in enumerate(g.roboter):
            aufteilungen[i % anzahl_ziele].append(roboter)

        neue_gruppen = []
        for teil in aufteilungen:
            zufall = random.choice(ziel_kandidaten)
            ziel_kandidaten.remove(zufall)
            gruppe = Gruppe(teil, g.current, node_x[g.current], node_y[g.current])
            gruppe.target = zufall
            neue_gruppen.append(gruppe)
        return neue_gruppen

    def _handle_head_gruppe(self, g, color_node, node_x, node_y, steps_robot):
        """Bearbeitet eine Gruppe mit Rolle 'Head': Bewegung entlang der aktuellen
        Kante, oder an einer Kreuzung: Ampel setzen, auf Kind-Knoten verteilen,
        oder bei einer Sackgasse zum Elternknoten zurückfahren."""
        if g.current != g.target:
            self.move(g, node_x, node_y, steps_robot)
            return [g]

        kinder = {k: v for k, v in self.graph[g.current].items() if v != 'r'}
        eltern = self.getEltern(g.current)

        if g.current != 0 and color_node[g.current] == 'green':
            color_node[g.current] = 'yellow'
            self.graph[eltern][g.current] = 'y'
            if len(kinder) > 0:
                if g.anzahl > 1:
                    ampel = g.roboter[-1]
                    g.roboter.remove(ampel)
                    g.anzahl -= 1
                    ampel_gruppe = Gruppe([ampel], g.current, g.x, g.y)
                    ampel_gruppe.role = 'WAmpel' if g.current == 1 else 'Ampel'
                    ampel_gruppe.current = g.current
                    ampel_gruppe.target = g.current
                    # g wird unten (mit einem Roboter weniger) weiterverarbeitet.
                    ergebnis = [ampel_gruppe]
                else:
                    g.role = 'Ampel'
                    g.target = g.current
                    return [g]
            else:
                ergebnis = []
        else:
            ergebnis = []

        if len(kinder) != 0:
            if len(kinder) == 1:
                g.target = list(kinder.keys())[0]
                ergebnis.append(g)
            else:
                kinder_g = [k for k, v in kinder.items() if v == 'g']
                kinder_y = [k for k, v in kinder.items() if v == 'y']
                kandidaten = kinder_g if kinder_g else kinder_y
                ergebnis.extend(self._verteile_gruppe(g, kandidaten, node_x, node_y))
        elif g.current != self.ziel:
            g.target = eltern
            self.graph[eltern][g.current] = 'r'
            color_node[g.current] = 'red'
            ergebnis.append(g)

        return ergebnis

    def _handle_whead_gruppe(self, g, node_x, node_y, steps_robot):
        """Bearbeitet eine wartende Kopf-Gruppe ('WHead'): folgt automatisch dem
        einzigen verbliebenen Pfad, bis das Ziel erreicht ist."""
        if g.current == g.target and g.current != self.ziel:
            kinder = {k: v for k, v in self.graph[g.current].items() if v != 'r'}
            g.target = list(kinder.keys())[0]
            return [g]
        if g.current != self.ziel:
            self.move(g, node_x, node_y, steps_robot)
            return [g]
        return []

    def _advance_groups(self, color_node, node_x, node_y, steps_robot):
        """Verarbeitet alle aktuellen Gruppen einen Simulationsschritt weiter."""
        grupp_akt = []
        for g in self.gruppen:
            if g.role == 'Head':
                grupp_akt.extend(self._handle_head_gruppe(g, color_node, node_x, node_y, steps_robot))
            elif g.role == 'WHead':
                grupp_akt.extend(self._handle_whead_gruppe(g, node_x, node_y, steps_robot))
            else:
                grupp_akt.append(g)
        return grupp_akt

    ### Debug-Ausgabe ###
    def _debug_print_gruppen(self):
        gruppen_map = defaultdict(list)
        for g in self.gruppen:
            gruppen_map[(g.current, g.target)].append(g)
        for key, gruppen in gruppen_map.items():
            gesamtanzahl = sum(g.anzahl for g in gruppen)
            rollen = [g.role for g in gruppen]
            if key[0] == key[1]:
                print(f"Position {key[0]} (statisch): {len(gruppen)} Gruppen; "
                      f"Gesamtanzahl Roboter: {gesamtanzahl}; Rollen: {rollen}")
            else:
                print(f"Position {key} (in Bewegung): {len(gruppen)} Gruppen; "
                      f"Gesamtanzahl Roboter: {gesamtanzahl}; Rollen: {rollen}")
        print()

    ### Plot-Frame ###
    def _gruppen_scatter(self, grupp_akt):
        x, y, anzahl = [], [], []
        farbe = 'white'
        for g in grupp_akt:
            x.append(g.x)
            y.append(g.y)
            anzahl.append(g.anzahl)
            farbe = g.color
        return go.Scatter(x=x, y=y, mode='markers+text',
                           marker=dict(size=20, color=farbe),
                           text=anzahl, textposition="middle center")

    def _build_slider_steps(self, anzahl_frames):
        return [{
            "label": f"{i}",
            "method": "animate",
            "args": [[f"f{i}"], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}]
        } for i in range(anzahl_frames)]

    def _apply_layout(self, fig, anzahl_frames):
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
                    "args": [None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}]
                }]
            }],
            sliders=[{
                "active": 0,
                "pad": {"t": 40},
                "steps": self._build_slider_steps(anzahl_frames),
            }],
        )

    ### Animation ###
    def animate(self, steps_robot, anzahl_sim, statisches_ziel=None):
        fig, edge_x, edge_y, node_x, node_y, color_node, node_text = self.create_base_figure()
        color_node[0] = 'black'
        color_node[self.ziel] = 'blue'
        frames = []

        # Initiale Positionen der Roboter
        for g in self.gruppen:
            fig.add_trace(go.Scatter(x=[g.x], y=[g.y], mode='markers+text',
                                     marker=dict(size=20, color=g.getColor()),
                                     text=[g.anzahl], textposition="middle center"))

        t = -1
        while len(self.gruppen) != 0:
            if anzahl_sim == 1 and self.obPrint:
                print("Step: ", t)

            frame_data = [
                go.Scatter(x=edge_x, y=edge_y, mode='lines',
                           line=dict(color='black', width=2)),
                go.Scatter(x=node_x, y=node_y, mode='markers+text',
                           marker=dict(size=20, color=color_node),
                           text=node_text, textposition="top center")
            ]

            self.gruppen = self._merge_groups_at_same_position()
            grupp_akt = self._advance_groups(color_node, node_x, node_y, steps_robot)

            if anzahl_sim == 1 and self.obPrint:
                self._debug_print_gruppen()

            if grupp_akt:
                frame_data.append(self._gruppen_scatter(grupp_akt))
            self.gruppen = grupp_akt

            frames.append(go.Frame(data=frame_data, name=f"f{t}"))
            t += 1
            if t > self.max_steps:
                if self.statistic is None:
                    print("Die maximale Zeit wurde überschritten!!!")
                break

        if anzahl_sim == 1 and self.obPrint:
            print("Steps: ", t)
        if self.statistic is not None:
            self.statistic.add(t - 1)

        self._apply_layout(fig, t)
        fig.frames = frames

        if t > self.max_steps:
            if self.statistic is not None and self.durchfaellePrint:
                fig.show()
        elif anzahl_sim == 1:
            fig.show()
