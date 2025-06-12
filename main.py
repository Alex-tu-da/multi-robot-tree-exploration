from MultiRobotSimulator import MultiRobotSimulator
from baum import Baum
from robot import Robot

baum = Baum()
baum.füge_kante_hinzu(0, 1)

baum.füge_kante_hinzu(1, 2)
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


roboter = [
    Robot(name="1", color="red", baum=baum, start=0),
    Robot(name="2", color="green", baum=baum, start=0),
    Robot(name="3", color="orange", baum=baum, start=0)
]

sim = MultiRobotSimulator(baum, roboter)
sim.animate()