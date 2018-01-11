#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author: Benjamin Rath, Laurene Cladt, Rodolphe Aubry

# On importe les librairies utiles
import os
import sys
import time
from multiprocessing import Process
from datetime import datetime,timedelta
import posix_ipc as pos
import shlex

# Tableau qui contiendra tous les threads
my_threads = []

# Tableaux permettant de passer d'un nombre au string correspondant à son jour de semaine ou au mois
jourT = ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
moisT = ['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']

# Fonction permettant de lire le fichier fbatch
def lectureFichier():
    #On initialise le nombre de lignes à 0
    i=0
    # On ouvre le fichier fbatch.txt en lecture (r)
    try:
        with open(os.path.expanduser("~/fbatch.txt"),"r") as f:
            # On retire les \r\n du fichier pour éviter leurs affichage lors de la lecture
            f=f.read().splitlines()
            # Pour chaque ligne du fichier
            for line in f:
                # On incrémente la variable pour chaque ligne
                i+=1
                #TODO: afficher le PID et vérifier qu'il tourne encore, sinon le relancer pour chaque ligne
                # On split la ligne en prenant en compte les quotes
                tabCmd = shlex.split(line)
                # Si jour de la semaine ou mois sont vides on ne regarde pas les tableaux
                if tabCmd[4] == '*':
                    joursemaineTxt = '*'
                else:
                    joursemaineTxt = jourT[int(tabCmd[4])]
                if tabCmd[3] == '*':
                    moisTxt = '*'
                else:
                    moisTxt = moisT[int(tabCmd[3])-1]

                # On affiche la ligne ainsi que les informations de fbatch de façon lisible pour l'utilisateur
                print "Ligne {} - Execution du programme {} chaque {} {} {} à {} H {}".format(i,tabCmd[5],joursemaineTxt,tabCmd[2],moisTxt,tabCmd[1],tabCmd[0])
    except IOError:
        print "Le fichier fbatch est vide ou n'existe pas."

# Fonction permettant d'écrire dans le fichier fbatch et de lancer le thread correspondant
def creationThread():
    # On ouvre le fichier fbatch et récupère la dernière ligne
    try:
        with open(os.path.expanduser("~/fbatch.txt"),"r") as f:
            # On récupère toutes les lignes du fichier
            f=f.read().splitlines()            

        # On s'interesse uniquement à la dernière ligne du fichier
        msg = f[-1]

        # On créé le thread qui utilisera une fonction à laquelle on passera les arguments
        thread = Process(target = threadedCron, args = shlex.split(msg))

        # On démarre le thread en tant que démon et l'ajoute au tableau
        thread.daemon = True
        thread.start()
        my_threads.append(thread)
    except IOError:
        print "Le fichier fbatch est vide ou n'existe pas."

#TODO:
def threadedCron(minute,heure,jourmois,mois,joursemaine,commande,stdout,stderr):
    # On démarre le thread
    print("Démarrage du Thread pour la commande : "+commande)
    print("_________________________")

    # On affiche les différents temps pour vérifier
    print("Minute : "+minute)
    print("Heure : "+heure)
    print("Jour du mois : "+jourmois)
    print("Mois : "+mois)
    print("Jour semaine : "+joursemaine)
    while(True):
        print("------------------")
        now=datetime.now()

        # On récupère la prochaine date d'éxécution avec la fonction correspondante
        sched=next_date(mois,jourmois,joursemaine,heure,minute)
        print("timenow : {}".format(now))
        print("timesched : {}".format(sched))

        # On récupère le total de secondes entre les deux dates
        secsched=(sched-now).total_seconds()
        print("nbr de secondes : {}".format(secsched))
        print("------------------")
        #On endort le thread le temps défini avant la prochaine execution de la commande
        time.sleep(secsched)
        #On execute la commande indiquer par l'utilisateur
        execFonction(commande,stdout,stderr)
    print("_________________________")
    print("Le Thread pour la commande : "+commande+" est termine")
    #TODO: lancer la commande dans secsched secondes

def execFonction(commande,stdout,stderr):
    # Exécute la commande précisée
    print("I am running again for "+commande)
    msg="{} 1>>{} 2>>{}".format(commande,stdout,stderr)
    os.system(msg)

