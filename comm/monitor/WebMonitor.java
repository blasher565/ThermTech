import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import javax.net.ssl.HttpsURLConnection;
import java.nio.charset.StandardCharsets;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.Thread;
import java.util.Queue;
import java.util.Map;
import java.util.Scanner;

import interfaces.*; // custom package

/**
 * Description: this program runs in the background and monitors/manages all outgoing and incoming information between
 * the device and the web server
 * 
 * Programmer: Christian Wagner
 * Date Created: 3/26/2020
 * Date Modified: 11/02/2020
 * Version: 1.0
 */

public class WebMonitor {
    // basic variables
    private static final String CONFIG_FILE = "./monitor_config.txt"; // location of local WebMonitor configuration file
    private static final String LOG_FILE = "./monitor_log.txt"; // location for log file to be placed
    private static boolean DEBUG_FLAG = false; // debug messages flag, true = show & false = hide
    private static File LOG_HANDLE = new File(LOG_FILE); // handle for monitor's log file
    private static int RESET_COUNT = 0; // track for number of resets

    // log message type variables
    private static final int MESSAGE_TYPE_ATTENTION = 0; // normal message
    private static final int MESSAGE_TYPE_WARNING = 1; // abnormal message
    private static final int MESSAGE_TYPE_ERROR = 2; // terminal message

    // WebMonitor config values
    private static URL serverAddress; // the address of the web server
    private static int interval; // time, in minutes, in between checks
    private static int timeout; // time, in seconds, that signals a timeout
    private static int assignedPID; // PID to monitor
    private static int port; // requested port for connection to interprocess server
    private static int failsafePort; // failsafe port for connection to interprocess server
    private static boolean secureConnection; // true for SSL connection, false otherwise

    // HttpURLConnection config values
    private static String connectionRequestMethod; // request method for server connection
    private static String connectionUserAgent; // agent name for server connection
    private static String connectionContentType; // content type for server connection

    // WebMonitor default config values
    private static final int INTERVAL_DEFAULT = 2; // default time, in minutes, in between checks
    private static final int TIMEOUT_DEFAULT = 30; // default time, in seconds, that signals a timeout
    private static final int PID_DEFAULT = -1; // default PID to monitor
    private static final int PORT_DEFAULT = 8100; // default requested port for connection to interprocess server
    private static final int FAIL_PORT_DEFAULT = 8101; // default failsafe port for connection to interprocess server
    private static final boolean SECURE_CONNECTION_DEFAULT = false; // default to unsecure connection

    // HttpURLConnection default config values
    private static String CONNECTION_REQUEST_METHOD_DEFAULT = "POST"; // default request method for server connection
    private static String CONNECTION_USER_AGENT_DEFAULT = "Java client"; // default agent name for server connection
    private static String CONNECTION_CONTENT_TYPE_DEFAULT = "application/x-www-form-urlencoded"; // default content type for server connection

