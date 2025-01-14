#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing  import List
import mysql.connector


class Persistencia_pelicula_mysql(IPersistencia_pelicula):
    def __init__(self, credencials) -> None:
        self._credencials = credencials
        self._conn = mysql.connector.connect(
                host=credencials["host"],
                user=credencials["user"],
                password=credencials["password"],
                database=credencials["database"]
                )
        if not self.check_table():
            self.create_table()

    def check_table(self):
        try:
            cursor = self._conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM PELICULA;")
            cursor.reset()
        except mysql.connector.errors.ProgrammingError:
            return False
        return True
    
    def count(self) -> int:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
        cursor.execute(query)
        count = cursor.rowcount
        return count
    
    def totes(self) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor.reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    def totes_pag(self, id:int):
        cursor = self._conn.cursor()
        query = f"SELECT * FROM PELICULA WHERE ID >= {id} LIMIT 10"
        cursor.execute(query)
        result = cursor.fetchall()
        pelis_list = []
        for peli in result:
            print(Pelicula(peli[1], peli[2], peli[3], peli[4], self, peli[0]))
            pelis_list.append(Pelicula(peli[1], peli[2], peli[3], peli[4], self, peli[0]))
        return pelis_list
    
    def desa(self, pelicula: Pelicula) -> bool:
        cursor = self._conn.cursor()
        query = f"INSERT INTO PELICULA (TITULO, ANYO, PUNTUACION, VOTOS) VALUES ('{pelicula.titol}', {pelicula.any}, {pelicula.puntuacio}, {pelicula.vots});"
        cursor.execute(query)
        self._conn.commit()
        cursor.close()
        return True
    
    def llegeix(self, any: int) -> List[Pelicula]:
        cursor = self._conn.cursor()
        query = f"SELECT * FROM PELICULA WHERE ANYO LIKE '{any}'"
        cursor.execute(query)
        result = cursor.fetchall()
        pelis_list = []
        if result:
            for peli in result:
                pelis_list.append(Pelicula(id = str(peli[0]), titol = str(peli[1]), any = str(peli[2]), puntuacio = str(peli[3]), vots = str(peli[4]), persistencia = self))
            return pelis_list

    def canvia(self, info:dict, id:int) -> bool:
        cursor = self._conn.cursor()
        if info["opt"] == "titol":
            query = f"UPDATE PELICULA SET TITULO='{info['value']}' WHERE id = {id}"
        elif info["opt"] == "any":
            query = f"UPDATE PELICULA SET ANYO={info['value']} WHERE id = {id}"
        elif info["opt"] == "puntuacio":
            query = f"UPDATE PELICULA SET PUNTUACION={info['value']} WHERE id = {id}"
        elif info["opt"] == "vots":
            query = f"UPDATE PELICULA SET VOTOS={info['value']} WHERE id = {id}"
        cursor.execute(query)
        self._conn.commit()
        return True
