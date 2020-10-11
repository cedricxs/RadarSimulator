class Observable:
    def __init__(self):
        self.value = 0
        self.observateurs = []
    def addObservateur(self, observateur):
        self.observateurs.append(observateur)
    def add(self, value):
        self.value += value
        self.notifyAll()
    def notifyAll(self):
        for observateur in self.observateurs:
            observateur.setText(str(self.value))
            
            
class Observateur:
    def __init__(self):
        self.observer = None
