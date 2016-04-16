import autopy
import time
import random

random.seed()

def typing(strings):
    for s in strings:
        n = random.random()

        milisecs = '.00'
        n = str(n)
        milisecs = milisecs + n
        milisecs = float(milisecs)

        autopy.key.toggle(s, True)
        time.sleep(milisecs)
        autopy.key.toggle(s, False)





typing("The brown fox jumped over the lazy brown dog.")
typing("My house is located here, but i dont know hwere here is so i dont know how to find the houe to where im going to go")

