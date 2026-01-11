from arts_mia.database.DB_connect import DBConnect
from arts_mia.model.connessione import Connessione
from arts_mia.model.object import Object


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def readObjects():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM objects"
        cursor.execute(query)
        for row in cursor: # row è un dizionario
            #result.append(Object(row["object_id"], row["object_name"]))
            result.append(Object(**row)) # ** fa l'unpacking del dizionario

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def readConnessioni(objects_dict): # Riceve la idMap degli Object
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT eo1.object_id AS o1, eo2.object_id AS o2, COUNT(*) AS peso
                    FROM exhibition_objects eo1, exhibition_objects eo2 
                    WHERE eo1.exhibition_id = eo2.exhibition_id 
                    AND eo1.object_id < eo2.object_id 
                    GROUP BY eo1.object_id, eo2.object_id"""
        cursor.execute(query)

        for row in cursor:
           o1 = objects_dict[row["o1"]] #
           o2 = objects_dict[row["o2"]]
           peso = row["peso"]
           result.append(Connessione(o1, o2, peso))  #costruisce una Connessione

        cursor.close()
        conn.close()
        return result # lista di oggetti di tipo Connessione


