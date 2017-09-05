from modules import RS
from modules import RandTime

class Idle():

    def __init__(self, time=0):
        self.time = time
        self.idleing()

    def idleing(self):
        while 1:
            RS.antiban('magic')
            for _ in xrange(50):
                RandTime.randTime(1,0,0,9,9,9)

idle = Idle()
    


