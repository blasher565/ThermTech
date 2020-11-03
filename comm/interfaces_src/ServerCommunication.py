import socket
import queue
import time
import IgluMessage

# ServerCommunication class used to access interprocess communication server
# Programmer: Christian Wagner
# Date Created: 3/11/2020
# Date Modified: 11/02/2020
# Version: 2.0

class ServerCommunication:
    # Overloaded constructor
    # host -> the name of the host
    # port -> the port number being served on
    # pid -> the process identification number
    def __init__(self,host='localhost',port=8189,pid=0):
        self.__DEBUG_FLAG = True # debug messages flag
        self.__RETRY_CONNECTION_COUNT = 4 # number of times to retry before giving up
        self.__RETRY_CONNECTION_WAIT = 1 # time to wait, in seconds, between retries
        super().__init__() # call to super constructor
        self.__host = host # name of host
        self.__port = port # port number
        self.__pid = pid # process identifcation number
        self.__coordination_port = 18000 # port for communication coordination
        self.__s = 0 # setup socket variable
        self.__connected = False # default connection status

    # getter for process identification number variable
    @property
    def PID(self):
        return self.__pid

    # Connect to server using given host and port parameters
    def connect(self):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialize socket object
        self.__s.connect((self.__host, self.__coordination_port)) # establish coordination socket connection
        
        try:
            tmp = 'test\n'
            self.__s.sendall(tmp.encode('utf-8')) # try sending on connection
            self.__connected = True
        except Exception as e:
            # connection failed, try again
            self.__connected = False

        if(not self.__connected):
            if(self.__DEBUG_FLAG): print('Connection on coordination port failed!')

            self.__s = 0 # clear variable

            # try to make connection again
            for x in range(0, self.__RETRY_CONNECTION_COUNT):
                if(self.__DEBUG_FLAG): print('Retrying connection on coordination port')

                self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialize socket object
                self.__s.connect((self.__host, self.__coordination_port)) # establish coordination socket connection

                time.sleep(self.__RETRY_CONNECTION_WAIT) # wait

                try:
                    tmp = 'test\n'
                    self.___s.sendall(tmp.encode('utf-8')) # try sending on connection
                    self.__connected = True # connecion was made
                except:
                    self.__connected = False # connection failed
                
                if self.__connected:
                    break

                # clear and restart
                self.__s = 0
            
            if not self.__connected:
                return False
                
        if(self.__DEBUG_FLAG): print('Connected to coordination port!')

        tmp = str(self.__port) + '\n'
        self.__s.sendall(tmp.encode('utf-8')) # communicate desired port
        check = self.__s.recv(1024) # get server status
        if check == b'a\n':
            self.disconnect()
            self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialize socket object
            self.__s.connect((self.__host, self.__port)) # establish socket connection
            ID = 'PID=' + str(self.__pid) + '\n' # create PID query
            self.__s.sendall(ID.encode('utf-8')) # send PID information
            return True
        else:
            if self.__DEBUG_FLAG: print('Coordination failed.')
            if self.__DEBUG_FLAG: print('Selected port is being used.')
            
            self.disconnect()
            return False

    # Disconnect from the server
    def disconnect(self):
        try:
            self.__s.sendall(b"exit\n") # signal exit
            self.__s.close() # close socket connection
            self.__s = 0 # clear variable
            return True
        except:
            return False

    # Open connection to the server
    def open(self):
        if self.__s != 0:
            try:
                self.__s.sendall(b"test\n") # signal exit
                return True # socket is already open
            except:
                return self.connect()
        else:
            return self.connect()

    # Close connection to the server
    def close(self):
        if self.__s == 0:
            return True # socket is already closed
        else:
            return self.disconnect()

    # Send data to the server for the queue
    # msg -> the data to send
    def WriteQueue(self, msg='NULL'):
        try:
            self.__s.sendall(b'QW\n')
            tmp = msg.get_tx_data() + '\n'
            self.__s.sendall(tmp.encode('utf-8')) # send data from IgluMessage object
            return True
        except:
            return False # socket is not connected

    # Check for items in the queue
    # return -> returns true if items are in the queue, false otherwise
    def CheckQueue(self):
        # method to check queue status
        self.__s.sendall(b'QC\n')
        check = self.__s.recv(1024) # get true/false flag
        if check == b't\n':
            return True # elemenets found
        else:
            return False # queue is empty

    # Reads and returns queue objects from the server
    # returns -> a queue of the elements gathered from the server
    def ReadQueue(self): # read items in queue
        tmpQueue = queue.Queue()
        while(self.CheckQueue()):
            try:
                self.__s.sendall(b'QR\n')
                data = self.__s.recv(1024) # get data
                data = str(data.decode('utf-8'))
                newMsg = IgluMessage.IgluMessage(data)
                tmpQueue.put(newMsg) # add fetched data to queue
            except:
                return tmpQueue
        return tmpQueue # return queue