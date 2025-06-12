import math
import random


class MultiRobotSimulator:
    def __init__(self, baum, roboter_liste, ziel):
        self.baum = baum
        self.robots = roboter_liste
        self.max_len = max(len(r.get_positions()) for r in roboter_liste)

        self.graph = baum.kanten
        self.ziel = ziel


    ### Graph Methoden ###
    def getEltern(self, node):
        for eltern, kinder in self.graph.items():
            if node in kinder:
                return eltern
        return None  # steht außerhalb der Schleife

    def animate(self, steps_robot):
        import plotly.graph_objects as go

        edge_x, edge_y = [], []
        for eltern, kinder in self.baum.kanten.items():
            for kind in kinder:
                x0, y0 = self.baum.pos[eltern]
                x1, y1 = self.baum.pos[kind]
                edge_x += [x0, x1, None]
                edge_y += [y0, y1, None]

        node_x = [self.baum.pos[k][0] for k in self.baum.knoten]
        node_y = [self.baum.pos[k][1] for k in self.baum.knoten]
        color_node =  [self.baum.getColor(k) for k in self.baum.knoten]
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
        for r in self.robots:
            x, y = 0, 0
            fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers+text',
                                     marker=dict(size=30, color=r.color),
                                     text=[r.name], textposition="top center"))



        # Frames generieren
        frames = []
        for t in range(self.max_len):



            frame_data = [
                go.Scatter(x=edge_x, y=edge_y, mode='lines',
                           line=dict(color='black', width=2)),
                go.Scatter(x=node_x, y=node_y, mode='markers+text',
                           marker=dict(size=20, color=color_node),
                           text=node_text, textposition="top center")
            ]

            for r in self.robots:

                if r.current == r.target:
                    node = r.current

                    print(f"Am Ziel: {node}")
                    print(self.graph[node])

                    kinder = {k: v for k, v in self.graph[node].items() if v != 'r'}
                    if len(kinder) != 0:
                        kinder_g = [k for k, v in kinder.items() if v == 'g']
                        if len(kinder_g) != 0:
                            zufall = random.choice(kinder_g)
                            self.graph[node][zufall] = 'y'
                            color_node[node] = 'yellow'
                            r.target = zufall
                        else:
                            kinder_y = [k for k, v in kinder.items() if v == 'y']
                            zufall = random.choice(kinder_y)
                            r.target = zufall
                    else:

                        if r.current != self.ziel:
                            eltern = self.getEltern(node)
                            r.target = eltern
                            self.graph[eltern][r.current] = 'r'
                            color_node[node] = 'red'
                else:
                    ziel_x, ziel_y = node_x[r.target], node_y[r.target]
                    r.x += (node_x[r.target]- node_x[r.current]) /steps_robot
                    r.y += (node_y[r.target] - node_y[r.current]) /steps_robot

                    if math.isclose(r.x, ziel_x, abs_tol=0.01) and math.isclose(r.y, ziel_y, abs_tol=0.01):
                        r.x = ziel_x
                        r.y = ziel_y
                        r.current = r.target



                frame_data.append(go.Scatter(x=[r.x], y=[r.y], mode='markers+text',
                                             marker=dict(size=30, color=r.color),
                                             text=[r.name], textposition="top center"))




            frames.append(go.Frame(data=frame_data, name=f"f{t}"))

        # Slider
        steps = [{
            "label": f"{i}",
            "method": "animate",
            "args": [[f"f{i}"], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}]
        } for i in range(self.max_len)]

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
