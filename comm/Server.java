import java.io.*;
import java.net.*;
import java.util.*;

import interfaces.IgluMessage; // custom package

/**
 * <code>Server</code> class used to host <code>ServerSocket</code> for inter-process communication
 * Programmer: Christian Wagner
 * Date Created: 3/11/2020
 * Date Modified: 11/02/2020
 * Version: 2.0
 */

public class Server {
    // debug messages flag
    private static final boolean DEBUG_FLAG = true;

    private static final int COORDINATION_PORT = 18000; // port for communication coordination
    private static final int MAX_NUMBER_CONNECTIONS = 20; // max number of server connections to allow
    private static ArrayList<interfaces.IgluMessage> queue = new ArrayList<interfaces.IgluMIgluMessageessage>(); // queue for all inter-process messages
    private static ArrayList<Integer> openPorts = new ArrayList<Integer>(); // list of open ports
    private static ArrayList<Thread> openServers = new ArrayList<Thread>(); // all open ServerSocket threads

    public static void main(String[] args) throws IOException {

        System.out.println("Listening for connection requests on port " + COORDINATION_PORT);
        ServerSocket listenSocket = new ServerSocket(COORDINATION_PORT);
        Thread tmpClient = null;

        while(true) {
            if(DEBUG_FLAG) System.out.println("Waiting for request...");
            Socket clientSocket = listenSocket.accept();
            InputStream inStream = clientSocket.getInputStream(); // reading data in
            DataOutputStream outStream = new DataOutputStream(clientSocket.getOutputStream()); // writting data out
            Scanner in = new Scanner(inStream);
            boolean done = false;
            while(!done) {
                if(in.hasNextLine()) {
                    String port = in.nextLine().trim();

                    if(port.equals("test")) { 
                        if(DEBUG_FLAG) System.out.println("test message received");
                        continue; // just a connection test, ignore
                    }

                    if(DEBUG_FLAG) System.out.println("Port requested: " + port);

                    // check for dead threads and update thread list
                    for(int i = 0; i < openServers.size(); i++) {
                        Thread tmp = openServers.get(i);
                        if(!tmp.isAlive()) {
                            openServers.remove(tmp);
                            openPorts.remove(i);
                            if(DEBUG_FLAG) System.out.println("Found and removed dead thread.");
                        }
                    }

                    // check for port availability
                    if(openPorts.contains(Integer.parseInt(port)) || openPorts.size() == MAX_NUMBER_CONNECTIONS) {
                        // can't allow connection so respond with 'denied'
                        if(DEBUG_FLAG) System.out.println("Port connection denied!");
                        String output = "d\n";
                        outStream.write(output.getBytes());
                    } else {
                        // connection accepted
                        String output = "a\n";
                        openPorts.add(Integer.parseInt(port));
                        // create server for that port on thread
                        openServers.add(new Thread(new ServerWorker(Integer.parseInt(port))));
                        openServers.get(openServers.size() - 1).start();
                        // tell client it's ok to connect
                        outStream.write(output.getBytes());
                    }
                    done = true;
                }
            }
        }
    }

    public static class ServerWorker implements Runnable {
        private ServerSocket serverSocket;
        private Socket incoming;
        private int port;

        public ServerWorker(int port) {
            this.port = port;
        }

        @Override
        public void run() {
            try {
                this.serverSocket = new ServerSocket(port);
                this.incoming = serverSocket.accept();
                handleServer();
                this.incoming.close();
                this.serverSocket.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        private void handleServer() throws IOException, ClassNotFoundException {
            try {
                InputStream inStream = incoming.getInputStream(); // reading data in
                DataOutputStream write = new DataOutputStream(incoming.getOutputStream()); // writting data out
                try (Scanner in = new Scanner(inStream)) {
                    boolean done = false;
                    boolean toQ = false; // To Queue flag
                    boolean PIDFlag = false;
                    int currentPID = 0;
                    while(!done) {
                        if(in.hasNextLine()) {
                            String line = in.nextLine(); // get message from client

                            if(DEBUG_FLAG) System.out.println("Client said: " + line);

                            if(PIDFlag) {
                                switch(line.trim()) {
                                    case "exit": // close current socket
                                        done = true;
                                        toQ = false; // turn off To Queue flag
                                        break;
                                    case "QC": // Queue Check
                                        boolean flag = false;
                                        for(int i = 0; i < queue.size(); i++) {
                                            interfaces.IgluMessage tmp = queue.get(i);
                                            if(tmp.getTarget() == currentPID) {
                                                flag = true;
                                                break;
                                            }
                                        }
                                        if(flag) {
                                            String output = "t\n";
                                            write.write(output.getBytes());
                                        } else {
                                            String output = "f\n";
                                            write.write(output.getBytes());
                                        }
                                        break;
                                    case "QR": // Queue Read
                                        for(int i = 0; i < queue.size(); i++) {
                                            // step through the queue
                                            interfaces.IgluMessage tmp = queue.get(i);
                                            if(tmp.getTarget() == currentPID) {
                                                String output = tmp.getTxData() + "\n";
                                                write.write(output.getBytes());
                                                if(DEBUG_FLAG) System.out.println(output);
                                                queue.remove(i);
                                                break;
                                            }
                                        }
                                        break;
                                    case "QW": // Queue Write
                                        toQ = true;
                                        break;
                                    default:
                                        if(DEBUG_FLAG) System.out.println("Adding Data To Queue: " + line );

                                        if(toQ) {
                                            queue.add(new interfaces.IgluMessage(line));
                                            toQ = false;
                                        } else if(DEBUG_FLAG) System.out.println("Recieved test message.");

                                        break;
                                }
                            } else {
                                // PID not set
                                if(line.contains("PID=")) {
                                    String[] pieces = line.split("=");
                                    currentPID = Integer.parseInt(pieces[1]);
                                    PIDFlag = true;

                                    if(DEBUG_FLAG) System.out.println("PID value set for connection!");
                                    if(DEBUG_FLAG) System.out.println("Current PID = " + currentPID);

                                } else {

                                    if(DEBUG_FLAG) System.out.println("Client failed to provide PID upon first communication.");
                                    if(DEBUG_FLAG) System.out.println("Closing connection!");

                                    done = true; // close connection
                                }
                            }
                        }
                    }
                }
            } catch (EOFException | SocketException e) {
                e.printStackTrace();
            }

            if(DEBUG_FLAG) System.out.println("Connection has been closed");
        }
    }
}
