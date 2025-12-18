from flight_delays.model.model import Model

model = Model()
model.buildGraph(5)
print(model._grafo)