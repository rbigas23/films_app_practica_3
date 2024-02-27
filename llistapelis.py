#!/bin/usr/python3

import json
from typing import List
from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula

class Llistapelis():
    def __init__ (self, persistencia_pelicula: IPersistencia_pelicula) -> None:
        self._pelicules= []
        self._ult_id = 0
        self._persistencia_pelicula:IPersistencia_pelicula = persistencia_pelicula
        
    @property
    def pelicules(self) -> List[Pelicula]:
        return self._pelicules
    
    @property
    def ult_id(self) -> int:
        return self._ult_id

    @property
    def persistencia_pelicula(self) -> IPersistencia_pelicula:
        return self._persistencia_pelicula
    
    def __repr__(self):
        return self.toJSON()
    
    def toJSON(self):
        pelicules_list = []
        for pelicula in self._pelicules:
            pelicules_list.append(json.loads(pelicula.toJSON()))
        self_dict = {"pelicules": pelicules_list}   
        return json.dumps(self_dict)

    def llegeix_de_disc(self, opt:str, id:int = None, any:int = None):
        if opt == '1':
            self._pelicules = self._persistencia_pelicula.totes_pag(id)
            self._ult_id = id + 10
        elif opt == '2':
            self._pelicules = self._persistencia_pelicula.llegeix(any)

    def escriu_al_disc(self, opt:str, peli_dict:dict = None, update_dict:dict = None, id:int = None):
        if opt == "create":
            peli = Pelicula(**peli_dict, persistencia = self._persistencia_pelicula)
            if self._persistencia_pelicula.desa(peli): return True
        elif opt == "update":
            if self._persistencia_pelicula.canvia(update_dict, id): return True
