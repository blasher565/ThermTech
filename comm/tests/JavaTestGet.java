import java.io.IOException;
import java.util.*;

import interfaces.*;

public class JavaTestGet {
    public static void main(String[] args) throws IOException, InterruptedException {
        System.out.println("This is a testing program for the interfaces!");
        System.out.println("This program gets data from the server's queue.");

        ServerCommunication comm = new ServerCommunication("localhost", 8189, 2); // new server communication module

        // open connection
        if(!comm.open()) { System.out.println("ERROR: could not open connection."); return; }

        Queue<IgluMessage> queue = comm.ReadQueue(); // read queue items

        if(queue != null) {
            if(!queue.isEmpty()) System.out.println("Items:");
            else System.out.println("Queue was empty!");

            while(!queue.isEmpty()) {
                System.out.println(queue.poll().getMessage());
            }
        } else 
            System.out.println("Queue returned is null!");

        // close connection
        if(!comm.close()) { System.out.println("ERROR: could not close connection."); return; }

        System.out.println("Program Exit");
    }
}