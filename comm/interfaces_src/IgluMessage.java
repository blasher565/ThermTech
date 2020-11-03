package interfaces;

/**
 * <code>IgluMessage</code> class used to format messages between processes
 * Programmer: Christian Wagner
 * Date Created: 1/4/2020
 * Date Modified: 11/02/2020
 * Version: 2.0
 */
public class IgluMessage {
    // defaults
    private final String DEFAULT_MSG = "Message not set"; // default message text
    private final String DEFAULT_TIMESTAMP = "0000-00-00 00:00:00"; // default timestamp text
    private final String ERROR_MSG = "Error building message object"; // error message text

    // message data delimiter setting
    private final String FORMAT_DELIMITER = "&";

    // object variables
    private String message; // message text
    private String timestamp; // message time on sending timestamp
    private int priority; // message priority level
    private int target; // message target Process ID (PID)
    private int sender; // message sender's PID for return messages
    private boolean encoded; // message encrypted flag

    /**
     * Default constructor for the <code>IgluMessage</code> class
     */
    public IgluMessage() {
        this.message = DEFAULT_MSG;
        this.timestamp = DEFAULT_TIMESTAMP;
        this.priority = 0;
        this.target = 0;
        this.sender = 0;
        this.encoded = false;
    }

    /**
     * Overloaded constructor for the <code>IgluMessage</code> class
     * Constructs a <code>IgluMessage</code> object using given data
     * @param message message text
     * @param timestamp message time on sending timestamp
     * @param priority message priority level
     * @param target message target Process ID (PID)
     * @param sender message sender's PID for return messages
     */
    public IgluMessage(String message, String timestamp, int priority, int target, int sender) {
        this.message = message;
        this.timestamp = timestamp;
        this.priority = priority;
        this.target = target;
        this.sender = sender;
        this.encoded = false;
    }

    /**
     * Overloaded constructor for <code>IgluMessage</code> class
     * Constructs a <code>IgluMessage</code> object using raw data from the server
     * @param rawData data stream from server
     */
    public IgluMessage(String rawData) {
        String[] pieces = rawData.split(FORMAT_DELIMITER); // parse raw data

        // check length
        if(pieces.length == 6) {
            // get message part
            String[] tmp = pieces[0].split("=");
            if(tmp[0].contains("MESSAGE") && tmp.length == 2) this.message = tmp[1];
            else this.message = ERROR_MSG;

            // get timestamp part
            tmp = pieces[1].split("=");
            if(tmp[0].contains("TIMESTAMP") && tmp.length == 2) this.timestamp = tmp[1];
            else this.timestamp = DEFAULT_TIMESTAMP;

            // get priority part
            tmp = pieces[2].split("=");
            if(tmp[0].contains("PRIORITY") && tmp.length == 2) this.priority = Integer.parseInt(tmp[1]);
            else this.priority = 0;

            // get target part
            tmp = pieces[3].split("=");
            if(tmp[0].contains("TARGET") && tmp.length == 2) this.target = Integer.parseInt(tmp[1]);
            else this.target = 0;

            // get sender part
            tmp = pieces[4].split("=");
            if(tmp[0].contains("SENDER") && tmp.length == 2) this.sender = Integer.parseInt(tmp[1]);
            else this.sender = 0;

            // get encoded part
            tmp = pieces[5].split("=");
            if(tmp[0].contains("ENCODED") && tmp.length == 2) this.encoded = (tmp[1].equals("1") ? true : false);
            else this.encoded = false;
        } else {
            this.message = ERROR_MSG;
            this.timestamp = DEFAULT_TIMESTAMP;
            this.priority = 0;
            this.target = 0;
            this.sender = 0;
            this.encoded = false;
        }
    }

    /**
     * Returns the message text if the message is not encoded
     * @return the message text if encoded is false, "encoded" otherwise
     */
    public String getMessage() {
        if(!this.encoded) return this.message;
        else return "encoded";
    }

    /**
     * Returns timestamp text
     * @return timestamp text
     */
    public String getTimestamp() {
        return this.timestamp;
    }

    /**
     * Returns priority level
     * @return priority level
     */
    public int getPriority() {
        return this.priority;
    }

    /**
     * Returns target Process ID (PID)
     * @return target process ID (PID)
     */
    public int getTarget() {
        return this.target;
    }

    /**
     * Returns sender's Process ID (PID)
     * @return sender's process ID (PID)
     */
    public int getSender() {
        return this.sender;
    }

    /**
     * Returns value of encoded flag
     * @return 1 if encoded, 0 otherwise
     */
    public int isEncoded() {
        if(encoded) return 1;
        else return 0;
    }

    /**
     * Gets text form of data stored in <code>IgluMessage</code> object for sending to the server
     * @return the text form of the <code>IgluMessage</code> object
     */
    public String getTxData() {
        String sendData = "MESSAGE=" + this.message;
        sendData += FORMAT_DELIMITER + "TIMESTAMP=" + this.timestamp;
        sendData += FORMAT_DELIMITER + "PRIORITY=" + this.priority;
        sendData += FORMAT_DELIMITER + "TARGET=" + this.target;
        sendData += FORMAT_DELIMITER + "SENDER=" + this.target;
        sendData += FORMAT_DELIMITER + "ENCODED=" + ((this.encoded) ? 1 : 0);
        return sendData;
    }

    /**
     * Encrypts the message with a specific encoding and key
     * @param encoding the encoding to use
     * @param key the key to encrypt with
     */
    public void encode(String encoding, String key) {this.encoded = true;}

    /**
     * Decrypts the message with a specific encoding and key
     * @param encoding the encoding to use
     * @param key the key to encrypt with
     */
    public void decode(String encoding, String key) {this.encoded = false;}
}
