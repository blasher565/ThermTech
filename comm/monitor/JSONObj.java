import java.util.ArrayList;
import java.io.IOException;

/**
 * The <code>JSONObj</code> class provides the functions needs to encode and decode JSON data
 * Programmer: Christian Wagner
 * Date Created: 4/04/2020
 * Date Modified: 4/19/2020
 * Version: 1.0
 */

public class JSONObj {
    
    private ArrayList<String> keyList; // list of JSON keys
    private ArrayList<String> valueList; // list of JSON values

    // default constructor
    public JSONObj() {
        this.keyList = new ArrayList<String>();
        this.valueList = new ArrayList<String>();
    }

    // overloaded constructor for parsing string JSON data
    public JSONObj(String dataStr) throws IOException {
        this.keyList = new ArrayList<String>(); // create blank list
        this.valueList = new ArrayList<String>(); // create blank list
        boolean error = false; // signals error in building object

        // check beginning and end
        if(dataStr.substring(0, 2).equals("{ ") && dataStr.substring(dataStr.length() - 2, dataStr.length()).equals(" }")) {
            String tmpStr = "";
            boolean foundQuote = false;
            boolean isKey = false;
            boolean isObj = false;
            int bracketCounter = 0;
            char last = 'v';
            for(int i = 2; i < dataStr.length() - 2; i++) {
                char current = dataStr.charAt(i);
                if(current == '{') {
                    // beginning of embedded object
                    bracketCounter++;
                    isObj = true;
                    tmpStr += current;
                } else if(current == '}') {
                    bracketCounter--;
                    // check for end of object or another embedded object
                    if(bracketCounter == 0) {
                        tmpStr += current; 
                        isObj = false; 
                        this.valueList.add(tmpStr); 
                        tmpStr = "";
                        last = 'v';
                    } else tmpStr += dataStr.charAt(i);
                } else if(isObj) {
                    tmpStr += dataStr.charAt(i);
                } else if(current == '"' && !foundQuote) {
                    foundQuote = true;
                    // start of key or value
                    if(last == 'k') isKey = false;
                    else isKey = true;
                } else if (current == '"' && foundQuote) {
                    foundQuote = false;
                    // end of key or value
                    if(isKey) { last = 'k'; isKey = false; this.keyList.add(tmpStr); }
                    else { last = 'v'; this.valueList.add(tmpStr); }
                    tmpStr = "";
                } else if (foundQuote) {
                    tmpStr += dataStr.charAt(i);
                }
            }
        } else error = true;
        
        if(error) throw new IOException();
    }

    // returns size of JSON object (number of key/value pairs)
    public int size() { return this.keyList.size(); }

    // returns list of all keys
    public ArrayList<String> keys() { return this.keyList; }

    // returns list of all values
    public ArrayList<String> values() { return this.valueList; }

    // put in a new key/value pair
    public void put(String key, String value) {
        this.keyList.add(key);
        this.valueList.add(value);
    }

    // put in a new key/value pair, value is another <code>JSONObj</code>
    public void put(String key, JSONObj addObj) {
        this.keyList.add(key);
        this.valueList.add(addObj.toString());
    }

    public boolean remove(String key) {
        int index = this.keyList.indexOf(key);
        if(index == -1) return false;
        else { this.keyList.remove(index); this.valueList.remove(index); return true; }
    }

    // clears entire <code>JSONObj</code>
    public void clear() {
        this.keyList.clear();
        this.valueList.clear();
    }

    // get value for the given key
    public String get(String key) {
        int index = this.keyList.indexOf(key);
        if(index == -1) return null;
        else return this.valueList.get(index);
    }

    // overridden toString method
    public String toString() {
        String msg = "{ ";
        if(this.keyList.size() == this.valueList.size()) {
            for(int i = 0; i < this.keyList.size(); i++) {
                msg += "\"" + this.keyList.get(i) + "\"";
                msg += ": ";

                // check for object equivalent as value
                String tmp = this.valueList.get(i);
                if(tmp.length() > 2) { 
                    if((tmp.substring(0, 2).equals("{ "))) 
                        msg += this.valueList.get(i); // value was object
                    else
                        msg += "\"" + this.valueList.get(i) + "\""; // value was string
                } else 
                    msg += "\"" + this.valueList.get(i) + "\""; // value was string

                // check if not last element
                if(!((i + 1) == this.keyList.size())) msg += ", ";
            }
        }

        msg += " }";

        return msg;
    }
}