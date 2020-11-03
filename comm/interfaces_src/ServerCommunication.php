<?php

require_once('IgluMessage.php');

/*
    Description: PHP class/functions used to access interprocess communication server
    Programmer: Christian Wagner
    Date Created: 3/11/2020
    Date Modified: 11/02/2020
    Version: 2.0
*/

class ServerCommunication {
    private $DEBUG_FLAG = FALSE;

    // defaults
    private $DEFAULT_HOST = 'localhost';
    private $DEFAULT_PORT = 8189;
    private $COORDINATION_PORT = 18000;

    // object variables
    private $host; // host name
    private $port; // port number
    private $pid; // process identification number
    private $socket; // client socket

    /*
        Constructor
    */
    function __construct() {
        if(func_num_args() == 3) {
            $args = func_get_args(); // get arguments
            $this->constructAll( $args[0], $args[1], $args[2] );
        } else
            $this->constructNone();
        $this->connect(1, 1000);
    }

    /*
        Constructor for no argument instance
    */
    function constructNone() {
        $this->host = $this->DEFAULT_HOST;
        $this->port = $this->DEFAULT_PORT;
        $this->pid = 0;
    }

    /*
        Constructor for all argument instance
        $host -> host name
        $port -> port number
        $pid -> process identification number
    */
    function constructAll( $host, $port, $pid ) {
        $this->host = $host;
        $this->port = $port;
        $this->pid = $pid;
    }

    /*
        Getter for the process identification number
        return -> process identification number
    */
    function getPID() {
        return $this->pid;
    }

    /*
        Connect to server using given host and port parameters, retry connection t times if refused
        $t -> number of times to retry connection
        $interval -> time, in milliseconds, between connection attempts
        return -> 1 if connection was established, 0 otherwise
    */
    private function connect( $t, $interval ) {
        for($i = 0; $i < $t; $i++) {
            $this->socket = fsockopen( $this->host, $this->COORDINATION_PORT, $errno, $errstr, 30 /* default timeout */ );
            if ( !$this->socket ) {
                echo "$errstr ($errno)<br />\n";
                return 0;
            } else {
                $this->write($this->port);
                if( $this->read() == "a\n" ) {
                    $this->disconnect();
                    $this->socket = fsockopen( $this->host, $this->port, $errno, $errstr, 30 /* default timeout */ );
                    $this->write( "PID=" . $this->pid );
                    return 1;
                } else {
                    $interval /= 1000; // convert from milliseconds
                    sleep( $interval );

                    if($this->DEBUG_FLAG) echo 'Coordination failed!';
                    if($this->DEBUG_FLAG) echo 'The selected port is being used.';
                    if($this->DEBUG_FLAG) echo 'Attempt ' . ( $i + 1 ) . ' out of ' . $t;
                    
                    $this->disconnect();
                }
            }
        }

        return 0;
    }

    /*
        Disconnect from the server
    */
    private function disconnect() {
        $this->write( "exit" ); // signal exit
        fclose( $this->socket ); // close socket connection
    }

    /*
        Write data to the server
        $str -> the data to write
    */
    private function write( $str ) {
        fwrite( $this->socket, $str . "\n" );
    }

    /*
        Read data from the server
        return -> data from the server
    */
    private function read() {
        return fgets( $this->socket, 128 );
    }

    /*
        Send data to the server for the queue
        $msg -> the data to send
    */
    function WriteQueue( $msg ) {
        $this->write( "QW" ); // Queue Write
        if( isset( $msg ) )
            $this->write( $msg->getTxData() );
        else
            $this->write( 'NULL' );
    }

    /*
        Check for items in the queue
        return -> 1 if items are in the queue, 0 otherwise
    */
    private function CheckQueue() {
        $this->write( "QC" ); // Queue Check
        if( $this->read() == "t\n" )
            return 1;
        else
            return 0;
    }

    /*
        Reads and returns queue elements from the server
        return -> an array of elements gathered from the server
    */
    function ReadQueue() {
        for( $i = 0; $this->CheckQueue(); $i++ ) {
            $this->write( "QR" ); // Queue Read
            $queue[$i] = new IgluMessage( $this->read() );
        }
        return $queue;
    }
}
?>