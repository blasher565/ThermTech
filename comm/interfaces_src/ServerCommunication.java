package interfaces;

import java.io.*;
import java.net.*;
import java.util.*;

/**
 * <code>ServerCommunication</code> class used to access interprocess communication server
 * Programmer: Christian Wagner
 * Date Created: 3/11/2020
 * Date Modified: 11/02/2020
 * Version: 2.0
 */
//
public class ServerCommunication {
    // debug messages flag
    private final boolean DEBUG_FLAG = false;

    // defaults
    private final String DEFAULT_HOST = "localhost"; // default host name
    private final int DEFAULT_PORT = 8189; // default port number
    private final int COORDINATION_PORT = 18000; // port for communication coordination
    private final int RETRY_CONNECTION_WAIT = 1; // time to wait, in seconds, between retries
    private final int RETRY_CONNECTION_COUNT = 10; // number of times to retry before giving up

    // object variables
    private String host; // host name
    private int port; // port number
    private int PID; // process identification number
    private Socket socket; // client socket
    private DataOutputStream write; // client socket write stream
    private BufferedReader read; // client socket read stream

    /**
     * Default constructor for <code>ServerCommunication</code> class
     */
    public ServerCommunication() {
        this.host = DEFAULT_HOST;
        this.port = DEFAULT_PORT;
        this.PID = 0;
    }

    /**
     * Overloaded constructor for <code>ServerCommunication</code> class
     * @param host host name
     * @param port port number being served on
     * @param PID process identification number
     */
    public ServerCommunication(String host, int port, int PID) {
        this.host = host;
        this.port = port;
        this.PID = PID;
    }

    /**
     * Getter for the process identification number
     * @return process identification number
     */
    public int getPID() {
        return this.PID;
    }


    /**
     * Connect to server using given host and port parameters, only tries once
     * @return true if connection was established, false otherwise
     */
    private boolean connect() {
        try {
            // do coordination
            socket = new Socket(host, COORDINATION_PORT);
            write = new DataOutputStream(socket.getOutputStream());
            read = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            // ensure connection was made, if not, try again
            if(!socket.isConnected()) {
                if(DEBUG_FLAG) System.out.println("Connection on coordination port failed!");

                // clear vars
                socket = null;
                write = null;
                read = null;

                // try to make connection again
                for(int i = 0; i < RETRY_CONNECTION_COUNT; i++) {
                    if(DEBUG_FLAG) System.out.println("Retrying connection on coordination port");

                    socket = new Socket(host, COORDINATION_PORT);
                    write = new DataOutputStream(socket.getOutputStream());
                    read = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                    try {
                        Thread.sleep(RETRY_CONNECTION_WAIT * 1000); // wait
                    } catch(InterruptedException e){
                        return false;
                    }

                    if(socket.isConnected()) break; // connection was made

                    // clear and restart
                    socket = null;
                    write = null;
                    read = null;
                }

                if(!socket.isConnected()) return false; // connection failed
            }

            if(DEBUG_FLAG) System.out.println("Connected to coordination port!");

            String output = port + "\n";
            write.write(output.getBytes()); // communicate desired port
            String status = read.readLine();
            if(status.equals("a")) {
                this.disconnect(); // don't care about return
                // connection accepted, port is open
                socket = new Socket(host, port);
                write = new DataOutputStream(socket.getOutputStream());
                read = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                this.write.writeUTF("PID=" + this.PID + "\n"); // send PID information
                return true;
            } else {
                this.disconnect(); // don't care about return

                if(DEBUG_FLAG) System.out.println("Coordination failed.");
                if(DEBUG_FLAG) System.out.println("Selected port is being used.");

                return false;
            }
        } catch (IOException e) { return false; }
    }

    /**
     * Disconnect from the server
     * @return true if disconnect was successful, false otherwise
     */
    private boolean disconnect() {
        try {
            this.write.writeUTF("exit\n"); // signal exit
            write.close(); // close open write stream
            read.close(); // close open read stream
            socket.close(); // close open connection
            write = null; // clear variable
            read = null; // clear variable
            socket = null; // clear variable
        } catch (IOException e) { return false; }

        return true;
    }

    /**
     * Open the current connection to the server
     * @return trye if open was successful, false otherwise
     */
    public boolean open() {
        if(socket != null) if(socket.isConnected()) return true; // socket was already open
        return this.connect();
    }

    /**
     * Close the current connection to the server
     * @return true if close was successful, false otherwise
     */
    public boolean close() {
        if(socket != null) if(socket.isClosed()) return true; // socket was already closed
        if(socket == null) return true; // socket was already closed
        else return this.disconnect(); // trying to disconnect
    }

    /**
     * Send data to the server for the queue
     * @param msg the data to send
     * @return returns true if successful, false otherwise
     */
    public boolean WriteQueue(IgluMessage msg) {
        if(!socket.isConnected()) return false; // catch socket not being connected

        try {
            // send data to server
            this.write.writeUTF("QW\n");
            this.write.writeUTF((msg == null) ? "NULL" : msg.getTxData()); // send from IgluMessage object
            this.write.writeUTF("\n");
        } catch (IOException e) { return false; }

        return true;
    }

    /**
     * Check for items in the queue
     * @return returns true if items are in the queue, false otherwise
     */
    private boolean CheckQueue() {
        if(!socket.isConnected()) return false; // catch socket not being connected

        try {
            this.write.writeUTF("QC\n");
            String tmp = this.read.readLine();
            return (tmp.equals("t")) ? true : false;
        } catch (IOException e) { return false; }

    }

    /**
     * Reads and returns queue objects from the server
     * @return a queue of the elements gathered from the server
     */
    public Queue<IgluMessage> ReadQueue() {
        Queue<IgluMessage> tmpQueue = new LinkedList<IgluMessage>(); // queue object to build

        while(CheckQueue()) {
            try {
                this.write.writeUTF("QR\n");
                String rawData = this.read.readLine();
                IgluMessage newMsg = new IgluMessage(rawData);
                tmpQueue.add(newMsg); // add next item to queue
            } catch (IOException e) { return tmpQueue; }
        }

        return tmpQueue;
    }
}
