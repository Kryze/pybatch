#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author: Benjamin Rath, Laurene Cladt, Rodolphe Aubry

#On importe les librairies utiles
import os
import sys
import time
import posix_ipc as pos

#TODO Mettre le repertoire avec le truc comme HOME a la place de benjamin
def lectureFichier():
        #On ouvre le fichier fbatch.txt en lecture (r)
        with open(os.path.expanduser("~/fbatch.txt"),"r") as f:
            #On retire les \r\n du fichier pour éviter leurs affichage lors de la lecture
            f=f.read().splitlines()
            #Pour chaque ligne
            for line in f:
                #On affiche la ligne
                # A faire Plus tard, afficher le PID et vérifier qu'il tourne encore, sinon le relancer pour chaque ligne
                print(line)


def run():
    while True:
        print("gobatch: En attente d'une commande")
        #Le processus est bloqué tant qu'aucune commande pgcycl n'est arrivée
        S.acquire()
        lectureFichier()

if __name__ == "__main__":
    #Initialisation du sémaphore
    try:
        S = pos.Semaphore("/S1",pos.O_CREAT|pos.O_EXCL,initial_value=0)
    except pos.ExistentialError:
        S = pos.Semaphore("/S1",pos.O_CREAT)
    run()
