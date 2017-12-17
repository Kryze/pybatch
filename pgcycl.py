#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author: Benjamin Rath, Laurene Cladt, Rodolphe Aubry

#On importe les librairies utiles
import os
import sys
import time
import posix_ipc as pos


def pgcyclwrite():
    #On ouvre le fichier fbatch.txt en écriture append pour ajouter et non pas remplacer (a)
    with open(os.path.expanduser("~/fbatch.txt"),"a") as f:
        print("pgcycl: Ecriture de la commande")
        #sys.argv contient tous les arguments dans un tableau, ici on veut une ligne avec la commande
        for arg in sys.argv:
            f.write(arg+" ")
        f.write("\r\n")

if __name__ == "__main__":
    #Initialisation du sémaphore
    try:
        S = pos.Semaphore("/S1",pos.O_CREAT|pos.O_EXCL,initial_value=0)
    except pos.ExistentialError:
        S = pos.Semaphore("/S1",pos.O_CREAT)
    print(str(sys.argv))
    pgcyclwrite()
    #On relache le sémaphore après avoir écrit une nouvelle ligne de commande dans le fichier
    S.release()
    print("pgcycl: Relachement du semaphore")
