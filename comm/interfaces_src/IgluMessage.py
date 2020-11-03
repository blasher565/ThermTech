# IgluMessage class used to format messages between processes
# Programmer: Christian Wagner
# Date Created: 1/09/2020
# Date Modified: 11/02/2020
# Version: 2.0

class IgluMessage:
    # constructor for raw data from the server
    def __init__(self, *args):
        self.__format_delimiter = '&' # message data delimiter setting
        if len(args) == 5:
            # new message without raw data
            self.__message = args[0]
            self.__timestamp = args[1]
            self.__priority = args[2]
            self.__target = args[3]
            self.__sender = args[4]
            self.__encoded = False
        elif len(args) == 1:
            # new message with raw data
            pieces = args[0].split(self.__format_delimiter) # parse raw data
            # check length
            if len(pieces) == 6:
                tmp = pieces[0].split("=")
                if 'MESSAGE' in tmp[0] and len(tmp) == 2:
                    self.__message = tmp[1]
                else:
                    self.__message = 'Error building message object'

                tmp = pieces[1].split("=")
                if 'TIMESTAMP' in tmp[0] and len(tmp) == 2:
                    self.__timestamp = tmp[1]
                else:
                    self.__timestamp = '0000-00-00 00:00:00'
            
                tmp = pieces[2].split("=")
                if 'PRIORITY' in tmp[0] and len(tmp) == 2:
                    self.__priority = tmp[1]
                else:
                    self.__priority = 0

                tmp = pieces[3].split("=")
                if 'TARGET' in tmp[0] and len(tmp) == 2:
                    self.__target = tmp[1]
                else:
                    self.__target = 0

                tmp = pieces[4].split("=")
                if 'SENDER' in tmp[0] and len(tmp) == 2:
                    self.__sender = tmp[1]
                else:
                    self.__sender = 0

                tmp = pieces[5].split("=")
                if 'ENCODED' in tmp[0] and len(tmp) == 2:
                    self.__encoded = False if tmp[1] == '0' else True
                else:
                    self.__encoded = False
            else:
                self.__message = 'Error building message object'
                self.__timestamp = '0000-00-00 00:00:00'
                self.__priority = 0
                self.__target = 0
                self.__sender = 0
                self.__encoded = False
        else:
            self.__message = 'Message not set'
            self.__timestamp = '0000-00-00 00:00:00'
            self.__priority = 0
            self.__target = 0
            self.__sender = 0
            self.__encoded = False

    # getter for __message variable
    @property
    def message(self):
        return self.__message

    # getter for __timestamp variable
    @property
    def timestamp(self):
        return self.__timestamp

    # getter for __priority variable
    @property
    def priority(self):
        return self.__priority

    # getter for __target variable
    @property
    def target(self):
        return self.__target

    # getter for __sender variable
    @property
    def sender(self):
        return self.__sender

    # getter for __encoded variable
    @property
    def encoded(self):
        return self.__encoded

    # Returns text form of data stored in IgluMessage object for sending to the server
    def get_tx_data(self):
        tmp = 'MESSAGE=' + self.__message
        tmp += self.__format_delimiter + 'TIMESTAMP=' + self.__timestamp
        tmp += self.__format_delimiter + 'PRIORITY=' + str(self.__priority)
        tmp += self.__format_delimiter + 'TARGET=' + str(self.__target)
        tmp += self.__format_delimiter + 'SENDER=' + str(self.__sender)
        tmp += self.__format_delimiter + 'ENCODED=' + ('1' if self.__encoded else '0')
        return tmp

    # Encrypts the message with a specific encoding and key
    # encoding -> the encoding to use
    # key -> the key to encrypt with
    def encode(self,encoding,key):
        self.__encoded = True

    # Decrypts the message with a specific encoding and key
    # encoding -> the encoding to use
    # key -> the key to encrypt with
    def decode(self,encoding,key):
        self.__encoded = False