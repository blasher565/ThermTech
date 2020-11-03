<?php

/*
    Description: IgluMessage class used to format messages between processes
    Programmer: Christian Wagner
    Date Created: 1/11/2020
    Date Modified: 11/02/2020
*/

class IgluMessage {
    // defaults
    private $DEFAULT_MSG = 'Message not set'; // default message text
    private $DEFAULT_TIMESTAMP = '00-00-0000 00:00:00'; // default timestamp text
    private $ERROR_MSG = 'Error building message object'; // error message text

    // message data delimiter setting
    private $FORMAT_DELIMITER = '@';

    // object variables
    private $message; // message text
    private $timestamp; // message time on sending timestamp
    private $priority; // message priority level
    private $target; // message target Process ID (PID)
    private $encoded; // message encrypted flag

    /*
        Constructor
    */
    function __construct() {
        $numargs = func_num_args();
        $args = func_get_args();
        if( $numargs == 0 )
            $this->fromNothing();
        else if( $numargs == 1 )
            $this->fromRawData( $args[0] );
        else if( $numargs == 4 )
            $this->fromAllInfo( $args[0], $args[1], $args[2], $args[3] );
        
    }

    /*
        Constructor for no argument instance
    */
    private function fromNothing() {
        $this->message = $DEFAULT_MSG;
        $this->timestamp = $DEFAULT_TIMESTAMP;
        $this->piority = 0;
        $this->target = 0;
        $this->encoded = 0;
    }

    /*
        Constructor for raw data argument instance
        $rawData -> raw data from server queue
    */
    private function fromRawData( $rawData ) {
        $pieces = explode( $this->FORMAT_DELIMITER, $rawData ); // parse raw data
        if( count($pieces) == 5 ) {
            // get message part
            $tmp = explode( "=", $pieces[0] );
            if( strpos( $tmp[0], 'MESSAGE' ) !== false && count($tmp) == 2 )
                $this->message = $tmp[1];
            else 
                $this->message = $ERROR_MSG;

            // get timestamp part
            $tmp = explode( "=", $pieces[1] );
            if( strpos( $tmp[0], 'TIMESTAMP' ) != false && count($tmp) == 2 )
                $this->timestamp = $tmp[1];
            else
                $this->timestamp = $DEFAULT_TIMESTAMP;

            // get priority part
            $tmp = explode( "=", $pieces[2] );
            if( strpos( $tmp[0], 'PRIORITY' ) != false && count($tmp) == 2 )
                $this->priority = $tmp[1];
            else
                $this->priority = 0;

            // get target part
            $tmp = explode( "=", $pieces[3] );
            if( strpos( $tmp[0], 'TARGET' ) != false && count($tmp) == 2 )
                $this->target = $tmp[1];
            else
                $this->target = 0;

            // get encoded part
            $tmp = explode( "=", $pieces[4] );
            if( strpos( $tmp[0], 'ENCODED' ) != false && count($tmp) == 2 )
                $this->encoded = $tmp[1];
            else
                $this->encoded = 0;

        } else {
            $this->message = $ERROR_MSG;
            $this->timestamp = $DEFAULT_TIMESTAMP;
            $this->piority = 0;
            $this->target = 0;
            $this->encoded = 0;
        }
    }

    /*
        Constructor for all argument instance
        $message -> message text
        $timestamp -> message time on sending timestamp
        $priority -> message priority level
        $target -> message target Process ID (PID)
    */
    private function fromAllInfo( $message, $timestamp, $priority, $target ) {
        $this->message = $message;
        $this->timestamp = $timestamp;
        $this->piority = $priority;
        $this->target = $target;
        $this->encoded = 0;
    }

    /*
        Returns the message text if the message is not encoded
        return -> the message text if encoded is false, 'encoded' otherwise
    */
    function getMessage() { 
        if($this->encoded == 0) return $this->message;
        else return 'encoded'; 
    }

    /*
        Returns timestamp text
        return -> timestamp text
    */
    function getTimestamp() { return $this->timestamp; }

    /*
        Returns priority level
        return -> priority level
    */
    function getPriority() { return $this->priority; }

    /*
        Returns target Process ID (PID)
        return -> target Process ID (PID)
    */
    function getTarget() { return $this->target; }

    /*
        Returns value of encoded flag
        return -> 1 if encoded, 0 otherwise
    */
    function isEncoded() { return $this->encoded; }

    /*
        Gets text form of data stored in IgluMessage object for sending to the server
        return -> the text form of the IgluMessage object
    */
    function getTxData() {
        $TxData = "MESSAGE=" . $this->message;
        $TxData .= $this->FORMAT_DELIMITER . "TIMESTAMP=" . $this->timestamp;
        $TxData .= $this->FORMAT_DELIMITER . "PRIORITY=" . $this->priority;
        $TxData .= $this->FORMAT_DELIMITER . "TARGET=" . $this->target;
        $TxData .= $this->FORMAT_DELIMITER . "ENCODED=" . $this->encoded;
        return $TxData;
    }

    /*
        Encrypts the message with a specific encoding and key
        $encoding -> the encoding to use
        $key -> the key to encrypt with
    */
    function encode( $encoding, $key ) { /* encode message */ }

    /*
        Decrypts the message with a specific encoding and key
        $encoding -> the encoding to use
        $key -> the key to encrypt with
    */
    function decode( $encoding, $key ) { /* decode message */ }
}
?>