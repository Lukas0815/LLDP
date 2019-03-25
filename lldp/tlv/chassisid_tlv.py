from enum import IntEnum
from ipaddress import ip_address, IPv4Address, IPv6Address

from lldp.tlv import TLV


class ChassisIdTLV(TLV):
    """Chassis ID TLV

    The chassis ID TLV identifies the chassis (i.e. device) running the LLDP agent.

    The chassis ID TLV is mandatory and MUST be the first TLV in the LLDPDU.
    Each LLDPDU MUST contain one, and only one, Chassis ID TLV.


    Attributes:
        type (TLV.Type): The type of the TLV
        subtype (ChassisIdTLV.Subtype): The chassis ID subtype
        value (str, bytes or ip_address): The chassis ID.
            The type of this attribute depends on the subtype
                MAC Address -> bytes,
                Network Address -> ip_address,
                Otherwise -> str

    TLV Format:

         0                   1                   2
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+...+-+-+-+
        |             |                 |               |               |
        |      1      |      Length     |    Subtype    |   Chassis ID  |
        |             |                 |               |               |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+...+-+-+-+

                                                           1 - 255 byte

    Subtypes:

        A chassis may be identified in several ways, e.g. by its IP address, MAC address or a name specified by an
        administrator. The type of identification is determined by the subtype value.

        | Subtype | ID Basis          | Example                    |
        | ------- | ----------------- | -------------------------- |
        | 0       | Reserved          |                            |
        | 1       | Chassis Component | cl-SJ17-3-006:rack1:rtr-U3 |
        | 2       | Interface Alias   | office net                 |
        | 3       | Port Component    | backplane1                 |
        | 4       | MAC Address       | 02:04:df:88:a2:b4          |
        | 5       | Network Address*  | 134.96.86.110              |
        | 6       | Interface Name    | eth0                       |
        | 7       | Locally Assigned  | Frank's Computer           |
        | 8 - 255 | Reserved          |                            |

        Depending on the subtype the value is to be interpreted in a certain way.

        With the exception of subtypes 4 (MAC Address) and 5 (Network Address), as far as the LLDP agent is concerned,
        the value is a string. A distinction between these subtypes is only made by a human observer.

    MAC Address Subtype:

        MAC addresses are represented as raw bytes, e.g. the MAC address 02:04:df:88:a2:b4 corresponds to a value of
        b"\x02\x04\xDF\x88\xA2\xB4".

    Network Address Subtype:

        Network addresses are represented as raw bytes.

        In practice there are many different network protocols, each with their own address format with e.g. a different
        length.

        To determine the type of network protocol and the appropriate length of the network address transmitted in the
        Chassis ID TLV, network addresses are prefixed with an extra byte identifying the address family.

        For this implementation we only consider IPv4 and IPv6.

        | Protocol | Family Number |
        | -------- | ------------- |
        |   IPv4   |             1 |
        |   IPv6   |             2 |

        Examples (Address -> Bytes -> Prefixed Bytes):
            134.96.86.110  ->  b"\x86\x60\x56\x6E"  -> b"\x01\x86\x60\x56\x6E"

            20db::1        ->  b"\x20\xdb\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01"
                           ->  b"\x02\x20\xdb\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01"

        The full list of registered protocol families is available at:
            https://www.iana.org/assignments/address-family-numbers/address-family-numbers.xhtml
    """

    class Subtype(IntEnum):
        CHASSIS_COMPONENT = 1
        INTERFACE_ALIAS = 2
        PORT_COMPONENT = 3
        MAC_ADDRESS = 4
        NETWORK_ADDRESS = 5
        INTERFACE_NAME = 6
        LOCAL = 7

        def __repr__(self):
            return repr(self.value)


    def __init__(self, subtype: Subtype, id):
        """ Constructor

        Args:
            subtype (ChassisIdTLV.Subtype): The ID subtype
            id (str, bytes or ip_address): The type of this attribute depends on the subtype
                MAC Address     -> bytes
                Network Address -> ip_address
                Otherwise       -> str
        """
        # TODO: Implement
        # self.type = NotImplemented
        # self.subtype = NotImplemented
        # self.value = NotImplemented
        
        self.type = TLV.Type.CHASSIS_ID
        self.subtype = subtype
        self.value = id
        # DONE

    def __bytes__(self):
        """Return the byte representation of the TLV.

        This method must return bytes. Returning a bytearray will raise a TypeError.
        See `TLV.__bytes__()` for more information.
        """
        # TODO: Implement
        return NotImplemented

    def __len__(self):
        """Return the length of the TLV value.

        This method must return an int. Returning anything else will raise a TypeError.
        See `TLV.__len__()` for more information.
        """
        # TODO: Implement
        # Note: This does not include subtype length

        if (self.subtype == 4):
            # Case value is Mac: Since MAC-Address is given in raw bytes this should work
            return len(self.value)
        elif self.subtype == 5:
            # case value is Network Address: Since those are also given in raw bytes this should work 
            # regardless of the type => One might merch this with subtype == 4 or distinguish between Ipv4 and Ipv6 and give it statically
            return len(self.value)
        else:
            #Case value is a string
            return len(self.value.encode())     #Not sure if this always works... Internet says this does give size of string in bytes!
        return NotImplemented
        #DONE

    def __repr__(self):
        """Return a printable representation of the TLV object.

        See `TLV.__repr__()` for more information.
        """
        # TODO: Implement
        return "ChassisIdTLV(" + repr(self.subtype) + ", " + repr(self.value) + ")"
        # DONE

    @staticmethod
    def from_bytes(data: TLV.ByteType):
        """Create a TLV instance from raw bytes.

        Args:
            data (bytes or bytearray): The packed TLV

        Raises a `ValueError` if the provided TLV contains errors (e.g. has the wrong type).
        """
        # TODO: Implement
        return NotImplemented
