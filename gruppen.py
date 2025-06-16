
class Gruppen:
    def __init__(self, gruppen):

        self. anzahl = len(gruppen)
        self.ids = [1]

    def addGruppe(self, gruppe):
        self.ids.append(self.ids[len(self.ids)-1])
        self.anzahl += 1

    def deleteGruppe(self, gruppe):
        self.ids.remove(len(self.ids)-1)
        self.anzahl -= 1