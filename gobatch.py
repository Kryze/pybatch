#!/usr/bin/python

#-*- coding: utf8 -*-
import os
import sys
import time
import posix_ipc as pos

def fonction():
    with open("/home/benjamin/fbatch.txt","a") as f:
        print("gobatch: Ecriture du temps...")
        f.write("Temps actuelle : " + time.ctime()+"\r")


def run():
    print("gobatch: En attente d'une commande")
    while True:
        S.acquire()
        fonction()

if __name__ == "__main__":
    try:
        S = pos.Semaphore("/S1",pos.O_CREAT|pos.O_EXCL,initial_value=0)
    except pos.ExistentialError:
        S = pos.Semaphore("/S1",pos.O_CREAT)
    run()
