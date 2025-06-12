from MultiRobotSimulator import MultiRobotSimulator
from baum import Baum
from gruppe import Gruppe
from robot import Robot


kanten = {
    0: [1],
    1: [2, 3, 4],
    2: [5, 6, 7],
    3: [9, 40],
    4: [11, 12, 13],
    5: [14, 15],
    6: [16, 17],
    7: [18, 19],
    11: [20, 41],
    12: [21, 8],
    13: [22, 10],
    20: [23, 24],
    21: [25, 26],
    22: [27, 28, 29],
    25: [30, 31],
    26: [32, 33],
    27: [34, 35],
    34: [36, 37],
    36: [38, 39]
}

baum = Baum()
for eltern, kinder in kanten.items():
    for kind in kinder:
        baum.füge_kante_hinzu(eltern, kind)


ziel = 38

for i in range(42):
    baum.setze_farbe(i, 'green')
baum.setze_farbe(ziel, 'blue')

roboter = [
    Robot(name="i", baum=baum, start=0, ziel=ziel),
    Robot(name="ii", baum=baum, start=0, ziel=ziel),
    Robot(name="iii", baum=baum, start=0, ziel=ziel),
    Robot(name="iv", baum=baum, start=0, ziel=ziel),
    Robot(name="v", baum=baum, start=0, ziel=ziel)
]

gruppe = Gruppe(roboter)

gruppe.print()

sim = MultiRobotSimulator(baum, roboter, ziel)
sim.animate(steps_robot=10)