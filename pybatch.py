#!/usr/bin/python

#-*- coding: utf8 -*-
import os
import sys
import time
import posix_ipc as pos

try:
    S = pos.Semaphore("/S1",pos.O_CREAT|pos.O_EXCL,initial_value=0)
except pos.ExistentialError:
    S = pos.Semaphore("/S1",pos.O_CREAT)

S.release()
print("pgcycl: Relachement du semaphore")
