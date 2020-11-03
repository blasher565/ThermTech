"""
Author: Brandon Lasher
Secondary: Christian Wagner (Last Update: 11/02/2020)

Parent class for all remote devices will define base functions
   and internal variables


"""


class device:
    def __init__(self, name, uniqueID, deviceType ):
        self.__name = name
        self.__uniqueID = uniqueID
        self.__deviceType = deviceType
        self.__zoneID = -1

    # Returns dict() with summary of the device information
    def about( self ):
        return {"name": self.__name,
                "uniqueID": self.__uniqueID,
                "deviceType": self.__deviceType,
                "zoneID:": self.__zoneID
                }

    # Return Device logical name
    @property
    def name( self ):
        return self.__name

    # Returns unqiue name for device ( MAC address )
    @property
    def uniqueID( self ):
        return self.__uniqueID

    # Returns zoneID for grouping
    @property
    def deviceType( self ):
        return self.__deviceType

    # Returns the zoneID
    @property
    def zoneID( self ):
        return self.__zoneID

    # Sets the new zoneID
    @zoneID.setter
    def zoneID( self, zoneID ):
        self.__zoneID = zoneID


if __name__ == "__main__":
    d = device( "testDev", 000000000, "damper")
    print( d.about() )
    d.zoneID = 10
    print(d.zoneID)
    # confirm setter worked
    print( d.about() )