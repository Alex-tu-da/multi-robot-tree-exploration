
class Gruppe:
    def __init__(self, roboter):
        self.head = roboter[0]
        roboter[0].role = 'Head'
        self.folower = roboter[1:]
        self.anzahl = len(roboter)
        self.color = 'black'
        for r in self.folower:
            r.role = 'Folower'

    def print(self):
        ausgabe = f"Head: {self.head.name};  {self.anzahl - 1} Folower:"
        if self.folower:
            for r in range(len(self.folower) ):
                ausgabe += f" {self.folower[r].name}"
        print(ausgabe)