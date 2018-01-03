#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author: Benjamin Rath, Laurene Cladt, Rodolphe Aubry

#On importe les librairies utiles
import os
import sys
import time
import threading
import datetime
import posix_ipc as pos

#Tableau qui contiendra tous les threads
my_threads = []
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

def ecritureFichier(msg):
    #On ouvre le fichier fbatch.txt en écriture append pour ajouter et non pas remplacer (a)
    with open(os.path.expanduser("~/fbatch.txt"),"a") as f:
        print("gobatch: Ecriture de la commande")
        f.write(msg+" \r\n")
    #On crée le thread qui utilisera une fonction auquel on passera les arguments
    dates=msg.split()
    thread = threading.Thread(target = threadedCron, args = (dates[0],dates[1],dates[2],dates[3],dates[4],"wow"))
    #On démarre le thread
    thread.start()
    my_threads.append(thread)

def threadedCron(minute,heure,jourmois,mois,joursemaine,commande):
    #TODO GERER LES JOUR DE LA SEMAINE SI POSSIBLE
    #On démarre le thread
    print("Démarrage du Thread pour la commande : "+commande)
    print("_________________________")
    #On affiche les différents temps pour vérifier
    print("Minute : "+minute)
    print("Heure : "+heure)
    print("Jour du mois : "+jourmois)
    print("Mois : "+mois)
    print("Jour semaine : "+joursemaine)
    now=datetime.datetime.now()
    #On modifie les étoiles en conséquence (A VERIFIER !!)
    if(minute=="*"):
        minute=00
    if(heure=="*"):
        heure=00
    if(jourmois=="*"):
        if(mois!="*"):
            jourmois=01
        else:
            jourmois=now.day
    if(mois=="*"):
        mois=now.month
    #On cree la date avec les différents paramètres
    sched=datetime.datetime(now.year,int(mois),int(jourmois),int(heure),int(minute),00)
    print(now)
    print("timenow")
    print(sched)
    print("timesched")
    #On récupère le total de secondes entre les deux dates
    secsched=(sched-now).total_seconds()
    print(secsched)
    print("_________________________")
    print("Le Thread pour la commande : "+commande+" est termine")

def run():
    while True:
        print("gobatch: En attente d'une commande")
        #Le processus est bloqué tant qu'aucune commande pgcycl n'est arrivée
        S.acquire()
        #lectureFichier()
        try:
            filmess=pos.MessageQueue("/queue",pos.O_CREAT) # ouvre la file
        except pos.ExistentialError:
            pos.unlink_message_queue("/queue") # détruit la file
            filmess = pos.MessageQueue("/queue",pos.O_CREAT) # puis redemande la création
        (message,priorite)=filmess.receive() # retire le message en tête de file
        print("gobatch : Le message reçu est : {}, de priorité {}".format(message,priorite))

        # Type d'action en fonction de la priorité (type) du message
        if priorite == 1:
            # Action : lecture du fichier fbatch
            lectureFichier()
        elif priorite == 2:
            # Action : suppression de la commande spécifiée
            print ""
        elif priorite == 3:
            # Action : écriture dans le fichier fbatch
            ecritureFichier(message)
            # On affiche les threads pour le moment, par la suite il faudra utiliser
            # for t in my_threads:
            # if not t.isAlive()
            # A ce moment là il faudra le relancer sinon rien
            print(my_threads)

if __name__ == "__main__":
    #Initialisation du sémaphore
    try:
        S = pos.Semaphore("/S1",pos.O_CREAT|pos.O_EXCL,initial_value=0)
    except pos.ExistentialError:
        S = pos.Semaphore("/S1",pos.O_CREAT)
    run()
