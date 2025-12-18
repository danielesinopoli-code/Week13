from flight_delays.database.DB_connect import DBConnect
from flight_delays.model.airport import Airport
from flight_delays.model.connessione import Connessione


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getNodes(min, dizionarioAeroporti):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT tmp.id, tmp.IATA_CODE, count(*) as somma
                    FROM
                    (SELECT a.id, a.IATA_CODE, f.AIRLINE_ID, COUNT(*)   
                    FROM flights f, airports a
                    WHERE a.id = f.ORIGIN_AIRPORT_ID OR
                          a.id = f.DESTINATION_AIRPORT_ID 
                    GROUP BY a.id, a.IATA_CODE, f.AIRLINE_ID) AS tmp
                    GROUP BY tmp.id, tmp.IATA_CODE 
                    HAVING somma>= %s """

        cursor.execute(query, (min, ))

        for row in cursor:
            result.append(dizionarioAeroporti[row["id"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(dizionarioAeroporti):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, COUNT(*) AS voli
                   FROM flights f 
                   GROUP BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID """

        cursor.execute(query)

        for row in cursor:
            idPartenza = row["ORIGIN_AIRPORT_ID"]
            idAarrivo = row["DESTINATION_AIRPORT_ID"]
            aPartenza = dizionarioAeroporti[idPartenza]
            aArrivo = dizionarioAeroporti[idAarrivo]
            voli = row["voli"]
            result.append(Connessione(aPartenza, aArrivo, voli))


        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getEdgesConQueryComplessa(dizionarioAeroporti):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, COALESCE(t1.n, 0) + coalesce(t2.n, 0) as voli
                    from 
                    (SELECT f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) as n FROM flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t1
                    left join 
                    (SELECT f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) as n FROM flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t2
                    on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID and t1.DESTINATION_AIRPORT_ID = t2.ORIGIN_AIRPORT_ID
                    where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is null"""

        cursor.execute(query)
        for row in cursor:
            result.append(Connessione(dizionarioAeroporti[row["ORIGIN_AIRPORT_ID"]], dizionarioAeroporti[row["DESTINATION_AIRPORT_ID"]], row["voli"]))
        cursor.close()
        conn.close()
        return result