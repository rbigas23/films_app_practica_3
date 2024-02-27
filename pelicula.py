#!/bin/usr/python3

import json

class Pelicula:
    def __init__(self, titol: str, any: int, puntuacio: float , vots: int, persistencia, id = None) -> None:
        self._titol = titol
        self._any = any
        self._puntuacio = puntuacio
        self._vots = vots
        self._persistencia = persistencia
        self._id = id

    @property
    def titol(self) -> str:
        return self._titol
    
    @titol.setter
    def titol(self, valor:str) -> None:
        self._titol = valor

    @property
    def any(self) -> int:
        return self._any
    
    @any.setter
    def any(self, valor:int) -> None:
        self._any = valor

    @property
    def puntuacio(self) -> float:
        return self._puntuacio
    
    @puntuacio.setter
    def puntuacio(self, valor:float) -> None:
        self._puntuacio = valor

    @property
    def vots(self) -> int:
        return self._vots
    
    @vots.setter
    def vots(self, valor:int) -> None:
        self._vots = valor

    @property
    def id(self):
        return self._id
    
    @property
    def persistencia(self):
        return self._persistencia

    def toJSON(self):
        return json.dumps({"id": self.id, "titol": self.titol, "any": self.any, "puntuacio": self.puntuacio, "vots": self.vots})
    
    def __repr__(self):
        return self.toJSON()