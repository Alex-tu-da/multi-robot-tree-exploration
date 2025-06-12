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

    def animate(self):
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
            x, y = r.get_positions()[0]
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

            #print(self.graph[1])
            #self.graph[1].remove(4)
            #print(self.graph[1])

            for r in self.robots:
                pos = r.get_positions()
                i = min(t, len(pos) - 1)
                xt, yt = pos[i]

                frame_data.append(go.Scatter(x=[xt], y=[yt], mode='markers+text',
                                             marker=dict(size=30, color=r.color),
                                             text=[r.name], textposition="top center"))

                for i in range(len(node_text)):



                    if node_x[i] == xt and node_y[i] == yt:


                        if len(self.graph[i]) == 0:
                            if i != self.ziel:
                                r.color = 'red'
                                color_node[i] = 'red'

                                if self.getEltern(i) is not None:
                                    self.graph[self.getEltern(i)].remove(i)
                        else:
                            color_node[i] = 'yellow'



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
