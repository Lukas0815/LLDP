from lldp.tlv import TLV


class LLDPDU:
    """LLDP Data Unit

    The LLDP Data Unit contains an ordered sequence of TLVs, three mandatory TLVs followed by zero or more optional TLVs
    plus an End Of LLDPDU TLV.

    Optional TLVs may be inserted in any order.

    An LLDPDU has to fit inside one Ethernet frame and cannot be split.

    LLDPDU Format:

        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+-+-+-+-+
        |                 |                 |                 |                                 |
        | Chassis ID TLV  |   Port ID TLV   |     TTL TLV     |         (Optional TLVs)         |
        |                 |                 |                 |                                 |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+-+-+-+-+
    """
    def __init__(self, *tlvs):
        self.__tlvs = []
        """List of included TLVs"""

        if len(tlvs) > 0:
            for tlv in tlvs:
                self.append(tlv)

    def __len__(self) -> int:
        """Get the number of TLVs in the LLDPDU"""
        return len(self.__tlvs)

    def __bytes__(self) -> bytes:
        """Get the byte representation of the LLDPDU"""
        res = b""
        for tlv in self.__tlvs:
            res += bytes(tlv)
        return res

    def __getitem__(self, item: int) -> TLV:
        """Get the TLV at position `item`"""
        return self.__tlvs[item]

    def __repr__(self):
        """Return a representation of the LLDPDU"""
        return "{}({})".format(self.__class__.__name__, repr(self.__tlvs))

    def __str__(self):
        """Return a printable representation of the LLDPDU"""
        return repr(self)

    def append(self, tlv: TLV):
        """Append `tlv` to the LLDPDU

        This method adds the given tlv to the LLDPDU.

        If adding the TLV makes the LLDPDU invalid (e.g. by adding a TLV after an EndOfLLDPDU TLV) it should raise a
        `ValueError`. Conditions for specific TLVs are detailed in each TLV's class description.
        """

        # TODO: Implement error checks

        # Check if already EoLLDPDU regardless of Type of tlv => Not working at all, due to out of range error => len() does not do what expected
        # if self.__getitem__(self.__len__()-1).get_type() == TLV.Type.END_OF_LLDPDU:
        #    raise ValueError
        
        # Checks for ChassisID
        # if tlv.get_type() == TLV.Type.CHASSIS_ID:
        #     # Trying to add ChassisID but not first item to be added? WAIT, thats illegal
        #     if self.__len__() != 0:
        #         raise ValueError
        #
        # # Checks for PortID
        # if tlv.get_type() == TLV.Type.PORT_ID:
        #     # PortID must be second item in LLDPDU
        #     if self.__len__() != 1:
        #         raise ValueError
        #
        # # Checks for TTL
        # if tlv.get_type() == TLV.Type.TTL:
        #     # TTL must be third item in LLDPDU
        #     if self.__len__() != 2:
        #         raise ValueError

        self.__tlvs.append(tlv)

    def complete(self):
        """Check if LLDPDU is complete.

        An LLDPDU is complete when it includes at least the mandatory TLVs (Chassis ID, Port ID, TTL).
        """
        # # TODO: Implement

        # Check length (quicker than checking if every mandatory TLV is there)
        if self.__len__() < 4:
            return False

        #Check for ChassisID
        # if self.__getitem__(0).get_type() != TLV.Type.CHASSIS_ID:
        #     return False

        # # Check PortID position
        # if self.__getitem__(1).get_type() != TLV.Type.PORT_ID:
        #     return False

        # # Check TTL position
        # if self.__getitem__(2).get_type() != TLV.Type.TTL:
        #     return False

        # # Check last TLV to be the EoLLDPDU
        # if self.__getitem__(self.__len__()) != TLV.Type.END_OF_LLDPDU:
        #     return False

        return True
        # DONE    


    @staticmethod
    def from_bytes(data: bytes):
        """Create an LLDPDU instance from raw bytes.

        Args:
            data (bytes or bytearray): The packed LLDPDU

        Raises a value error if the provided TLV is of unknown type. Apart from that validity checks are left to the
        subclass.
        """
        # TODO: Implement
        return NotImplemented
