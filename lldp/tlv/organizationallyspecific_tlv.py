from lldp.tlv import TLV


class OrganizationallySpecificTLV(TLV):
    """Organizationally Specific TLV

    This TLV type is provided to allow organizations, software developers and equipment vendors to define TLVs
    to advertise information to remote devices which can not be included in other TLV types.

    It is an optional TLV and as such may be included in an LLDPDU zero or more times between the TTL TLV and the
    End of LLDPDU TLV.

    Attributes:
        type    (TLV.Type): The type of the TLV
        oui     (bytes or bytearray): Organizationally unique identifier
        subtype (bytes or bytearray): Organizationally defined subtype
        value   (bytes or bytearray): Organizationally defined information


    TLV Format:

         0               1               2               5               6
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+-+-|
        |             |                 |    Organiz.   |    Organiz.   |   Organizationally  |
        |     127     |      Length     |   Unique ID   |    Defined    | Defined Information |
        |             |                 |     (OUI)     |    Subtype    |       (Value)       |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+-+-|

                                                                             0 - 507 byte

    The OUI is a 24 bit number uniquely identifying a vendor, manufacturer or organization.

    The subtype should be a unique subtype value assigned by the defining organization.
    """

    def __init__(self, oui: TLV.ByteType, subtype: TLV.ByteType, value):
        """Constructor

        Parameters:
            oui (bytes or bytearray): The OUI. See above
            subtype (bytes or bytearray): The organizationally defined subtype
            value (any): The value
        """
        
        self.type = TLV.Type.ORGANIZATIONALLY_SPECIFIC
        self.oui = oui
        self.subtype = subtype
        if type(value) == str:
            self.value = value.encode()
        elif type(value) == int:
            self.value = bytes([value])
        else:
            self.value = value
        # DONE

    def __bytes__(self):
        """Return the byte representation of the TLV.

        This method must return bytes. Returning a bytearray will raise a TypeError.
        See `TLV.__bytes__()` for more information.
        """
        
        firstByteInt = (127 << 1) + (self.__len__()  >> 7)
        secondByteInt = self.__len__()
        byteval = bytes([firstByteInt]) + bytes([secondByteInt])
        # add oui
        byteval += self.oui
        # add subtype
        byteval += self.subtype
        # add value
        byteval += self.value

        return byteval
        # DONE

    def __len__(self):
        """Return the length of the TLV value.

        This method must return an int. Returning anything else will raise a TypeError.
        See `TLV.__len__()` for more information.
        """
        
        return len(self.value) +4
        # DONE


    def __repr__(self):
        """Return a printable representation of the TLV object.

        See `TLV.__repr__()` for more information.
        """
        
        return "OrganizationallySpecificTLV(" + repr(self.oui) + ", " + repr(self.subtype) + ", " + repr(self.value) + ")"
        # DONE

    @staticmethod
    def from_bytes(data: TLV.ByteType):
        """Create a TLV instance from raw bytes.

        Args:
            data (bytes or bytearray): The packed TLV

        Raises a `ValueError` if the provided TLV contains errors (e.g. has the wrong type).
        """
        
        work_data = bytearray(data)
        # check type
        type = work_data[0] >> 1
        if type != 127:
            raise ValueError
        
        # oui
        oui = work_data[2:5]
        # oui subtype
        subtype = work_data[5]
        #value
        value = work_data[6:]

        return OrganizationallySpecificTLV(oui, bytes([subtype]), value)
