import gruppe
from MultiRobotSimulator import MultiRobotSimulator
from baum import Baum
from gruppe import Gruppe
from robot import Robot
from statistic import Statistic

kanten1 = {
    0: [1],
    1: [2, 3, 4],
    2: [5, 6, 7],
    3: [8, 9],
    4: [10, 11],
    5: [12, 13],
    6: [28],
    7: [14, 15],
    8: [29],
    9: [30, 31],
    10: [32],
    11: [16, 17],
    12: [24, 25],
    13: [33],
    14: [18, 19, 20],
    15: [34],
    16: [21, 22, 23],
    17: [26, 27],
    18: [35, 36],
    20: [37],
    22: [38],
    25: [39, 40],
    27: [41],
    31: [42, 43],
    36: [44, 45]
}

kanten2 = {
    0: [1],
    1: [2, 3, 4],
    2: [5, 6, 7],
    3: [8, 9],
    4: [10, 11],
    5: [12, 13],
    6: [28, 29],
    7: [14, 15],
    8: [30],
    9: [31, 32],
    10: [33],
    11: [16, 17],
    12: [24, 25],
    13: [34, 35],
    14: [18, 19, 20],
    15: [36],
    16: [21, 22, 23],
    17: [26, 27],
    18: [37],
    19: [38, 39],
    20: [40],
    22: [41],
    24: [42, 43],
    25: [44],
    26: [45],
    27: [46, 47],
    28: [48],
    29: [49, 50],
    30: [51],
    31: [52, 53],
    32: [54],
    33: [55],
    34: [56],
    36: [57, 58],
    39: [59, 60],
    41: [61],
    44: [62],
    45: [63],
    47: [64, 65],
    50: [66],
    53: [67],
    58: [68, 69],
    60: [70],
    62: [71],
    65: [72, 73]
}



ziel = 71
anzahl_sim = 1
statistic_f = False
statistic = Statistic()



roboter = [
    Robot(name="i"),
    Robot(name="i"),
    Robot(name="i"),
    Robot(name="i"),
    Robot(name="i"),
    Robot(name="i")
]

if statistic_f:
    for i in range(0, 10):
        roboter += roboter
        print(f"Anzahl Roboter: {len(roboter)}")
        for i in range(anzahl_sim):
            baum = Baum()
            for eltern, kinder in kanten2.items():
                for kind in kinder:
                    baum.füge_kante_hinzu(eltern, kind)
            baum.setze_farbe(ziel, 'blue')
            gruppe = Gruppe(roboter, start=0, x=0, y=0)
            sim = MultiRobotSimulator(baum, gruppe, ziel, statistic)
            sim.animate(steps_robot=10, anzahl_sim=anzahl_sim)
        statistic.print_statistic()
else:
    for i in range(anzahl_sim):
        baum = Baum()
        for eltern, kinder in kanten2.items():
            for kind in kinder:
                baum.füge_kante_hinzu(eltern, kind)
        baum.setze_farbe(ziel, 'blue')
        gruppe = Gruppe(roboter, start=0, x=0, y=0)
        sim = MultiRobotSimulator(baum, gruppe, ziel, statistic)
        sim.animate(steps_robot=10, anzahl_sim=anzahl_sim)