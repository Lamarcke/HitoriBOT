#!/usr/bin/python
from subprocess import Popen
import sys

filename = 'bot.py'
while True:
    print("\nStarting " + filename)
    p = Popen("python3.8 " + filename, shell=True)
    p.wait()
