from arts_mia.model.model import Model

model = Model()
# qui dovrei aver già letto gli oggetti
print(model._objects_dict[1234])

model.buildGrafo()
print(model._grafo)

percorsoMigliore, pesoMigliore = model.getPercorsoMassimo(1234, 15)
print(f"pesoMigliore: {pesoMigliore}")
print(percorsoMigliore)

