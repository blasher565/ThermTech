import java.io.IOException;
import java.util.*;
import java.text.*;

import interfaces.*; // custom package

public class JavaTestSend {
    public static void main(String[] args) throws IOException, InterruptedException {
        System.out.println("This is a testing program for the interfaces!");
        System.out.println("This program sends data to the server.");

        Scanner in = new Scanner(System.in); // to get msg
        boolean run = true; // flow control
        ServerCommunication comm = new ServerCommunication("localhost", 8188, 3); // new server communication module

        // open connection
        if(!comm.open()) { System.out.println("ERROR: could not open connection."); return; }

        while(run) {
            System.out.print("Send Msg: ");
            String msg = in.nextLine();

            if(msg.equals("exit")) { run = false; continue; }

            SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            Date date = new Date();

            IgluMessage message = new IgluMessage(msg, formatter.format(date), 0, 1 /* Target PID */, 3 /* Sender's PID */); // create new message object

            if(!comm.WriteQueue(message)) System.exit(0);
        }

        in.close();

        // close connection
        if(!comm.close()) { System.out.println("ERROR: could not close connection."); return; }

        System.out.println("Program Exit");
    }
}