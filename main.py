"""Startpunkt für die Multi-Robot-Baum-Exploration-Simulation.

Beispiel-Baumstrukturen liegen in `beispielbaeume.py`.
"""

from baum import Baum
from beispielbaeume import baum5
from dynamischeSim import dynamischeSim
from gruppe import Gruppe
from MultiRobotSimulator import MultiRobotSimulator
from robot import Robot
from robot1 import Robot1
from statistic import Statistic


def baum_aus_kanten(kanten):
    """Baut ein Baum-Objekt aus einem Dict {Eltern-Knoten: [Kind-Knoten, ...]}."""
    baum = Baum()
    for eltern, kinder in kanten.items():
        for kind in kinder:
            baum.füge_kante_hinzu(eltern, kind)
    return baum


def alle_knoten(kanten):
    """Liefert alle Knotennummern, die in einem Kanten-Dict vorkommen."""
    knoten = set(kanten.keys())
    for kinder in kanten.values():
        knoten.update(kinder)
    return knoten


def simulation(statistic_f, anzahl_sim, stat_rob, anzahl_rob, ziel, kanten, max_time,
               obPrint, durchfällePrint, statisches_ziel):
    """Startet die Simulation.

    Args:
        statistic_f: Bei True werden mehrere Simulationen ohne Live-Animation
            gerechnet und statistisch ausgewertet (min/max/Mittelwert der
            Schritte, Anzahl "Durchfälle" = Zeitüberschreitungen).
        anzahl_sim: Anzahl der Simulationsläufe pro Roboteranzahl.
        stat_rob: Anzahl unterschiedlicher Roboteranzahlen, die getestet
            werden (nur relevant, wenn statistic_f True ist).
        anzahl_rob: Basis-Anzahl an Robotern in der Gruppe.
        ziel: Nummer des Zielknotens im Baum.
        kanten: Dict {Eltern-Knoten: [Kind-Knoten, ...]}, das den Baum
            beschreibt (siehe beispielbaeume.py).
        max_time: Maximale Anzahl Schritte, bevor eine Simulation als
            "durchgefallen" gilt.
        obPrint: Bei True wird der Simulationsverlauf auf der Konsole
            ausgegeben (nur bei einem einzelnen Lauf, statistic_f=False).
        durchfällePrint: Bei True wird auch für einen "durchgefallenen" Lauf
            die Animation angezeigt.
        statisches_ziel: Bei True bleibt der Zielknoten fest
            (MultiRobotSimulator). Bei False bewegt sich ein simulierter
            Ziel-Roboter durch den Baum (dynamischeSim).

    Raises:
        ValueError: Wenn `ziel` kein Knoten des übergebenen Baums (`kanten`) ist.
    """
    knoten = alle_knoten(kanten)
    if ziel not in knoten:
        raise ValueError(
            f"Zielknoten {ziel} kann nicht im Baum stehen: der Baum enthält "
            f"nur die Knoten {min(knoten)} bis {max(knoten)}."
        )

    if statistic_f:
        for i in range(stat_rob):
            statistic = Statistic(max_time, anzahl_sim)
            for j in range(anzahl_sim):
                roboter = [Robot(name=f"R{i}") for i in range(anzahl_rob + i)]

                baum = baum_aus_kanten(kanten)
                baum.setze_farbe(ziel, 'blue')

                gruppe = Gruppe(roboter, start=0, x=0, y=0)
                sim = MultiRobotSimulator(baum, gruppe, ziel, statistic, max_time, obPrint, durchfällePrint)
                sim.animate(steps_robot=10, anzahl_sim=anzahl_sim)

                if j == anzahl_sim - 1:
                    print()
                    print(f"Anzahl Roboter: {len(roboter) + 1}")

            statistic.print_statistic()
    else:
        for i in range(anzahl_sim):
            baum = baum_aus_kanten(kanten)

            roboter = [Robot(name=f"R{i}") for i in range(anzahl_rob)]
            gruppe = Gruppe(roboter, start=0, x=0, y=0)

            roboter1 = [Robot1([0, 0]) for _ in range(anzahl_rob)]

            if statisches_ziel:
                sim = MultiRobotSimulator(baum, gruppe, ziel, None, max_time, obPrint, durchfällePrint)
            else:
                sim = dynamischeSim(baum, roboter1, ziel, max_time, obPrint)

            sim.animate(steps_robot=10, anzahl_sim=anzahl_sim, statisches_ziel=statisches_ziel)


if __name__ == "__main__":
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
        statisches_ziel=False,
    )
