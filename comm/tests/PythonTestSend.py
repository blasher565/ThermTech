import ServerCommunication
import IgluMessage
import sys
from datetime import datetime

print('This is a testing program for the interfaces!')

run = True
comm = ServerCommunication.ServerCommunication('localhost', 8188, 2)

if(not comm.open()):
    print('ERROR: Unable to open connection')
    sys.exit()

while(run):
    tmp = input('Send Msg: ')
    if tmp == 'exit':
        run = False
    else:
        msg = IgluMessage.IgluMessage(tmp,datetime.now().strftime('%Y-%m-%d %H:%M:%S'),0,2,1)
        success = comm.WriteQueue(msg)
        if not success:
            print("Server was busy!")

if(not comm.close()):
    print('ERROR: Unable to close connection')
    sys.exit()

print('Program Exit')