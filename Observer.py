class Observable:
    def __init__(self):
        self.value = None
        self.observateurs = []
    def addObservateur(self, observateur):
        self.observateurs.append(observateur)
    def add(self, value):
        self.set(self.value+value)
    def set(self, value):
        self.value = value
        self.notifyAll()
    
class TimeObservable(Observable):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.oldTime = self.value
    def notifyAll(self):
        for observateur in self.observateurs:
            observateur.setTime(observateur.time().addSecs(self.value-self.oldTime))
        self.oldTime = self.value
                
class SeaDataObservable(Observable):
    def __init__(self):
        super().__init__()
    def notifyAll(self):
        for observateur in self.observateurs:
            observateur.updateView(self.value)

class AppStatusObservable(Observable):
    def __init__(self):
        super().__init__()
        self.value = 'loading'
    def notifyAll(self):
        for observateur in self.observateurs:
            observateur.updateView(self.value)

class Observateur:
    def __init__(self):
        self.observer = None