# Fonction qui définie la prochaine date d'éxecution
def next_date(mois,jourmois,joursemaine,heure,minute):
  next=datetime.now() # on récupère la date d'aujourd'hui
  next+=timedelta(minutes=1) # on ajoute une minute pour éviter les problèmes
  next=next.replace(second=0) # on initialise les secondes à 0
  cont=True

  while(cont):
    # Mois
    if mois.isdigit() and int(mois)!=next.month:
        if next.month>int(mois):
            next=next.replace(year=next.year+1) # si on a dépassé le mois, on ajoute une année
        next=next.replace(month=int(mois),day=1,hour=0,minute=0) # on se place au début du mois
        continue

    # Jour du mois
    if jourmois.isdigit() and int(jourmois)!=next.day:
      if next.day > int(jourmois): # voir pour le nbr de jours par mois
       next=next.replace(month=next.month+1,day=1) # si on a dépassé le jour, on se place au mois suivant
      else:
        try:
         next=next.replace(day=int(jourmois))
        except ValueError:
          next=next.replace(month=next.month+1,day=1) # si le mois actuel ne contient pas le bon nombre de jours (exemple on veut le jour 31 et on est en Février, on se place au mois suivant)
      next=next.replace(hour=0,minute=0) # on se place au début du jour
      continue

    # Jour de la semaine
    if joursemaine.isdigit() and int(joursemaine)!=next.weekday():
      diff=int(joursemaine)-next.weekday() # on calcule la différence entre les jours de la semaine
      if diff < 0:
        diff+=7 # si on a dépassé le jour, on se place à la semaine suivante
      next+=timedelta(days=diff)
      next=next.replace(hour=0,minute=0) # on se place au début du jour
      continue

    # Heure
    if heure.isdigit() and int(heure)!=next.hour:
      if next.hour > int(heure):
        next+=timedelta(days=1) # si on a dépassé l'heure, on se place au jour suivant
      next=next.replace(hour=int(heure),minute=0) # on se place au début de l'heure
      continue

    # Minute
    if minute.isdigit() and int(minute)!=next.minute:
      if next.minute > int(minute):
        next+=timedelta(hours=1) # si on a dépassé la minute, on se place à l'heure suivante
      next=next.replace(minute=int(minute))

    cont=False # lorsque la date correspond, on sort de la boucle

  return(next) # retourne la prochaine date d'éxecution

def supprimerThread(message):
    # Supprime le thread correspondant à la ligne supprimée
    print(my_threads)
    my_threads[int(message)-1].terminate()
    my_threads[int(message)-1].join()
    #On supprime la référence du thread de la liste
    del my_threads[int(message)-1]
    print(my_threads)

def run():
    while True:
        print "gobatch: En attente d'une commande"
        # Le processus est bloqué tant qu'aucune commande pgcycl n'est arrivée
        S.acquire()
        # gobatch attend de reçevoir un message de pgcycl :
        try:
            filmess=pos.MessageQueue("/queue",pos.O_CREAT) # ouvre la file
        except pos.ExistentialError:
            pos.unlink_message_queue("/queue") # détruit la file
            filmess = pos.MessageQueue("/queue",pos.O_CREAT) # puis redemande la création
        (message,priorite)=filmess.receive() # retire le message en tête de file
        print "gobatch : Le message reçu est : {}, de priorité {}".format(message,priorite)

        # Type d'action en fonction de la priorité (type) du message
        if priorite == 1:
            # Action : lecture du fichier fbatch
            lectureFichier()
        elif priorite == 2:
            # Action : suppression de la commande spécifiée
            supprimerThread(message)
        elif priorite == 3:
            # Action : écriture dans le fichier fbatch
            creationThread()
            #TODO: On affiche les threads pour le moment, par la suite il faudra utiliser
            # for t in my_threads:
            # if not t.isAlive()
            # A ce moment là il faudra le relancer sinon rien

if __name__ == "__main__":
    #Initialisation du sémaphore
    try:
        S = pos.Semaphore("/S1",pos.O_CREAT|pos.O_EXCL,initial_value=0)
    except pos.ExistentialError:
        S = pos.Semaphore("/S1",pos.O_CREAT)
    run()
