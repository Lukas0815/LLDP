from enum import IntEnum

from lldp.tlv import TLV


class SystemCapabilitiesTLV(TLV):
    """System Capabilities TLV

    The System Capabilities TLV is an optional TLV that identifies the primary function(s) of the system and whether or
    not these primary functions are enabled.

    It is an optional TLV and as such may be included in an LLDPDU zero or more times between
    the TTL TLV and the End of LLDPDU TLV.

    Attributes:
        type (TLV.Type): The type of the TLV
        value (int): Supported and enabled capabilities


    TLV Format:

         0                   1                   2                   3                   4
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |             |                 |            System             |            Enabled            |
        |      7      |      Length     |         Capabilities          |         Capabilities          |
        |             |                 |                               |                               |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                                        |                                                               |
                                        |             2 byte                           2 byte           |
                                        |                                                               |
                                        |                                                               |
                                        |<--------------------------  Value  -------------------------->|

    Capabilities:

        Capabilities are encoded in a bitmap. A binary one in a bit position indicates that the function associated with
        the bit is supported / enabled.

        | ----- | ------------------- | ------------------------------------------------------------ |
        |  Bit  |     Capability      |                           Description                        |
        | ----- | ------------------- | ------------------------------------------------------------ |
        |   0   |        Other        |                                                              |
        |   1   |      Repeater       |                                                              |
        |   2   |       Bridge        | e.g. an Ethernet switch                                      |
        |   3   |  WLAN Access Point  |                                                              |
        |   4   |       Router        |                                                              |
        |   5   |     Telephone       | i.e. a VoIP phone                                            |
        |   6   | DOCSIS cable device | i.e. a cable modem                                           |
        |   7   |    Station Only     | e.g. a PC, should not be set in conjunction with other bits  |
        | 8–15  |      reserved       |                                                              |
        | ----- | ------------------- | ------------------------------------------------------------ |

        If the system capabilities field does not indicate the existence of a capability that the enabled capabilities
        field indicates is enabled, the TLV will be interpreted as containing an error and a ValueError is raised.
    """

    class Capability(IntEnum):
        """Capability bit values

        This enum can be used to construct a capability bitmap in a descriptive way.

        To create a capability bitmap the enum values can be ORed with each other, e.g. for a WLAN router the
        capabilities might look like this:

            caps = Capability.WLAN_AP | Capability.ROUTER
        """
        OTHER = 1
        REPEATER = 2
        BRIDGE = 4
        WLAN_AP = 8
        ROUTER = 16
        TELEPHONE = 32
        DOCSIS_DEVICE = 64
        STATION_ONLY = 128
        C_VLAN_COMPONENT = 256
        S_VLAN_COMPONENT = 512
        TWO_PORT_MAC_RELAY = 1024

        def __repr__(self):
            return repr(self.value)

    def __init__(self, supported: int = 128, enabled: int = 128):
        """Constructor

        Parameters:
            supported (int): Bitmap of supported capabilities
            enabled (int): Bitmap of enabled capabilities
        """
        
        self.type = TLV.Type.SYSTEM_CAPABILITIES
        self.value = (supported << 16) + enabled
        self.supported_int = supported
        self.enabled_int = enabled
        if not self.supports(enabled):
            raise ValueError


    def __bytes__(self):
        """Return the byte representation of the TLV.

        This method must return bytes. Returning a bytearray will raise a TypeError.
        See `TLV.__bytes__()` for more information.
        """
        
        firstByteInt = (7 << 1)
        secondByteInt = self.__len__()
        byteval = firstByteInt.to_bytes(1, byteorder='big', signed=False) + secondByteInt.to_bytes(1, byteorder='big', signed=False)
        # add value
        byteval += self.value.to_bytes(4, byteorder='big', signed=False)

        return byteval


    def __len__(self):
        """Return the length of the TLV value.

        This method must return an int. Returning anything else will raise a TypeError.
        See `TLV.__len__()` for more information.
        """
        
        return 4
        # DONE

    def __repr__(self):
        """Return a printable representation of the TLV object.

        See `TLV.__repr__()` for more information.
        """
        
        return "SystemCapabilitiesTLV(" + repr(self.value) + ")"
        # DONE

    @staticmethod
    def from_bytes(data: TLV.ByteType):
        """Create a TLV instance from raw bytes.

        Args:
            data (bytes or bytearray): The packed TLV

        Raises a `ValueError` if the provided TLV contains errors (e.g. has the wrong type).
        """
        
        work_data = bytearray(data)

        # test overal length
        if len(work_data) != 6:
            raise ValueError
        

        # test type
        type = work_data[0] >> 1
        if type != 7:
            raise ValueError
        
        # read values
        supported = int.from_bytes(work_data[2:4], byteorder='big', signed=False)
        enabled = int.from_bytes(work_data[4:6], byteorder='big', signed=False)

        if (supported | enabled) != supported:
            raise ValueError
        if (supported & enabled) != enabled:
            raise ValueError

        return SystemCapabilitiesTLV(supported, enabled)

    def supports(self, capabilities: int):
        """Check if the system supports a given set of capabilities.

        Multiple capabilities should be ORed together.
        """
        
        return True if (capabilities == (capabilities & self.supported_int)) else False
    

    def enabled(self, capabilities: int):
        """Check if the system has a given capability enabled.

        Multiple capabilities should be ORed together.
        """
        
        combined = capabilities & self.enabled_int
        if (capabilities == combined):
            return True
        else:
            return False
