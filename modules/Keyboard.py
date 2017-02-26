#Keyboard.py
import autopy
import time
import random

### My Modules
import RandTime

def type_this(strings):
	"""Types the passed characters with random pauses in between strokes"""
	for s in strings:

		# delay between key presses--key UP/DOWN
		autopy.key.toggle(s, True)
		
		if random.randint(0,5) == 0:
			RandTime.randTime(0,0,0,0,2,9)
		else:
			RandTime.randTime(0,0,0,0,1,9)
			
		autopy.key.toggle(s, False)
		# delay after key UP--next key 
		RandTime.randTime(0,0,0,0,0,9) 

def press(button):
    if button == 'enter':
        autopy.key.toggle(autopy.key.K_RETURN, True)
        RandTime.randTime(0,0,1,0,0,1)
        autopy.key.toggle(autopy.key.K_RETURN, False)

    else:
        autopy.key.toggle(autopy.key.button, True)

