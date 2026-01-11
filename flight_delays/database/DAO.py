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
    def getNodes(min,dizionarioAeroporti):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT tmp.id , tmp.IATA_CODE, COUNT(*) AS Somma
                    FROM
                    (SELECT a.id ,a.IATA_CODE ,f.AIRLINE_ID , COUNT(*)
                    FROM flights f ,airports a  
                    WHERE a.id = f.ORIGIN_AIRPORT_ID  OR
	                      a.id = f.DESTINATION_AIRPORT_ID 
                    GROUP BY a.id ,a.IATA_CODE ,f.AIRLINE_ID ) AS tmp
                    GROUP BY tmp.id , tmp.IATA_CODE  HAVING Somma >= %s
                    ORDER BY Somma ASC """

        cursor.execute(query, (min,))


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
        query = """ SELECT f.ORIGIN_AIRPORT_ID ,f.DESTINATION_AIRPORT_ID ,COUNT(*) as voli
                    FROM flights f 
                    GROUP BY f.ORIGIN_AIRPORT_ID ,f.DESTINATION_AIRPORT_ID                                    
                    """

        cursor.execute(query)

        for row in cursor:
            idP= row["ORIGIN_AIRPORT_ID"]
            idA= row["DESTINATION_AIRPORT_ID"]
            aPartenza= dizionarioAeroporti[idP]
            aArrivo= dizionarioAeroporti[idA]

            voli = row["voli"]
            result.append(Connessione(aPartenza,aArrivo,voli))

        cursor.close()
        conn.close()
        return result


