class nodo():
    def __init__(self, value, successors: dict):
        self.value = value
        self.successors = successors

abierta = []
cerrada = []
exito = False