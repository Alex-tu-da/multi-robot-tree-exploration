import gruppe
from MultiRobotSimulator import MultiRobotSimulator
from baum import Baum
from gruppe import Gruppe
from robot import Robot


kanten = {
    0: [1],
    1: [2, 3, 4],
    2: [5, 6, 7],
    3: [8, 9],
    4: [10, 11],
    5: [12, 13],
    7: [14, 15],
    11: [16, 17],
    14: [18, 19, 20],
    16: [21, 22, 23]
}

baum = Baum()
for eltern, kinder in kanten.items():
    for kind in kinder:
        baum.füge_kante_hinzu(eltern, kind)


ziel = 18

baum.setze_farbe(ziel, 'blue')

roboter = [
    Robot(name="i", baum=baum, start=0, ziel=ziel),
    Robot(name="ii", baum=baum, start=0, ziel=ziel),
    Robot(name="iii", baum=baum, start=0, ziel=ziel),
    Robot(name="iv", baum=baum, start=0, ziel=ziel),
    Robot(name="v", baum=baum, start=0, ziel=ziel),
    Robot(name="vi", baum=baum, start=0, ziel=ziel),
    Robot(name="vii", baum=baum, start=0, ziel=ziel),
    Robot(name="viii", baum=baum, start=0, ziel=ziel),
    Robot(name="ix", baum=baum, start=0, ziel=ziel),
    Robot(name="x", baum=baum, start=0, ziel=ziel)
]

gruppe = Gruppe(roboter, start=0, x=0, y=0)



sim = MultiRobotSimulator(baum, gruppe, ziel)
sim.animate(steps_robot=10)