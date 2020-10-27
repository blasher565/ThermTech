#!/usr/bin/env python3

"""
Author: Brandon Lasher
Last Update: 10/25/2020

This is a simple message class will encode / decode 
  messages sent for the Iglu system

History:
    10/25/2020 - Orignal 

"""

import json
from datetime import datetime

class message:
    
    def __init__( self, src="NULL", dst="NULL", msg=dict() ):
        self.src = src
        self.dst = dst
        self.timestamp = datetime.now().isoformat()

        #store what is to be transmitted
        self.message = dict() 
        self.message["src"] = self.src
        self.message["dst"] = self.dst
        self.message["msg"] = json.dumps(msg)


    #Updates the informaiton for Source
    def setSrc( self, src ):
        self.src = src
        self.message["src"] = self.src


    #Updates the information for the destination
    def setDst( self, dst ):
        self.dst = dst
        self.message["dst"] = self.dst

    #Assumes all fields are defined
    def encodeMsg( self ):
        self.timestamp = datetime.now().isoformat()
        self.message["timestamp"] = self.timestamp
        return json.dumps( self.message, indent=4 )


    #Decodes the message and returns the dict
    def decodeMsg( self, rcv_msg ):
        self.message = json.loads( rcv_msg )
        self.src =  self.message["src"]
        self.dst = self.message["dst"] 
        self.timestamp = self.message["timestamp"];
        return self.message["msg"]










#
if __name__ == "__main__":
   
    info = dict()
    info["Command"] = "UPDATE";
    info["Current Temp"] = 98;
    info["Target Temp"] = 60;
    info["Humidity"] = .40;

    sent_msg = message("127.0.0.1:5800", "127.0.0.1:5801", msg = info )
    rcv_msg = message()

    data_sent = sent_msg.encodeMsg();
    data_rcv = rcv_msg.decodeMsg(data_sent);

    print("\nOrignal data struct")
    print( info )

    print("\nJson formatted")
    print( data_sent )

    print("\nDecoded Message")
    print( data_rcv )

