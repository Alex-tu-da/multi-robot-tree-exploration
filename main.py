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
    12: [24, 25],
    17: [26, 27],
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
    Robot(name="i"),
    Robot(name="ii"),
    Robot(name="iii"),
    Robot(name="iv"),
    Robot(name="v"),
    Robot(name="vi"),
    Robot(name="vii"),
    Robot(name="viii"),
    Robot(name="ix"),
    Robot(name="x")
]

gruppe = Gruppe(roboter, start=0, x=0, y=0)



sim = MultiRobotSimulator(baum, gruppe, ziel)
sim.animate(steps_robot=10)