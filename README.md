# pybatch

## Gestion de Processus en Batch (Python)

La gestion de processus en batch permet à tout utilisateur de lancer de façon cyclique à une date ou une heure précise un programme. 

**Par exemple, lancement automatique du programme PAIE tous les 26 de chaque mois à 23h30, ou lancement automatique d'un programme de sauvegarde du contenu d’un disque tous les lundis à 3h du matin.** 
 
La mise en œuvre d'un tel système nécessite l'écriture d'un programme démon gobatch qui explore un fichier fbatch dans lequel sont définis les programmes ou commandes à exécuter cycliquement. 
 
L'utilisateur qui veut lancer un programme cyclique ou le supprimer doit lancer la commande pgcycl en précisant au besoin des paramètres comme : 
 
- minute 0-59   
- heure 0-23
- jour du mois 1-31
- mois 1-12
- jour de la semaine 0-6   

commande à exécuter en précisant le nom du fichier de sortie et le nom du fichier des erreurs 
 
pgcycl modifie en conséquence le fichier fbatch. 
 
La sortie standard (stdout) et la sortie des erreurs (stderr) des commandes soumises à gobatch sont redirigées vers les fichiers précisés dans le champ 6. 
 
Le démon gobatch, lancé en arrière-plan, est averti à chaque modification du fichier par pgcycl. Par souci de simplification, gobatch ne travaille que pour le compte d'un utilisateur et est lancé une fois pour toutes. 
 
syntaxe de pgcycl : 
 
pgcycl 
- <-l> fbatch pour lister le contenu de fbatch 
- <-d> fbatch pour détruire une ligne de  fbatch 
- <-a> fbatch pour ajouter une ligne à  fbatch 
 
Prévoyez une démonstration "parlante".
