
class Statistic:
    def __init__(self):
        self.statistic = []


    def add(self, statistic):
        self.statistic.append(statistic)


    def print_statistic(self):
        print(
            f"Minimal: {min(self.statistic)}; maximal: {max(self.statistic)}; mittlerer Wert: {sum(self.statistic) / len(self.statistic):.2f}")
