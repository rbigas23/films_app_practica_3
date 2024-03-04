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
    
def mostra_lent(missatge, v=0.02):
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

def database_read(opt:str, id:int= None, any:int = None):
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencia = get_persistencies(la_meva_configuracio)
    films = Llistapelis(persistencia["pelicula"])
    films.llegeix_de_disc(opt, id, any)
    return films

def database_update(opt:str, peli_dict:dict = None, update_dict:dict = None, id:int = None) -> bool:
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencia = get_persistencies(la_meva_configuracio)
    films = Llistapelis(persistencia["pelicula"])
    if (films.escriu_al_disc(opt, peli_dict, update_dict, id)): return True

def bucle_principal(context):
    opcio = None
    while opcio != '0':
        print("0.- Surt de l'aplicació.\n1.- Mostra pel·lícules\n2.- Insereix un registre\n3.- Modifica un registre")
        opcio = input("Selecciona una opció: ")
        os.system('clear')
        if opcio == '1':
            print("1.- Mostra les primeres 10 pel·lícules\n2.- Mostra pel·lícules per any")
            opcio = input("Selecciona una opció: ")
            os.system('clear')
            if opcio == '1':
                data = None
                sub_opcio = None
                while sub_opcio != '0':
                    opcio = '1'
                    if data:
                        id = data.ult_id
                    else:
                        id = 1
                    data = database_read(opcio, id = id)
                    context["llistapelis"] = data.toJSON()
                    sub_opcio = input("Prem la tecla 'ENTER' per a continuar o introduiex un 0 per acabar: ")
                    os.system('clear')
            elif opcio == '2':
                any = input("Introduiex un any per mostrar les pel·lícules d'aquest: ")
                os.system('clear')
                films = database_read(opcio, any = any)
                print(films)
                context["llistapelis"] = films   
                input("Prem la tecla 'Enter' per a continuar")
                os.system('clear')
        elif opcio == '2':
            print("Insereix les dades de la pel·lícula:")
            peli_dict = {"titol": None, "any":None, "puntuacio":None, "vots":None}
            peli_dict["titol"] = input("Introdueix el títol: ")
            peli_dict["any"] = input("Introdueix l'any: ")
            peli_dict["puntuacio"] = input("Introdueix la puntuacio: ")
            peli_dict["vots"] = input("Introdueix el vots: ")
            if database_update(opt = "create", peli_dict = peli_dict): print("Pel·lícula inserida correctament")
            input("Prem la tecla 'Enter' per a continuar")
            os.system('clear')
        elif opcio == '3':
            id = input("Indica la ID de pel·lícula que vols canviar: ")
            update_opt = input("Indica quin atribut vols modificar (titol, any, puntuació o vots): ")
            update_value = input("Indica el nou valor de l'atribut: ")
            info = {"opt":update_opt, "value": update_value}
            if database_update(opt = "update", update_dict = info, id = id): print("Pel·lícula inserida correctament")
            input("Prem la tecla 'Enter' per a continuar")
            os.system('clear')
        elif opcio != '0':
            print("Opció incorrecta")
    print("Ha sigut un plaer, adéu!")



def main():
    context = {"llistapelis": None}
    landing_text()
    bucle_principal(context)


if __name__ == "__main__":
    main()
