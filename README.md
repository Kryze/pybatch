<p align="center"><img width="150"src="https://user-images.githubusercontent.com/18222418/34547852-62892c5a-f0fe-11e7-8f31-ce815664d201.png"></a></p>

<h1 align="center"> Pybatch </h1>

<p align="center">A Python cron-like tool to schedule execution of commands.</p>



## What is Pybatch ? 

----------

Pybatch is a program who let you schedule execution of a command when you want.

It's a school project for a M1 MIAGE course.

## Installation  

----------

This project only works for UNIX systems because of the use of semaphore and for the meaning of the course.

First, you need to install `posix_ipc` by running :

`pip install posix_ipc`

Download both python script (gobatch.py & pybatch.py) and put them in a directory of your choice.

You need to run gobatch.py by running `./gobatch` which is the server of your commands.

You will then enter commands with `pybatch.py`

## How works Pybatch ? 

----------

Each time you want to enter a command, a file named `fbatch.txt`

There is 3 parameters available :

`./pgcycl -a minute hour monthday month weekday command output error`

You can choose the interval of execution of your commands by choosing which parameters you want to fill.
Here is the interval of each value :

- minute 0-59   
- hour 0-23
- monthday 1-31
- month 1-12
- weekday 0-6 
- output (The file of the standard output)
- error (The file of the error output)

You can also put `"*"` to replace an empty time/date field or just let the rest of the time/date field empty.

You must choose a command and an output/error parameter.

A command can take space by putting `"''"` between the parameter.

`./pgcycl -l`

This command let you list the differents commands you are running in a cycle.

`./pgcycl -d x`

This command let you delete an execution of command by choosing the line of the command you want to delete.

You can view each line with `./pgcycl -l`

# Contributors 

----------

## Laurene Cladt

<p><a href="https://github.com/claurene" target="_blank"><img width="80"src="https://avatars2.githubusercontent.com/u/22750010?s=460&v=4"></a></p>

## Rodolphe Aubry

<p><a href="https://github.com/rodobry" target="_blank"><img width="80"src="https://avatars1.githubusercontent.com/u/22979894?s=460&v=4"></a></p>

## Benjamin "Kryze"

<p><a href="https://github.com/Kryze" target="_blank"><img width="80"src="https://avatars3.githubusercontent.com/u/18222418?s=460&v=4"></a></p>

