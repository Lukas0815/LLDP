from lldp.tlv import TLV


class TTLTLV(TLV):
    """Time To Live TLV

    The Time To Live TLV indicates the number of seconds that the recipient LLDP agent is to regard the information
    associated with the transmitting LLDP agent as valid.

    The Time To Live TLV is mandatory and MUST be the third TLV in the LLDPDU.
    Each LLDPDU MUST contain one, and only one, TTL TLV.

    Attributes:
        type (TLV.Type): The type of the TLV
        value (int): The TTL in seconds

    TLV Format:

         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |             |                 |                               |
        |      3      |      Length     |               TTL             |
        |             |                 |                               |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    """

    def __init__(self, ttl: int):
        # TODO: Implement
        self.type = TLV.Type.TTL
        self.value = ttl

        if ttl < 0 or ttl > 65535:
            raise ValueError

    def __bytes__(self):
        """Return the byte representation of the TLV.

        This method must return bytes. Returning a bytearray will raise a TypeError.
        See `TLV.__bytes__()` for more information.
        """
        # TODO: Implement
        firstByteInt = (3 << 1) + (self.__len__()  >> 7)
        secondByteInt = self.__len__()
        byteval = firstByteInt.to_bytes(1, byteorder='big') + secondByteInt.to_bytes(1, byteorder='big')
        #add value
        byteval += self.value.to_bytes(2, 'big')

        return byteval
        # DONE

    def __len__(self):
        """Return the length of the TLV value.

        This method must return an int. Returning anything else will raise a TypeError.
        See `TLV.__len__()` for more information.
        """
        # TODO: Implement
        return 2
        # DONE

    def __repr__(self):
        """Return a printable representation of the TLV object.

        See `TLV.__repr__()` for more information.
        """
        # TODO: Implement
        return "TtlTLV(" + repr(self.value) + ")"
        # DONE

    @staticmethod
    def from_bytes(data: TLV.ByteType):
        """Create a TLV instance from raw bytes.

        Args:
            data (bytes or bytearray): The packed TLV

        Raises a `ValueError` if the provided TLV contains errors (e.g. has the wrong type).
        """
        # TODO: Implement
        work_data = bytearray(data)
        
        # check the length
        if len(work_data) != 4:
            raise ValueError

        # check type
        type = work_data[0] >> 1
        if type != 3:
            raise ValueError

        #read length
        highestBit = work_data[0] & 1
        length = (highestBit << 9) + work_data[1]
        if length != 2: #appereandly always 2 bytes
            raise ValueError
       

        # get ttl
        ttl = int.from_bytes(work_data[2:], byteorder='big', signed=False)
        if ttl < 0 or ttl > 65535:
            raise ValueError

        return TTLTLV(ttl)
