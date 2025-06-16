class Statistic:
    def __init__(self, max_time, anzahl_sim):
        self.statistic = []
        self.max_time = max_time
        self.durchgefallen = 0
        self.anzahl_sim = anzahl_sim

    def add(self, statistic):
        if statistic != self.max_time:
            self.statistic.append(statistic)
        else:
            self.durchgefallen += 1

    def print_statistic(self):
        if len(self.statistic) != 0:
            print(
                f"Anzahl Simulationen : {self.anzahl_sim}; Minimal: {min(self.statistic)}; maximal: {max(self.statistic)}; mittlerer Wert: {sum(self.statistic) / len(self.statistic):.2f}; Durchfälle: {self.durchgefallen}")
        else:
            print(f"Alle Simulationen {self.anzahl_sim} wurden durchgefallen!")