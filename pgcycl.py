#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author: Benjamin Rath, Laurene Cladt, Rodolphe Aubry

# On importe les librairies utiles
import os
import sys
import time
import posix_ipc as pos
import re

def run():
    # pgcycl envoie un message à gobatch. La priorité change en fonction du paramètre.
    # La fonction est appelée de la sorte : ./pgcycl [0-59] [0-23] [1-31] [1-12] [0-6] cmd stdout stderr

    # Création de la file de messages
    try:
        filmess = pos.MessageQueue("/queue",pos.O_CREAT)
        print "pgcycl : creation de la file de message"
    except pos.ExistentialError:
        pos.unlink_message_queue("/queue") # détruit la file
        filmess = pos.MessageQueue("/queue",pos.O_CREAT) # puis redemande la création

    # On récupère les arguments
    args=sys.argv

    # On vérifie le paramètre
    if len(args)>1 and re.match("^-[lda]$",args[1]):
        param=args[1][1]

        # Actions à effectuer en fonction du paramètre
        if param=="l":
            # Affichage du fichier fbatch
            message="fbatch list"
            filmess.send(message,None,1)
            print "pgcycl : message {} envoyé".format(message)
        elif param=="d":
            # Suppression d'une ligne, on verifie qu'il y a bien 3 arguments et que c'est un nombre
            if(len(args)==3 and args[-1].isdigit()):
                message=args[-1]
                filmess.send(message,None,2)
                print "pgcycl : message {} envoyé".format(message)
            else:
                print "_________________________"
                print "Erreur, veuillez indiquer la ligne que vous souhaitez supprimer"
                print "Le format est : -d x"
                print "Ou x est la ligne à supprimer"
                print "_________________________"
        elif param=="a":
            # Ajout d'une ligne au fichier fbatch
            # On récupère les arguments correspondant au temps
            cron=[]
            try:
                # Boucle sur les arguments cron
                for arg in args[2:-3]:
                    if re.match("^[0-9]{1,2}$",arg):
                        cron.append(arg)
                    elif re.match("^\*$",arg):
                        cron.append("*")
                    else:
                        print "Paramètre {} invalide.".format(arg)
                # Formattage de cron :
                if len(cron)<5:
                    for i in range(5-len(cron)):
                        cron.append('*')
                elif len(cron)>5:
                    cron=cron[:5]

                # On récupère le nom de la commande ainsi que les fichiers de sortie
                cmd=args[-3]
                # On récupère le nom des fichiers de sortie standard et erreur
                stdout=args[-2]
                stderr=args[-1]
                # Cela nous permet également de vérifier que le nombre de paramètres est correct
                
                if re.match("^[0-9\*]{1,2}$",cmd) or re.match("^[0-9\*]{1,2}$",stdout) or re.match("^[0-9]{1,2}$",stderr):
                    # On vérifie que l'utilisateur a bien entré les paramètres correspondants, en utilisant une regex
                    print "Paramètre(s) invalide(s). Veuillez renseigner une commande, une sortie standard et une sortie d'erreurs."
                else:
                    # On envoie le message à gobatch : ce qu'il devra écrire dans fbatch
                    # Le message correspond à cron + commande + fichiers de sortie
                    message=' '.join(cron+args[-3:])
                    filmess.send(message,None,3)
                    print "pgcycl : message {} envoyé".format(message)
            except IndexError:
                print "Nombre de paramètres invalides."
    else:
        print "Paramètre invalide. Utilisez -l, -d ou -a"


if __name__ == "__main__":
    # Initialisation du sémaphore
    try:
        S = pos.Semaphore("/S1",pos.O_CREAT|pos.O_EXCL,initial_value=0)
    except pos.ExistentialError:
        S = pos.Semaphore("/S1",pos.O_CREAT)
    run()
    # On relache le sémaphore après avoir envoyé un message à gobatch
    S.release()
    print "pgcycl: Relachement du semaphore"
