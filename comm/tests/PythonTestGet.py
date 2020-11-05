import ServerCommunication
import sys

print('This is a testing program for the interfaces!')

comm = ServerCommunication.ServerCommunication('localhost', 8189, 1)

if(not comm.open()):
    print('ERROR: Unable to open connection')
    sys.exit()

q = comm.ReadQueue()

if q == 'NULL':
    print("Queue returned is null!")
else:
    if q.empty():
        print("Queue was empty")
    else:
        print("Queue had items in it")
        while not q.empty():
            print(q.get().message)

if(not comm.close()):
    print('ERROR: Unable to close connection')
    sys.exit()

print('Program Exit')