    public static void main(final String[] args) {

        writeLog("Starting WebMonitor process.", MESSAGE_TYPE_ATTENTION); // write log
        init(CONFIG_FILE);

        if (!test()) {
            writeLog("First test failed. Program must now exit.", MESSAGE_TYPE_ERROR); // write log
            System.exit(0);
        }

        // start monitor service
        MonitorWorker monitor = new MonitorWorker("localhost", port, assignedPID);
        writeLog("New monitor thread started.", MESSAGE_TYPE_ATTENTION); // write log

        // BEGIN terminal interface
        final Scanner read = new Scanner(System.in);
        System.out.print("WebMonitor> ");
        while (read.hasNextLine()) {
            final String tmp = read.nextLine();
            switch (tmp) {
                case "dvals":
                    System.out.println();
                    System.out.println("Current Defaults");
                    System.out.println("INTERVAL_DEFAULT=" + INTERVAL_DEFAULT);
                    System.out.println("TIMEOUT_DEFAULT=" + TIMEOUT_DEFAULT);
                    System.out.println("PID_DEFAULT=" + PID_DEFAULT);
                    System.out.println("PORT_DEFAULT=" + PORT_DEFAULT);
                    System.out.println("FAIL_PORT_DEFAULT=" + FAIL_PORT_DEFAULT);
                    System.out.println("SECURE_CONNECTION_DEFAULT=" + SECURE_CONNECTION_DEFAULT);
                    System.out.println("CONNECTION_REQUEST_METHOD_DEFAULT=" + CONNECTION_REQUEST_METHOD_DEFAULT);
                    System.out.println("CONNECTION_USER_AGENT_DEFAULT=" + CONNECTION_USER_AGENT_DEFAULT);
                    System.out.println("CONNECTION_CONTENT_TYPE_DEFAULT=" + CONNECTION_CONTENT_TYPE_DEFAULT);
                    System.out.println();
                    writeLog("dvals command completed.", MESSAGE_TYPE_ATTENTION); // write log
                    break;
                case "cvals":
                    System.out.println();
                    System.out.println("Current Values");
                    System.out.println("server=" + serverAddress.toExternalForm());
                    System.out.println("interval=" + interval);
                    System.out.println("timeout=" + timeout);
                    System.out.println("pid=" + assignedPID);
                    System.out.println("port=" + port);
                    System.out.println("failport=" + failsafePort);
                    System.out.println("secure=" + (secureConnection ? "yes" : "no"));
                    System.out.println("method=" + connectionRequestMethod);
                    System.out.println("user-agent=" + connectionUserAgent);
                    System.out.println("content-type=" + connectionContentType);
                    System.out.println();
                    writeLog("cvals command completed.", MESSAGE_TYPE_ATTENTION); // write log
                    break;
                case "reset":
                    writeLog("Attempting to reset monitor.", MESSAGE_TYPE_ATTENTION); // write log
                    
                    // interrupt monitor service
                    if(monitor.stop()) writeLog("Monitor thread has been interrupted.", MESSAGE_TYPE_ATTENTION); // write log
                    else {
                        writeLog("Monitor thread failed to terminate. Reset failed.", MESSAGE_TYPE_WARNING); // write log
                        continue;
                    }

                    init(CONFIG_FILE);
                    if (!test()) {
                        writeLog("Server connection test failed.", MESSAGE_TYPE_ERROR); // write log
                        System.exit(0);
                    }

                    // start monitor service again
                    monitor = new MonitorWorker("localhost", port, assignedPID);
                    writeLog("Reset has finished successfully.", MESSAGE_TYPE_ATTENTION); // write log
                    if(DEBUG_FLAG) System.out.println(); // new line if terminal messages are on

                    RESET_COUNT++; // increment reset counter
                    writeLog("Reset count: " + RESET_COUNT, MESSAGE_TYPE_ATTENTION); // write log
                    writeLog("reset command completed.", MESSAGE_TYPE_ATTENTION); // write log
                    break;
                case "test":
                    writeLog("Running connection test.", MESSAGE_TYPE_ATTENTION); // write log
                    System.out.println("Running connection test...");

                    String result = (test() ? "OK" : "Not connected"); // store test result

                    System.out.println("Test: " + result);
                    writeLog("Test connection returned: " + result, MESSAGE_TYPE_ATTENTION); // write log
                    System.out.println();
                    writeLog("test command completed.", MESSAGE_TYPE_ATTENTION); // write log
                    break;
                case "debug=on":
                    if(DEBUG_FLAG) System.out.println("WARNING: DEBUG_FLAG is already enabled.");
                    else {
                        DEBUG_FLAG = true;
                        System.out.println("ATTENTION: DEBUG_FLAG has been turned on.");
                    }
                    writeLog("debug command completed. Switch is on.", MESSAGE_TYPE_ATTENTION); // write log
                    break;
                case "debug=off":
                    if(!DEBUG_FLAG) System.out.println("WARNING: DEBUG_FLAG is not enabled!");
                    else {
                        DEBUG_FLAG = false;
                        System.out.println("ATTENTION: DEBUG_FLAG has been turned off.");
                    }
                    writeLog("debug command completed. Switch is off.", MESSAGE_TYPE_ATTENTION); // write log
                    break;
                case "print=reset":
                    System.out.println("Number of resets: " + RESET_COUNT);
                    System.out.println();
                    writeLog("print command completed. Showed resets.", MESSAGE_TYPE_ATTENTION); // write log
                    break;
                case "print=debug":
                    System.out.println("Debug flag status: debug=" + (DEBUG_FLAG ? "on" : "off"));
                    System.out.println();
                    writeLog("print command completed. Showed debug flag.", MESSAGE_TYPE_ATTENTION); // write log
                    break;
                case "exit":
                    if(monitor.stop()) writeLog("Monitor thread has been interrupted.", MESSAGE_TYPE_ATTENTION); // write log
                    writeLog("exit command completed. Now exiting program.", MESSAGE_TYPE_ATTENTION); // write log
                    System.exit(0);
                    break;
            }
            System.out.print("WebMonitor> ");
        }

        read.close();

        writeLog("END PROGRAM", MESSAGE_TYPE_ATTENTION); // write log
        // END terminal interface
    }

