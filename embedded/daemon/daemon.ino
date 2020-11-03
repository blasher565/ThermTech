/*
 * First try at Iglu ATMega328p daemon
 * Programmer: Christian Wagner
 * Date Created: 11/02/2020
 * Date Modified: 11/02/2020
 */

// flags
const bool DEBUG = true;
const bool COMM_ENABLE = true;

// PIN setup
const int RELAY_PIN_1 = 8;
const int RELAY_PIN_2 = 9;
const int RELAY_PIN_3 = 10;
const int RELAY_PIN_4 = 11;

// init parameters
const int NUM_INIT_RELAYS = 3;

// the setup function runs once when you press reset or power the board
void setup() {
  // setup pins for relay control
  pinMode(RELAY_PIN_1, OUTPUT);
  digitalWrite(RELAY_PIN_1, HIGH);
  delay(50);
  pinMode(RELAY_PIN_2, OUTPUT);
  digitalWrite(RELAY_PIN_2, HIGH);
  delay(50);
  pinMode(RELAY_PIN_3, OUTPUT);
  digitalWrite(RELAY_PIN_3, HIGH);
  delay(50);
  pinMode(RELAY_PIN_4, OUTPUT);
  digitalWrite(RELAY_PIN_4, HIGH);
  delay(50);

  // start comms if enabled
  if(COMM_ENABLE) Serial.begin(9600);

  // signal start
  if(DEBUG && COMM_ENABLE) Serial.println("Doing init");

  // do init and check for success
  if(!doInit()) {
    Serial.println("doInit failed");
    exit(0);
  }
  
  // signal end
  if(DEBUG && COMM_ENABLE) Serial.println("Finished init");
}

// function for init
bool doInit() {
  digitalWrite(RELAY_PIN_1, LOW);
  digitalWrite(RELAY_PIN_2, LOW);
  digitalWrite(RELAY_PIN_3, LOW);
  digitalWrite(RELAY_PIN_4, LOW);

  delay(1000);

  digitalWrite(RELAY_PIN_1, HIGH);
  digitalWrite(RELAY_PIN_2, HIGH);
  digitalWrite(RELAY_PIN_3, HIGH);
  digitalWrite(RELAY_PIN_4, HIGH);

  delay(1000);

  for(int i = 0; i < NUM_INIT_RELAYS; i++) {
    // try all relays
    digitalWrite(RELAY_PIN_1, LOW);
    delay(50);
    digitalWrite(RELAY_PIN_1, HIGH);
    delay(50);
    digitalWrite(RELAY_PIN_2, LOW);
    delay(50);
    digitalWrite(RELAY_PIN_2, HIGH);
    delay(50);
    digitalWrite(RELAY_PIN_3, LOW);
    delay(50);
    digitalWrite(RELAY_PIN_3, HIGH);
    delay(50);
    digitalWrite(RELAY_PIN_4, LOW);
    delay(50);
    digitalWrite(RELAY_PIN_4, HIGH);
    delay(500);
  }

  return true;
}

// the loop function runs over and over again forever
void loop() {
  // check for serial commands
  if(Serial.available() > 0) {
    // get and confirm serial string
    String serialString = Serial.readString();
    
    if(DEBUG && COMM_ENABLE) Serial.print("RX: " + serialString);
    
    serialString.trim();
    
    // check for commands
    if(serialString.equals("STOP")) {
      // check for debug
      Serial.println("STOP called! Ending daemon.");
      // wait for serial to finish
      delay(5000);
      // stop daemon
      digitalWrite(RELAY_PIN_1, HIGH);
      digitalWrite(RELAY_PIN_2, HIGH);
      digitalWrite(RELAY_PIN_3, HIGH);
      digitalWrite(RELAY_PIN_4, HIGH);
      // kill process
      exit(0);
    } else if(serialString.equals("R1,1")) {
      digitalWrite(RELAY_PIN_1, LOW);
    } else if(serialString.equals("R1,0")) {
      digitalWrite(RELAY_PIN_1, HIGH);
    } else if(serialString.equals("R2,1")) {
      digitalWrite(RELAY_PIN_2, LOW);
    } else if(serialString.equals("R2,0")) {
      digitalWrite(RELAY_PIN_2, HIGH);
    } else if(serialString.equals("R3,1")) {
      digitalWrite(RELAY_PIN_3, LOW);
    } else if(serialString.equals("R3,0")) {
      digitalWrite(RELAY_PIN_3, HIGH);
    } else if(serialString.equals("R4,1")) {
      digitalWrite(RELAY_PIN_4, LOW);
    } else if(serialString.equals("R4,0")) {
      digitalWrite(RELAY_PIN_4, HIGH);
    }

    if(COMM_ENABLE) Serial.println("1");
    
  } 
}
