# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 21:04:35 2020

@author: Brandon Lasher

   Creates a thead which just continously counts
This will be used as a referance for our test enviroment
to sync the various parts

"""

import threading
import time
import datetime as dt

class iglu_Timer (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self._counter = 0
        self._runCounter = False
        self._countSpeed = 1
        self._observers = []
        self._stopevent  = threading.Event()
        self._time = dt.datetime.now()
       
    def run(self):
        while not( self._stopevent.isSet() ):
            
            #Changes the count amount, if the speed it too quick and 
            #  process can't sleep and wake that quick
            cntSize = 1
            delay = cntSize / self._countSpeed
            
            #.050 sets the minium sleep and update time for the 
            # counter
            while(  delay  < .1 ):
                delay = cntSize / self._countSpeed
                cntSize = cntSize+1
            
            
            #delay = max( .020, 1 / self._countSpeed )
            self._stopevent.wait(delay)
            
            if self._runCounter:
                self._counter = self._counter+cntSize
                for callback in self._observers:
                    callback( self._counter )
                
            #print( "Timer Value is: %d " % self.counter)
    
    def updateSpeed( self, speedVal ):
        self._countSpeed = max(1, speedVal)

    def restartCounter(self):
        self._counter = 0
        self._runCounter = False
        for callback in self._observers:
            callback( self._counter )
    
    def startCounter(self):
        self._runCounter = True
       
    def pauseCounter(self):
        self._runCounter = False
    
    def getCount(self):
        return self._counter
    
    def getCountSpeed(self):
        return self._countSpeed
    
    def isCounting(self):
        return self._runCounter
    
    # Allows functions to be called on 
    #  counter value change
    def bind_to(self,callback):
        self._observers.append(callback)
        
    def join(self, timeout=None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        
    def updateAbsTime( self ):
        hours, mins = divmod(self._counter, 60)
        days, hours = divmod(hours, 24)
        print( days, hours, mins )
        self._time = self._time + dt.timedelta(days=days, hours=hours, minutes=mins)
        return self._time
        
    @property
    def absTime(self):
        return self.updateAbsTime()
    
    @property
    def absTimePretty(self):
        return "{:%b %d, %Y %I:%M %p}".format(self.absTime)
    
    @property
    def relTime(self):
        return self._counter
    
        

global globalTimer
globalTimer = iglu_Timer(1, "Iglu_Timer")
globalTimer.start()



import atexit
@atexit.register
def terminate():
    global globalTimer
    globalTimer.join()
    
    
if __name__ == "__main__":
    print( globalTimer.relTime, globalTimer.absTime )
    time.sleep(2)
    print( globalTimer.relTime, globalTimer.absTime )
    globalTimer.updateSpeed(20)
    globalTimer.startCounter()
    time.sleep(2)
    print( globalTimer.relTime, globalTimer.absTime, globalTimer.absTimePretty  )
    terminate()
    