    private static void init(final String config_addr) {
        try {
            // default config values
            interval = INTERVAL_DEFAULT;
            timeout = TIMEOUT_DEFAULT;
            assignedPID = PID_DEFAULT;
            port = PORT_DEFAULT;
            failsafePort = FAIL_PORT_DEFAULT;
            secureConnection = SECURE_CONNECTION_DEFAULT;
            connectionRequestMethod = CONNECTION_REQUEST_METHOD_DEFAULT;
            connectionUserAgent = CONNECTION_USER_AGENT_DEFAULT;
            connectionContentType = CONNECTION_CONTENT_TYPE_DEFAULT;

            // print header
            if(DEBUG_FLAG) System.out.println("\n\n");
            if(DEBUG_FLAG) System.out.println("----- INIT DETAILS -----");

            final Scanner read = new Scanner(new File(config_addr));
            while (read.hasNextLine()) {
                // read line and configure
                final String tmp = read.nextLine();
                if (tmp.equals("") || tmp.substring(0, 2).equals("//")) {
                    // empty or comment so just skip
                    continue;
                } else {
                    final String[] splitStr = tmp.split("=");
                    switch (splitStr[0]) {
                        case "server":
                            try {
                                serverAddress = new URL(splitStr[1]);
                                if(DEBUG_FLAG) System.out.println("Server address has been set to " + serverAddress.toExternalForm());
                            } catch (final MalformedURLException e) {
                                writeLog("Failed to set server address.", MESSAGE_TYPE_ERROR); // write log
                                System.exit(0);
                            }
                            break;
                        case "interval":
                            try {
                                interval = Integer.parseInt(splitStr[1]);
                                if(DEBUG_FLAG) System.out.println("Interval has been set to " + interval);
                            } catch (final Exception e) {
                                interval = INTERVAL_DEFAULT;
                                writeLog("Interval config value error. Default has been set.", MESSAGE_TYPE_WARNING); // write log
                            }
                            break;
                        case "timeout":
                            try {
                                timeout = Integer.parseInt(splitStr[1]);
                                if(DEBUG_FLAG) System.out.println("Timeout has been set to " + timeout);
                            } catch (final Exception e) {
                                timeout = TIMEOUT_DEFAULT;
                                writeLog("Timeout config value error. Default has been set.", MESSAGE_TYPE_WARNING); // write log
                            }
                            break;
                        case "pid":
                            try {
                                assignedPID = Integer.parseInt(splitStr[1]);
                                if(DEBUG_FLAG) System.out.println("PID has been set to " + assignedPID);
                            } catch (final Exception e) {
                                assignedPID = PID_DEFAULT;
                                writeLog("PID-to-monitor config value error. Default has been set.", MESSAGE_TYPE_WARNING); // write log
                            }
                            break;
                        case "port":
                            try {
                                port = Integer.parseInt(splitStr[1]);
                                if(DEBUG_FLAG) System.out.println("Main port has been set to " + port);
                            } catch (final Exception e) {
                                port = PORT_DEFAULT;
                                writeLog("Server connection port config value error. Default has been set.", MESSAGE_TYPE_WARNING); // write log
                            }
                            break;
                        case "failport":
                            try {
                                failsafePort = Integer.parseInt(splitStr[1]);
                                if(DEBUG_FLAG) System.out.println("Failsafe port has been set to " + failsafePort);
                            } catch (final Exception e) {
                                failsafePort = FAIL_PORT_DEFAULT;
                                writeLog("Failsafe server connection port config value error. Default has been set.", MESSAGE_TYPE_WARNING); // write log
                            }
                            break;
                        case "secure":
                            if(splitStr[1].equals("yes")) secureConnection = true;
                            else secureConnection = false;
                            if(DEBUG_FLAG) System.out.println("Secure connection has been set to " + secureConnection);
                            break;
                        case "method":
                            connectionRequestMethod = splitStr[1];
                            if(DEBUG_FLAG) System.out.println("Connection request method has been set to " + connectionRequestMethod);
                            break;
                        case "user-agent":
                            connectionUserAgent = splitStr[1];
                            if(DEBUG_FLAG) System.out.println("Connection user-agent has been set to " + connectionUserAgent);
                            break;
                        case "content-type":
                            connectionContentType = splitStr[1];
                            if(DEBUG_FLAG) System.out.println("Connection content-type has been set to " + connectionContentType);
                            break;
                    }
                }
            }

            if(DEBUG_FLAG) System.out.println("\n\n");
            writeLog("Configuration complete.", MESSAGE_TYPE_ATTENTION); // write log
        } catch (final FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    private static String write(final String params) {
        if(!secureConnection) {
            try {
                // open connection to server
                final HttpURLConnection serverConnection = (HttpURLConnection)serverAddress.openConnection();
    
                writeLog("HTTP conection opened. " + params, MESSAGE_TYPE_ATTENTION); // write log

                // setup configs
                serverConnection.setDoOutput(true);
                serverConnection.setRequestMethod(connectionRequestMethod);
                serverConnection.setRequestProperty("User-Agent", connectionUserAgent);
                serverConnection.setRequestProperty("Content-Type", connectionContentType);
    
                // create write stream
                final DataOutputStream writeOut = new DataOutputStream(serverConnection.getOutputStream());
    
                // create POST data byte array
                final byte[] postData = params.getBytes(StandardCharsets.UTF_8);
    
                // send POST data to server
                writeOut.write(postData);
    
                // create read stream
                final BufferedReader readIn = new BufferedReader(new InputStreamReader(serverConnection.getInputStream()));
    
                // read and return response
                final String output = readIn.readLine();

                writeLog("Post data sent: " + params, MESSAGE_TYPE_ATTENTION); // write log
                writeLog("Data received: " + output, MESSAGE_TYPE_ATTENTION); // write log
                writeLog("HTTP conection closed. " + params, MESSAGE_TYPE_ATTENTION); // write log

                return output;
            } catch (final IOException e) {
                writeLog("HTTP Connection failed.", MESSAGE_TYPE_ERROR);
                return null;
            }
        } else {
            try {
                // open secure connection to server
                final HttpsURLConnection serverConnection = (HttpsURLConnection)serverAddress.openConnection();

                writeLog("HTTPS conection opened. " + params, MESSAGE_TYPE_ATTENTION); // write log
    
                // setup configs
                serverConnection.setDoOutput(true);
                serverConnection.setRequestMethod(connectionRequestMethod);
                serverConnection.setRequestProperty("User-Agent", connectionUserAgent);
                serverConnection.setRequestProperty("Content-Type", connectionContentType);
    
                // create write stream
                final DataOutputStream writeOut = new DataOutputStream(serverConnection.getOutputStream());
    
                // create POST data byte array
                final byte[] postData = params.getBytes(StandardCharsets.UTF_8);
    
                // send POST data to server
                writeOut.write(postData);
    
                // create read stream
                final BufferedReader readIn = new BufferedReader(new InputStreamReader(serverConnection.getInputStream()));
    
                // read and return response
                final String output = readIn.readLine();

                writeLog("Post data sent: " + params, MESSAGE_TYPE_ATTENTION); // write log
                writeLog("Data received: " + output, MESSAGE_TYPE_ATTENTION); // write log
                writeLog("HTTPS conection closed. " + params, MESSAGE_TYPE_ATTENTION); // write log

                return output;
            } catch (final IOException e) {
                writeLog("HTTPS Connection failed.", MESSAGE_TYPE_ERROR);
                return null;
            }
        }
    }

    public static boolean test() {
        final String test = write("test=1");
        if(DEBUG_FLAG) System.out.println("Test: " + test);
        return test == null ? false : (test.equals("y") ? true : false);
    }

    // write to log file
    private static void writeLog(String msg, int type) {
        try {
            FileWriter write = new FileWriter(LOG_HANDLE, true);

            // decide message type
            switch(type) {
                case MESSAGE_TYPE_ATTENTION:
                    // attention message
                    msg = "ATTENTION: " + msg;
                    break;
                case MESSAGE_TYPE_WARNING:
                    // warning message
                    msg = "WARNING: " + msg;
                    break;
                case MESSAGE_TYPE_ERROR:
                    // error message
                    msg = "ERROR: " + msg;
                    break;
            }

            // ****** OLD CODE ******    java.util.Date tmpDate = new java.util.Date();    ****** OLD CODE ******
            // add timestamp
            msg += (" - " + (new java.util.Date().toString()));

            // add newline character
            msg += "\n";

            // write to file
            write.write(msg);

            // close stream
            write.close();

            // write message to terminal if DEBUG_FLAG is on
            if(DEBUG_FLAG) System.out.println(msg);
        } catch(IOException e) {
            e.printStackTrace();
        }
    }

    public static class MonitorWorker implements Runnable {
        Thread mainThread;
        ServerCommunication comm;

        MonitorWorker(String host, int portNum, int PIDNum) {
            mainThread = new Thread(this);
            comm = new ServerCommunication("localhost", portNum, PIDNum);
            mainThread.start();
        }

        @Override
        public void run() {
            try {
                this.handleMonitor();
            } catch (InterruptedException e) {
                //e.printStackTrace();
                //System.out.println("WARNING: MonitorWorker thread interrupted!");
            }
        }

        private void handleMonitor() throws InterruptedException {
            boolean done = false;
            boolean link = false;

            // open connection with interprocess server
            this.open();

            Queue<IgluMessage> queue;

            while(!done) {
                queue = comm.ReadQueue(); // read queue items

                if(!link) Thread.sleep(5000/*interval * 60000*/);
                else System.out.println("Link active!");

                if(queue.isEmpty()) continue; // no new messages

                // create new object for JSON data
                JSONObj mainObj = new JSONObj();

                int current = 0;

                for(IgluMessage tmpMsg : queue) {
                    // Ensure message is not null
                    if(tmpMsg == null) break;

                    // JSON object for current message
                    JSONObj currentObj = new JSONObj();

                    // Add message information to JSON object
                    currentObj.put("text", tmpMsg.getMessage());
                    currentObj.put("timestamp", tmpMsg.getTimestamp());
                    currentObj.put("sender", Integer.toString(tmpMsg.getSender()));

                    // Add current JSON object to main JSON object
                    mainObj.put(("msg" + current), currentObj);

                    // Clear current JSON object
                    currentObj.clear();
                    currentObj = null;

                    current++;
                }

                final String response = write("Messages=" + mainObj.toString() + ((link) ? "&Link=1" : "&Link=0"));
                writeLog("Response: " + response, MESSAGE_TYPE_ATTENTION);

                // ******     START     ******
                // This will be modified to fit the specific implementation on the server side
                // attempt to revert JSON response back into IgluMessage

                // TODO: NEED TO READ MESSAGE. ARE WE DOING XML OR JSON?

                try {
                    JSONObj responseObj = new JSONObj(response);
                    if(responseObj.keys().contains("msg")) {
                        IgluMessage responseMsg = new IgluMessage(responseObj.get("msg"), responseObj.get("tstamp"), Integer.parseInt(responseObj.get("lvl")), Integer.parseInt(responseObj.get("to")), -1 /* Signals web server as sender */);
                        if(DEBUG_FLAG) System.out.println("RESPONSE: " + responseMsg.getMessage());

                        // determine if message is system message or not
                        if(responseMsg.getMessage().equals("???")) {
                            // deal with system messages
                        } else {
                            comm.WriteQueue(responseMsg);
                        }
                    }
                
                    responseObj.clear();
                    responseObj = null;
                } catch (Exception e) {
                    if(DEBUG_FLAG) System.out.println("ERROR - Could not create JSON object from response (response: " + response + ")");
                }
                // ******     END     ******

                // Clear main JSON object
                mainObj.clear();
                mainObj = null;
            }

            // close connection with interprocess server and interrupt thread
            this.stop();

            return;
        }

        public boolean stop() {
            if(!comm.close()) if(DEBUG_FLAG) { System.out.println("ERROR: could not close connection."); return false; }
            mainThread.interrupt();
            return true;
        }

        public boolean open() {
            if(!comm.open()) if(DEBUG_FLAG) { System.out.println("ERROR: could not open connection to server."); return false; }
            return true;
        }
    }
}