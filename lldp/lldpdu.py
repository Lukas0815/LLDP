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
        # LLDPDU must fit into an ethernet frame
        if len(bytes(self)) + len(bytes(tlv)) > 1500:
            raise ValueError

        # Check if already EoLLDPDU regardless of Type of tlv => Not working at all, due to out of range error => len() does not do what expected
        if tlv.type == TLV.Type.END_OF_LLDPDU:
            if self.__len__() < 3:
                # print("end but not long enough lldp")
                raise ValueError
            if self.__tlvs[len(self.__tlvs)-1].type == TLV.Type.END_OF_LLDPDU:
                # print("eolldpdu is not end")
                raise ValueError 
        
        # Checks for ChassisID
        if tlv.type == TLV.Type.CHASSIS_ID:
            # Trying to add ChassisID but not first item to be added? WAIT, thats illegal
            if self.__len__() != 0:
                # print("wrong location of chassis")
                raise ValueError
        
        # Checks for PortID
        if tlv.type == TLV.Type.PORT_ID:
            # PortID must be second item in LLDPDU
            if self.__len__() != 1:
                # print("wrong location of portid")
                raise ValueError
        
        # Checks for TTL
        if tlv.type == TLV.Type.TTL:
            # TTL must be third item in LLDPDU
            if self.__len__() != 2:
                # print("wrong location of ttl")
                raise ValueError
        
        if not (tlv.type in [TLV.Type.END_OF_LLDPDU, TLV.Type.CHASSIS_ID, TLV.Type.PORT_ID, TLV.Type.TTL]):
            # other tlvs must be after chassis, port and ttl
            if self.__len__() < 3:
                raise ValueError

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
        if self.__getitem__(0).type != TLV.Type.CHASSIS_ID:
            return False

        # # Check PortID position
        if self.__getitem__(1).type != TLV.Type.PORT_ID:
            return False

        # # Check TTL position
        if self.__getitem__(2).type != TLV.Type.TTL:
            return False

        # # Check last TLV to be the EoLLDPDU
        if self.__getitem__(self.__len__()-1).type != TLV.Type.END_OF_LLDPDU:
            return False

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
        notEnd = True
        work_data = bytearray(data)
        currentID = 0
        tlvs = []
        while notEnd:
            type = work_data[currentID] >> 1
            if not (type in [0,1,2,3,4,5,6,7,8,127]):
                print("type: ", type)
                raise ValueError
            if type == TLV.Type.END_OF_LLDPDU:
                notEnd = False    

            length = work_data[currentID+1]
            tlvs.append(TLV.from_bytes(work_data[currentID:currentID+length+2]))
            currentID += length+2

        return LLDPDU(*tlvs)

