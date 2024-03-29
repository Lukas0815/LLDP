from lldp.tlv import TLV
from ipaddress import ip_address, IPv4Address, IPv6Address
from enum import IntEnum


class ManagementAddressTLV(TLV):
    """Management Address TLV

    The Management Address TLV identifies an address associated with the local LLDP agent that may be used to reach
    higher layer entities to assist discovery by network management, e.g. a web interface for device configuration.

    It is an optional TLV and as such may be included in an LLDPDU zero or more times between
    the TTL TLV and the End of LLDPDU TLV.

    Attributes:
        type    (TLV.Type): The type of the TLV
        subtype (IFNumberingSubtype): The interface numbering subtype
        value   (ip_address): The management address
        oid     (bytes): The object identifier of the device sending the TLV

    TLV Format:

         0               1               2               3               4
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+~
        |             |                 |  Management   |  Management   |   Management    |
        |     0x10    |      Length     |    Address    |    Address    |     Address     |
        |             |                 | String Length |    Subtype    | (m=1-31 octets) |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-...-+-+-+-+~

         5+m             6+m              10+m           11+m
       ~+-+-+-+-+-+-+-+-+-+-+-+...+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+.....+-+-+-+-+-+-+-+
        |   Interface   |   Interface   |  OID String   |        Object identifier        |
        |   Numbering   |    Number     |    Length     |         (0-128 octets)          |
        |    Subtype    |   (4 octets)  |   (1 octet)   |                                 |
       ~+-+-+-+-+-+-+-+-+-+-+-+...+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+.....+-+-+-+-+-+-+-+

    Management Address Subtype and Management Address String Length:

        In practice there are many different network protocols, each with their own address format and length.

        To identify the type of network protocol and length of the network address the TLV includes a management address
        subtype and string length. Address lengths are given in bytes.

        For this implementation we only consider IPv4 and IPv6.

        | Protocol | Subtype |
        | -------- | ------- |
        |   IPv4   |       1 |
        |   IPv6   |       2 |

        Example:
            134.96.86.110 is an IPv4 address, so it has a subtype of 1 and it has a length of 4 bytes.

        The full list of registered protocol families is available at:
            https://www.iana.org/assignments/address-family-numbers/address-family-numbers.xhtml


    Interface Number and Subtype:

        The interface numbering subtype indicates the numbering method used to define the interface number.

        From the view of the LLDP agent the interface number is not treated differently depending on the numbering
        subtype. It is just a number.

        The LLDP standard specifies three valid subtypes:

        | Subtype |    Description     |
        | ------- | ------------------ |
        |       1 |      Unknown       |
        |       2 |  Interface Index   |
        |       3 | System Port Number |

    OID / OID Length:

        An OID (Object IDentifier) is a globally unabiguous name for any type of object / thing.
        It can be used to e.g. identify the kind of hardware component associated with the management address.

        This implementation will not make use of the OID, but it nevertheless has to be handled properly if included in
        a TLV. It does not have to be interpreted.

        Example:
            >>> tlv = ManagementAddressTLV(ip_address("192.0.2.1"), 4, ifsubtype=IFNumberingSubtype.IF_INDEX,
            >>>                            oid=b"\x00\x08\x15")
            >>> tlv.oid
            b'\x00\x08\x15'
    """

    class IFNumberingSubtype(IntEnum):
        UNKNOWN = 1
        IF_INDEX = 2
        SYSTEM_PORT = 3

        def __repr__(self):
            return repr(self.value)

    def __init__(self, address, interface_number: int = 0, ifsubtype: IFNumberingSubtype = IFNumberingSubtype.UNKNOWN, oid: TLV.ByteType = None):
        """ Constructor

        Args:
            address (ip_address): IP Address to be parsed
            interface_number (int): The interface number
            ifsubtype (IFNumberingSubtype): The interface numbering subtype
            oid (bytes): The OID. See above
        """
        
        self.type = TLV.Type.MANAGEMENT_ADDRESS
        self.subtype = ifsubtype
        if type(address) == str:
            address = ip_address(address)

        self.value = address
        if oid is None:
            self.oid = None
        else:
            self.oid = oid

        self.ifnmbr = interface_number
        # DONE

    def __bytes__(self):
        """Return the byte representation of the TLV.

        This method must return bytes. Returning a bytearray will raise a TypeError.
        See `TLV.__bytes__()` for more information.
        """
        
        """ Achtung, könnte alles jeweils 1 byte groß sein
            Dementsprechend ist das bitshiften nicht notwendig
        """

       
        # get type and length right (first 2 bytes)
        firstByteInt = (8 << 1)
        secondByteInt = self.__len__()
        byteval = bytes([firstByteInt]) + bytes([secondByteInt])
        #add Management Address string length (of byterep?)
        byteval += bytes([len(self.value.packed)+1])
        # add Management Address Subtype
        if self.value.version == 4:
            byteval += bytes([1])
        else:
            byteval += bytes([2])
        # add Management address
        byteval += self.value.packed
        # add Interface Numbering subtype
        byteval += bytes([self.subtype])   
        # add Interface Number
        byteval += self.ifnmbr.to_bytes(4, byteorder='big', signed=False)
        # oid length
        byteval += bytes([0]) if self.oid is None else bytes([len(self.oid)])
        # add oid
        if not (self.oid is None):
            byteval += self.oid

        return byteval
        # DONE

    def __len__(self):
        """Return the length of the TLV value.

        This method must return an int. Returning anything else will raise a TypeError.
        See `TLV.__len__()` for more information.
        """
        
        if self.oid is None:
            oidlength = 0
        else: 
            oidlength = len(self.oid)
        # Note: Only includes length of Address?!  
        if self.value.version == 4:
            return 12 + oidlength
        
        # Case IPv6
        return 24  + oidlength  # +4 for address?
        # DONE

    def __repr__(self):
        """Return a printable representation of the TLV object.

        See `TLV.__repr__()` for more information.
        """
        
        return "ManagementAddressTLV(" + repr(self.subtype) + ", " + repr(self.value) + ", " + repr(self.oid) + ")"

    @staticmethod
    def from_bytes(data: TLV.ByteType):
        """Create a TLV instance from raw bytes.

        Args:
            data (bytes or bytearray): The packed TLV

        Raises a `ValueError` if the provided TLV contains errors (e.g. has the wrong type).
        """
        
        work_data = bytearray(data)
        
        # check type
        type = work_data[0]
        
        
        # Management Address String length
        ma_strlength = work_data[2] -2

        # Management Address Subtype
        ma_subtype = work_data[3]

        # Management Address
        ma_address = ip_address(addr2Str(ma_subtype, work_data[4:5+ma_strlength]))

        # Interface Numbering Subtype
        insubtype = work_data[5+ma_strlength]

        # Interface Number
        ifacenmbr = work_data[6+ma_strlength:10+ma_strlength]

        #OID String length
        
        oid_strlength = work_data[10+ma_strlength]

        if oid_strlength != 0:
            # OID
            oid = work_data[11+ma_strlength:]
        else:
            oid = None


        return ManagementAddressTLV(ma_address, ifacenmbr, insubtype, oid)

def addr2Str(iptype, data):
    addrstr = ''
    work_data = bytearray(data)
    if iptype == 1:
        for b in work_data:
            addrstr += str(b) + '.'
    else:
        counter = 0
        genau = bytearray()
        for b in work_data:
            counter += 1
            genau.append(b)
            if counter == 2:
                addrstr += str(hex(int.from_bytes(genau, byteorder='big', signed=False)))[2:] + ':'
                genau = bytearray()
                counter = 0

    return addrstr[:-1]