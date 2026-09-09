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

## Simulation konfigurieren und starten

Alle Eigenschaften der Simulation werden über den Aufruf von `simulation(...)`
am Ende von [`main.py`](main.py) festgelegt. Passe dort die Parameter an und
starte anschließend mit:

```bash
python3 main.py
```

Das öffnet eine interaktive Plotly-Animation im Browser.

**Parameter:**

| Parameter | Bedeutung |
|---|---|
| `statistic_f` | `True` = mehrere Läufe ohne Animation, nur statistische Auswertung (min/max/Mittelwert der Schritte). `False` = ein einzelner Lauf mit Live-Animation. |
| `anzahl_sim` | Anzahl der Simulationsläufe pro Roboteranzahl. Bei einem einzelnen animierten Lauf: `1`. |
| `stat_rob` | Nur relevant bei `statistic_f=True`: Anzahl unterschiedlicher Roboteranzahlen, die nacheinander getestet werden. |
| `anzahl_rob` | Basis-Anzahl an Robotern in der Gruppe. |
| `ziel` | Nummer des Zielknotens im Baum (siehe Knoten-Beschriftung in der Animation). |
| `kanten` | Der zu durchsuchende Baum, z. B. `baum5` aus [`beispielbaeume.py`](beispielbaeume.py) (oder `baum3`, `baum4`, `kanten0`, `kanten1`, `kanten2`). |
| `max_time` | Maximale Anzahl Schritte, bevor ein Lauf als "durchgefallen" (Timeout) gilt. |
| `obPrint` | `True` = Simulationsverlauf wird auf der Konsole mitgeloggt (nur bei einem einzelnen Lauf sinnvoll). |
| `durchfällePrint` | `True` = auch für einen durchgefallenen (getimeouteten) Lauf wird die Animation angezeigt. |
| `statisches_ziel` | `True` = Zielknoten bleibt fest (`MultiRobotSimulator`). `False` = ein simulierter Ziel-Roboter bewegt sich selbst durch den Baum (`dynamischeSim`), die suchenden Roboter verfolgen ihn. |

**Beispiel – einzelner Lauf, statisches Ziel:**

```python
simulation(
    statistic_f=False,
    anzahl_sim=1,
    stat_rob=10,
    anzahl_rob=13,
    ziel=42,
    kanten=baum5,
    max_time=500,
    obPrint=True,
    durchfällePrint=True,
    statisches_ziel=True,
)
```

**Beispiel – Statistik über mehrere Roboteranzahlen:**

```python
simulation(
    statistic_f=True,
    anzahl_sim=20,
    stat_rob=5,
    anzahl_rob=5,
    ziel=42,
    kanten=baum5,
    max_time=500,
    obPrint=False,
    durchfällePrint=False,
    statisches_ziel=True,
)
```

**Beispiel – einzelner Lauf, dynamisches Ziel:**

Ein simulierter Ziel-Roboter bewegt sich selbst durch den Baum, die
suchenden Roboter verfolgen ihn, sobald sie ihn entdecken.

```python
from beispielbaeume import kanten1

simulation(
    statistic_f=False,
    anzahl_sim=1,
    stat_rob=10,
    anzahl_rob=13,
    ziel=21,
    kanten=kanten1,
    max_time=500,
    obPrint=True,
    durchfällePrint=True,
    statisches_ziel=False,
)
```

Denk daran, den passenden Baum aus `beispielbaeume.py` zu importieren (z. B.
`from beispielbaeume import kanten1` statt `baum5`), wenn du einen anderen als
den Standardbaum nutzen willst.

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
