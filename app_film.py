#!/usr/bin/python3

import os, yaml, sys, time, json
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql
from llistapelis import Llistapelis
import logging

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
RUTA_FITXER_CONFIGURACIO = os.path.join(THIS_PATH, 'configuracio.yml') 
print(RUTA_FITXER_CONFIGURACIO)

def get_configuracio(ruta_fitxer_configuracio) -> dict:
    config = {}
    with open(ruta_fitxer_configuracio, 'r') as conf:
        config = yaml.safe_load(conf)
    return config

def get_persistencies(conf: dict) -> dict:
    credencials = {}
    if conf["base de dades"]["motor"].lower().strip() == "mysql":
        credencials['host'] = conf["base de dades"]["host"]
        credencials['user'] = conf["base de dades"]["user"]
        credencials['password'] = conf["base de dades"]["password"]
        credencials['database'] = conf["base de dades"]["database"]
        return {
            'pelicula': Persistencia_pelicula_mysql(credencials)
        }
    else:
        return {
            'pelicula': None
        }
    
def mostra_lent(missatge, v=0.05):
    for c in missatge:
        print(c, end='')
        sys.stdout.flush()
        time.sleep(v)
    print()

def landing_text():
    os.system('clear')
    print("Benvingut a la app de pel·lícules")
    time.sleep(1)
    msg = "Desitjo que et sigui d'utilitat!"
    mostra_lent(msg)
    input("Prem la tecla 'Enter' per a continuar")
    os.system('clear')

def mostra_llista(llistapelicula):
    os.system('clear')
    mostra_lent(json.dumps(json.loads(llistapelicula.toJSON()), indent=4), v=0.01)

def mostra_seguents(llistapelicula):
    os.system('clear')

def mostra_menu_next10():
    print("0.- Surt de l'aplicació.\n2.- Mostra les següents 10 pel·lícules")

def database_read(opt:int, id:int = None, any:int = None):
    logging.basicConfig(filename = 'pelicules.log', encoding = 'utf-8', level = logging.DEBUG)
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencia = get_persistencies(la_meva_configuracio)
    films = Llistapelis(persistencia["pelicula"])
    films.llegeix_de_disc(opt, id, any)
    return films

def bucle_principal(context):
    opcio = None
    while opcio != '0':
        print("0.- Surt de l'aplicació.\n1.- Mostra pel·lícules")
        opcio = input("Selecciona una opció: ")
        opcio = opcio
        if opcio == '1':
            print("1.- Mostra les primeres 10 pel·lícules\n2.- Mostra pel·lícules per any")
            opcio = input("Selecciona una opció: ")
            opcio = opcio
            if opcio == '1':
                id = input("Introduiex la id per la que vols començar: ")
                films = database_read(opcio, id = id)
            elif opcio == '2':
                any = input("Introduiex un any per mostrar les pel·lícules d'aquest: ")
                films = database_read(opcio, any = any)
                context["llistapelis"] = films
                print(films)
        elif opcio == '2':
            pass
        else:
            print("Opció incorrecta")



def main():
    context = {"llistapelis": None}
    landing_text()
    bucle_principal(context)


if __name__ == "__main__":
    main()
