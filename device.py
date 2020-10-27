"""
Author: Brandon Lasher

Parent class for all remote devices will define base functions
   and internal variables


"""


class device:
    def __init__(self, name, uniqueID, deviceType ):
        self._name = name
        self._uniqueID = uniqueID
        self._deviceType = deviceType
        self._zoneID = -1;

    #Returns dict() with summary of the device information
    def about( self ):
        return {"name": self._name, "uniqueID": self._uniqueID, "deviceType": self._deviceType, "zoneID:": self._zoneID };

    # Return Device logical name
    def getName( self ):
        return self._name

    # Returns unqiue name for device ( MAC address )
    def getUniqueID( self ):
        return self._uniqueID

    #Returns zoneID for grouping
    def getDeviceType( self ):
        return self._deviceType

    #Sets the new zoneID and returns its value
    def setZoneID( self, zoneID ):
        self._zoneID = zoneID
        return self._zoneID

    #Returns the zoneID 
    def getZoneID( self ):
        return self._zoneID



if __name__ == "__main__":
    d = device( "testDev", 000000000, "damper")
    print( d.about() )
    d.setZoneID( 10 )
    print(d.getZoneID())

