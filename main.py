from MultiRobotSimulator import MultiRobotSimulator
from baum import Baum
from robot import Robot

baum = Baum()
baum.füge_kante_hinzu(0, 1)

"""baum.füge_kante_hinzu(1, 2)
baum.füge_kante_hinzu(1, 3)
baum.füge_kante_hinzu(1, 4)

baum.füge_kante_hinzu(2, 5)
baum.füge_kante_hinzu(2, 6)
baum.füge_kante_hinzu(2, 7)

baum.füge_kante_hinzu(3, 8)
baum.füge_kante_hinzu(3, 9)

baum.füge_kante_hinzu(4, 10)
baum.füge_kante_hinzu(4, 11)

baum.füge_kante_hinzu(5, 12)
baum.füge_kante_hinzu(5, 13)

baum.füge_kante_hinzu(7, 14)
baum.füge_kante_hinzu(7, 15)

baum.füge_kante_hinzu(11, 16)
baum.füge_kante_hinzu(11, 17)

baum.füge_kante_hinzu(14, 18)
baum.füge_kante_hinzu(14, 19)
baum.füge_kante_hinzu(14, 20)

baum.füge_kante_hinzu(16, 21)
baum.füge_kante_hinzu(16, 22)
baum.füge_kante_hinzu(16, 23)

"""

baum.füge_kante_hinzu(1, 2)
baum.füge_kante_hinzu(1, 3)
baum.füge_kante_hinzu(1, 4)

baum.füge_kante_hinzu(2, 5)
baum.füge_kante_hinzu(2, 6)
baum.füge_kante_hinzu(2, 7)

baum.füge_kante_hinzu(3, 8)
baum.füge_kante_hinzu(3, 9)
baum.füge_kante_hinzu(3, 10)

baum.füge_kante_hinzu(4, 11)
baum.füge_kante_hinzu(4, 12)
baum.füge_kante_hinzu(4, 13)

baum.füge_kante_hinzu(5, 14)
baum.füge_kante_hinzu(5, 15)

baum.füge_kante_hinzu(6, 16)
baum.füge_kante_hinzu(6, 17)

baum.füge_kante_hinzu(7, 18)
baum.füge_kante_hinzu(7, 19)

baum.füge_kante_hinzu(11, 20)

baum.füge_kante_hinzu(12, 21)

baum.füge_kante_hinzu(13, 22)

baum.füge_kante_hinzu(20, 23)
baum.füge_kante_hinzu(20, 24)

baum.füge_kante_hinzu(21, 25)
baum.füge_kante_hinzu(21, 26)

baum.füge_kante_hinzu(22, 27)
baum.füge_kante_hinzu(22, 28)
baum.füge_kante_hinzu(22, 29)

baum.füge_kante_hinzu(25, 30)
baum.füge_kante_hinzu(25, 31)

baum.füge_kante_hinzu(26, 32)
baum.füge_kante_hinzu(26, 33)

baum.füge_kante_hinzu(27, 34)
baum.füge_kante_hinzu(27, 35)

baum.füge_kante_hinzu(34, 36)
baum.füge_kante_hinzu(34, 37)

baum.füge_kante_hinzu(36, 38)
baum.füge_kante_hinzu(36, 39)

ziel = 38

for i in range(40):
    baum.setze_farbe(i, 'green')
baum.setze_farbe(ziel, 'blue')

roboter = [
    Robot(name="1", role='Head', baum=baum, start=0, ziel=ziel),
    Robot(name="2", role='Head', baum=baum, start=0, ziel=ziel),
    Robot(name="1", role='Head', baum=baum, start=0, ziel=ziel),
    Robot(name="2", role='Head', baum=baum, start=0, ziel=ziel),
    Robot(name="3", role='Head', baum=baum, start=0, ziel=ziel)
]

sim = MultiRobotSimulator(baum, roboter, ziel)
sim.animate(steps_robot=10)