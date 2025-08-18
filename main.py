import gruppe
from MultiRobotSimulator import MultiRobotSimulator
from baum import Baum
from dynamischeSim import dynamischeSim
from gruppe import Gruppe
from robot import Robot
from robot1 import Robot1
from statistic import Statistic

# Geraden
gerade2 ={
    0: [1],
    1: [2],
    2: [3]
}
gerate4={
    0: [1],
    1: [2],
    2: [3]
}

# Höhe 3
baum3 ={
    0: [1],               # Wurzel hat nur ein Kind

    1: [2, 3, 4],         # Ebene 1

    2: [5, 6, 7],         # Ebene 2
    3: [8, 9, 10],
    4: [11, 12, 13],
}
# Höhe 4
baum4 = {
    0: [1],               # Höhe 0 (Wurzel)

    1: [2, 3, 4],         # Höhe 1

    2: [5, 6, 7],         # Höhe 2
    3: [8, 9, 10],
    4: [11, 12, 13],

    5: [14, 15, 16],      # Höhe 3
    6: [17, 18, 19],
    7: [20, 21, 22],
    8: [23, 24, 25],
    9: [26, 27, 28],
    10: [29, 30, 31],
    11: [32, 33, 34],
    12: [35, 36, 37],
    13: [38, 39, 40],
}
# Höhe 5
baum5 = {
    0: [1],               # Höhe 0 (Wurzel)

    1: [2, 3, 4],         # Höhe 1

    2: [5, 6, 7],         # Höhe 2
    3: [8, 9, 10],
    4: [11, 12, 13],

    5: [14, 15, 16],      # Höhe 3
    6: [17, 18, 19],
    7: [20, 21, 22],
    8: [23, 24, 25],
    9: [26, 27, 28],
    10: [29, 30, 31],
    11: [32, 33, 34],
    12: [35, 36, 37],
    13: [38, 39, 40],

    14: [41, 42, 43],     # Höhe 4
    15: [44, 45, 46],
    16: [47, 48, 49],
    17: [50, 51, 52],
    18: [53, 54, 55],
    19: [56, 57, 58],
    20: [59, 60, 61],
    21: [62, 63, 64],
    22: [65, 66, 67],
    23: [68, 69, 70],
    24: [71, 72, 73],
    25: [74, 75, 76],
    26: [77, 78, 79],
    27: [80, 81, 82],
    28: [83, 84, 85],
    29: [86, 87, 88],
    30: [89, 90, 91],
    31: [92, 93, 94],
    32: [95, 96, 97],
    33: [98, 99, 100],
    34: [101, 102, 103],
    35: [104, 105, 106],
    36: [107, 108, 109],
    37: [110, 111, 112],
    38: [113, 114, 115],
    39: [116, 117, 118],
    40: [119, 120, 121]

    # Höhe 5 Blätter (keine Kinder mehr)
}
baum5_1 = {
    0: [1],               # Höhe 0 (Wurzel)

    1: [2, 3, 4],         # Höhe 1

    2: [5, 6, 7],         # Höhe 2
    3: [8, 9, 10],
    4: [11, 12, 13],

    5: [14, 15, 16],      # Höhe 3
    6: [17, 18, 19],
    7: [20, 21, 22],
    9: [23, 24, 25],
    10: [26, 27, 28],
    12: [29, 30, 31],
    13: [32, 33, 34],

    14: [35, 36, 37],
    15: [38, 39, 40],
    16: [41, 42, 43],
    17: [44, 45, 46],
    18: [47, 48, 49],
    19: [50, 51, 52],
    20: [53, 54, 55],
    21: [56, 57, 58],
    22: [59, 60, 61],
    23: [62, 63, 64],
    24: [65, 66, 67],
    25: [68, 69, 70],
    26: [71, 72, 73],
    27: [74, 75, 76],
    28: [77, 78, 79],
    29: [80, 81, 82],
    30: [83, 84, 85],


}

kanten0 = {
    0: [1],
    1: [2, 3, 4],
    2: [5, 6, 7],
    5: [8,9],
    6: [10],
    7: [11,12],
    8: [13,14],
    9: [15],
    11: [16,17,18],
    12: [19],
    14: [20,21],
}

kanten1 = {
    0: [1],
    1: [2, 3, 4],
    2: [5, 6, 7],
    3: [8, 9],
    4: [10, 11],
    5: [12, 13],
    7: [14, 15],
    11: [16, 17],
    14: [18, 19, 20],
    16: [21, 22, 23],
    17: [24, 25],
    18: [26, 27],
    20: [28],
    25: [29, 30],
    27: [31]
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

def simulation (statistic_f, anzahl_sim, stat_rob, anzahl_rob, ziel, kanten, max_time, obPrint, durchfällePrint, statisches_ziel):
    if statistic_f:
        for i in range(stat_rob):
            statistic = Statistic(max_time, anzahl_sim)
            for j in range(anzahl_sim):

                roboter = [Robot(name=f"R{i}") for i in range(anzahl_rob + i)]

                # Baum darstellen
                baum = Baum()
                for eltern, kinder in kanten.items():
                    for kind in kinder:
                        baum.füge_kante_hinzu(eltern, kind)
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
            # Baum darstellen
            baum = Baum()
            for eltern, kinder in kanten.items():
                for kind in kinder:
                    baum.füge_kante_hinzu(eltern, kind)

            roboter = [Robot(name=f"R{i}") for i in range(anzahl_rob)]
            gruppe = Gruppe(roboter, start=0, x=0, y=0)

            roboter1 = []
            for i in range(anzahl_rob):
                roboter1.append(Robot1([0,0]))

            if statisches_ziel:
                sim = MultiRobotSimulator(baum, gruppe, ziel, None, max_time, obPrint, durchfällePrint)
            else:
                sim = dynamischeSim(baum, roboter1, ziel, max_time, obPrint)

            sim.animate(steps_robot=10, anzahl_sim=anzahl_sim, statisches_ziel=statisches_ziel)

simulation(False, 1,10, 13, 42, baum5, 500, True, True, False)