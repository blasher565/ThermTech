#!/usr/bin/env python3

"""
Author: Brandon Lasher
Secondary: Christian Wagner (Last Update: 11/02/2020)
Last Update: 10/25/2020

This is a simple message class will encode / decode 
  messages sent for the Iglu system

History:
    10/25/2020 - Orignal
    11/02/2020 - @property added

"""

import json
from datetime import datetime

class message:
    
    def __init__( self, src="NULL", dst="NULL", msg=dict() ):
        self.__src = src
        self.__dst = dst
        self.__timestamp = datetime.now().isoformat()

        # store what is to be transmitted
        self.__message = dict() 
        self.__message["src"] = self.__src
        self.__message["dst"] = self.__dst
        self.__message["msg"] = json.dumps(msg)

    @property
    def src(self):
        return self.__src

    # Updates the informaiton for Source
    @src.setter
    def src(self, src):
        self.__src = src
        self.__message["src"] = self.__src

    @property
    def dst(self):
        return self.__dst

    #Updates the information for the destination
    @dst.setter
    def dst(self, src):
        self.__dst = dst
        self.__message["dst"] = self.__dst

    #Assumes all fields are defined
    def encodeMsg( self ):
        self.__timestamp = datetime.now().isoformat()
        self.__message["timestamp"] = self.__timestamp
        return json.dumps( self.__message, indent=4 )

    #Decodes the message and returns the dict
    def decodeMsg( self, rcv_msg ):
        self.__message = json.loads( rcv_msg )
        self.__src =  self.__message["src"]
        self.__dst = self.__message["dst"] 
        self.__timestamp = self.__message["timestamp"];
        return self.__message["msg"]


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

