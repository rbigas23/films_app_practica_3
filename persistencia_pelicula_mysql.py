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
    
    def totes_pag(self, id:int) -> List[Pelicula]:
        cursor = self._conn.cursor()
        query = f"SELECT * FROM PELICULA WHERE ID > {id} LIMIT 10"
        cursor.execute(query)
        result = cursor.fetchall()
        pelis_list = List[Pelicula]
        for peli in result:
            pelis_list.append(Pelicula(peli[1], peli[2], peli[3], peli[4]))
        return pelis_list
    
    def desa(self, pelicula: Pelicula) -> Pelicula:
        cursor = self._conn.cursor()
        query = f"INSERT INTO PELICULA (TITULO, ANYO, PUNTUACION, VOTOS) VALUES ({pelicula.titol}, {pelicula.any}, {pelicula.puntuacio}, {pelicula.vots});"
        cursor.execute(query)
        self._conn.commit()
        cursor.close()
        return pelicula
    
    def llegeix(self, any: int) -> List[Pelicula]:
        cursor = self._conn.cursor()
        query = f"SELECT * FROM PELICULA WHERE ANYO LIKE '{any}'"
        cursor.execute(query)
        result = cursor.fetchall()
        pelis_list = []
        if result:
            for peli in result:
                pelis_list.append(Pelicula(titol = str(peli[1]), any = str(peli[2]), puntuacio = str(peli[3]), vots = str(peli[4]), persistencia = self))
            return pelis_list
        else:
            print("No existeixen pel·ícules d'aquest any a la base de dades.")

    def canvia(self, info:dict, pelicula:Pelicula) -> Pelicula:
        cursor = self._conn.cursor()
        if info["opt"] == "titol":
            query = f"UPDATE PELICULA SET TITULO={info['value']} WHERE id = {pelicula.id}"
        elif info["opt"] == "any":
            query = f"UPDATE PELICULA SET ANYO={info['value']} WHERE id = {pelicula.id}"
        elif info["opt"] == "punt":
            query = f"UPDATE PELICULA SET PUNTUACION={info['value']} WHERE id = {pelicula.id}"
        elif info["opt"] == "vots":
            query = f"UPDATE PELICULA SET VOTOS={info['value']} WHERE id = {pelicula.id}"
        cursor.execute(query)
        self._conn.commit()
        return pelicula
