from ipersistencia_pelicula import IPersistencia_pelicula


class Persistencia_pelicula_postgresql(IPersistencia_pelicula):
    
    def __init__(self, credencials) -> None:
        self._credencials = credencials
