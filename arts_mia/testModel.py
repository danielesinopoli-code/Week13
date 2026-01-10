from arts_mia.model.model import Model

model = Model()
# qui dovrei aver già letto gli oggetti
print(model._objects_dict[1234])

model.buildGrafo()
print(model._grafo)
