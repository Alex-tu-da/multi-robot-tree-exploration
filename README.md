# Multi-Robot Tree Exploration

Simulation einer Gruppe von Robotern, die gemeinsam einen Baum-Graphen
erkunden, um einen Zielknoten zu finden. Roboter-Gruppen teilen sich an
Verzweigungen auf, markieren besuchte Kanten farblich (grün → gelb → rot bei
Sackgassen) und hinterlassen "Ampel"-Roboter, um Redundanz zu vermeiden. Die
Simulation wird als interaktive [Plotly](https://plotly.com/python/)-Animation
mit Zeit-Slider dargestellt.

## Installation

```bash
pip install -r requirements.txt
```

## Ausführen

```bash
python main.py
```

Öffnet eine Plotly-Animation im Browser. Welcher Baum simuliert wird und mit
wie vielen Robotern, wird über den Aufruf von `simulation(...)` am Ende von
`main.py` gesteuert (siehe Docstring dort für alle Parameter).

## Zwei Simulationsmodi

- **Statisches Ziel** (`statisches_ziel=True`, [`MultiRobotSimulator.py`](MultiRobotSimulator.py)):
  Der Zielknoten steht fest, die Roboter erkunden den Baum systematisch bis
  eine Gruppe ihn erreicht.
- **Dynamisches Ziel** (`statisches_ziel=False`, [`dynamischeSim.py`](dynamischeSim.py)):
  Ein simulierter "Ziel-Roboter" bewegt sich selbst durch den Baum und
  versucht, den suchenden Robotern auszuweichen.

## Projektstruktur

| Datei | Zweck |
|---|---|
| `main.py` | Einstiegspunkt, startet eine Simulation |
| `beispielbaeume.py` | Beispiel-Baumstrukturen als Kanten-Dicts |
| `baum.py` | `Baum`-Klasse (Graph-Struktur, Layout-Berechnung) |
| `MultiRobotSimulator.py` | Simulator für den statischen-Ziel-Modus |
| `dynamischeSim.py` | Simulator für den dynamischen-Ziel-Modus |
| `gruppe.py` / `gruppe1.py` | Roboter-Gruppen (Head/Ampel/WHead-Rollen) |
| `robot.py` / `robot1.py` | Einzelner Roboter |
| `zielRobot.py` | Der sich bewegende Ziel-Roboter (dynamischer Modus) |
| `statistic.py` | Sammelt min/max/Mittelwert über mehrere Simulationsläufe |
