from lldp.tlv import TLV


class PortDescriptionTLV(TLV):
    """Port Description TLV

    The Port Description TLV allows network management to advertise the device's port description.

    It is an optional TLV and as such may be included in an LLDPDU zero or more times between
    the TTL TLV and the End of LLDPDU TLV.

    Attributes:
        type (TLV.Type): The type of the TLV
        description (str): The port description

    TLV Format:

         0                   1                   2
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+
        |             |                 |                           |
        |      4      |      Length     |     Port Description      |
        |             |                 |                           |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+

                                                0 - 255 byte
    """

    def __init__(self, description: str):
        
        self.type = TLV.Type.PORT_DESCRIPTION
        self.value = description
        # DONE

    def __bytes__(self):
        """Return the byte representation of the TLV.

        This method must return bytes. Returning a bytearray will raise a TypeError.
        See `TLV.__bytes__()` for more information.
        """
        
        firstByteInt = (4 << 1) + (self.__len__()  >> 7)
        secondByteInt = self.__len__()
        byteval = bytes([firstByteInt]) + bytes([secondByteInt])
        # add value
        byteval += self.value.encode()

        return byteval
        # DONE

    def __len__(self):
        """Return the length of the TLV value.

        This method must return an int. Returning anything else will raise a TypeError.
        See `TLV.__len__()` for more information.
        """
        
        # Note: Maybe use __sizeof__ ?
        return len(self.value.encode())
        # DONE

    def __repr__(self):
        """Return a printable representation of the TLV object.

        See `TLV.__repr__()` for more information.
        """
        
        return "StringTLV(" + repr(self.value) + ")"
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
        if type != 4:
            raise ValueError
        
        # get value
        value = work_data[2:].decode()

        return PortDescriptionTLV(value)


class SystemDescriptionTLV(TLV):
    """System Description TLV

    The System Description TLV allows network management to advertise the system’s description.

    It is an optional TLV and as such may be included in an LLDPDU zero or more times between
    the TTL TLV and the End of LLDPDU TLV.

    Attributes:
        type (TLV.Type): The type of the TLV
        description (str): The system description

    TLV Format:

         0                   1                   2
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+
        |             |                 |                           |
        |      6      |      Length     |     System Description    |
        |             |                 |                           |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+

                                                0 - 255 byte
    """

    def __init__(self, description: str):
        
        self.type = TLV.Type.SYSTEM_DESCRIPTION
        self.value = description

    def __bytes__(self):
        """Return the byte representation of the TLV.

        This method must return bytes. Returning a bytearray will raise a TypeError.
        See `TLV.__bytes__()` for more information.
        """
        
        firstByteInt = (6 << 1) + (self.__len__()  >> 7)
        secondByteInt = self.__len__()
        byteval = bytes([firstByteInt]) + bytes([secondByteInt])
        # add decsription
        byteval += self.value.encode()

        return byteval

    def __len__(self):
        """Return the length of the TLV value.

        This method must return an int. Returning anything else will raise a TypeError.
        See `TLV.__len__()` for more information.
        """
        
        return len(self.value.encode())

    def __repr__(self):
        """Return a printable representation of the TLV object.

        See `TLV.__repr__()` for more information.
        """
        
        return "SystemDescriptionTLV(" + repr(self.value) + ")"

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
        if type != 6:
            raise ValueError
        
        # get value
        value = work_data[2:].decode()

        return SystemDescriptionTLV(value)


class SystemNameTLV(TLV):
    """System Name TLV

    The System Name TLV allows network management to advertise the system’s assigned name.

    It is an optional TLV and as such may be included in an LLDPDU zero or more times between
    the TTL TLV and the End of LLDPDU TLV.

    Attributes:
        type (TLV.Type): The type of the TLV
        name (str): The system name

    TLV Format:

         0                   1                   2
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+
        |             |                 |                           |
        |      5      |      Length     |     System Description    |
        |             |                 |                           |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+

                                                        0 - 255 byte
    """

    def __init__(self, name: str):
       
        self.type = TLV.Type.SYSTEM_NAME
        self.value = name

    def __bytes__(self):
        """Return the byte representation of the TLV.

        This method must return bytes. Returning a bytearray will raise a TypeError.
        See `TLV.__bytes__()` for more information.
        """
        
        firstByteInt = (5 << 1) 
        secondByteInt = self.__len__()
        byteval = bytes([firstByteInt]) + bytes([secondByteInt])
        # add value
        byteval += self.value.encode()

        return byteval

    def __len__(self):
        """Return the length of the TLV value.

        This method must return an int. Returning anything else will raise a TypeError.
        See `TLV.__len__()` for more information.
        """
        
        return len(self.value.encode())

    def __repr__(self):
        """Return a printable representation of the TLV object.

        See `TLV.__repr__()` for more information.
        """
        
        return "SystemNameTLV("+  repr(self.value) + ")"

    @staticmethod
    def from_bytes(data: TLV.ByteType):
        """Create a TLV instance from raw bytes.

        Args:
            data (bytes or bytearray): The packed TLV

        Raises a `ValueError` if the provided TLV contains errors (e.g. has the wrong type).
        """
        
        work_data = bytearray(data)

        # test type
        type = work_data[0] >> 1
        if type != 5:
            raise ValueError
        
        # get value
        value = work_data[2:].decode()

        return SystemNameTLV(value)
