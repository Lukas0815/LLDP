import socket, select
import time
from .lldpdu import LLDPDU
from .tlv import *


class StdoutLogger:
    def __init__(self):
        pass

    def log(self, msg):
        print(msg)


class LLDPAgent:
    """LLDP Agent

    The LLDP agent is the top-level component. It provides two functions.

    It announces its presence on the network by sending LLDP frames in regular intervals.
    At the same time it listens for LLDP frames from other network devices.

    If a frame is received and it is valid its contents will be logged for the administrator.
    """
    def __init__(self, mac_address: bytes, interface_name: str = "", interval=1.0, sock=None, logger=None):
        """LLDP Agent Constructor

        Sets up the network socket and LLDP agent state.

        Parameters:
            mac_address (bytes): The local MAC address
            interface_name (str): Name of the local interface
            interval (float): Announce interval in seconds
            sock: A previously opened socket. Used for testing
            logger: A logger instance. Used for testing
            
        """
        if sock is None:
            # Open a socket suitable for transmitting LLDP frames.
            self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, 768) # DONE
        else:
            self.socket = sock

        self.interface_name = interface_name
        self.mac_address = mac_address
        self.announce_interval = interval  # in seconds
        self.logger = StdoutLogger() if logger is None else logger

    def run(self, run_once: bool=False):
        """Agent Loop

        This is the main loop of the LLDP agent. It takes care of sending as well as receiving LLDP frames.

        The loop continuously checks the socket for new data. If data (in the form of an Ethernet frame)
        has been received, it will check if the frame is a valid LLDP frame and, if so, log its contents for the
        administrator. All other frames will be ignored.

        Valid LLDP frames have an ethertype of 0x88CC, are directed to one of the LLDP multicast addresses
        (01:80:c2:00:00:00, 01:80:c2:00:00:03 and 01:80:c2:00:00:0e) and have not been sent by the local agent.

        After processing received frames, the agent announces itself by calling `LLDPAgent.announce()` if a sufficient
        amount of time has passed.

        Parameters:
            run_once (bool): Stop the main loop after the first pass
        """
        received = False
        t_previous = time.time()
        try:
            while not run_once or not received:
                r, _, _ = select.select([self.socket], [], [], self.announce_interval)
                if len(r) > 0:
                    # Frames have been received by the network card

                    # Get the next frame
                    data = r[0].recv(4096)
                    # Check format and extract LLDPDU (raw bytes)
                    
                    work_data = bytearray(data)
                    etherType = work_data[12:14]
                    if etherType != b'\x88\xcc':
                        #print("WRONG ETHER-TYPE")
                        continue
                    destination = work_data[:6]
                    source = work_data[6:12]
                    # NOTE: this raises ValueError when executing main.py
                    if not (destination in [b'\x01\x80\xc2\x00\x00\x0e', b'\x01\x80\xc2\x00\x00\x00', b'\x01\x80\xc2\x00\x00\x03']):
                        print("not correct source")
                        continue
                    raw_lldpdu = work_data[14:]

                    # Instantiate LLDPDU object from raw bytes
                    
                    lldpdu = LLDPDU.from_bytes(raw_lldpdu)
                    # if not lldpdu.complete():
                    #     raise ValueError
                    # Log contents
                    self.logger.log(str(lldpdu))
                    received = True

                # Announce if the time is right
                t_now = time.time()
                if t_now - t_previous > self.announce_interval:
                    self.announce()
                    print("genau")
                    t_previous = t_now

        except KeyboardInterrupt:
            pass
        finally:
            # Clean up
            self.socket.close()

    def announce(self):
        """Announce the agent

        Send an LLDP frame using the socket.

        Sends an LLDP frame with an LLDPDU containing:
            * the agent's MAC address as its chassis id
            * the agent's interface name as port id
            * a TTL of 60 seconds
        """

        # Construct LLDPDU
    
        tlvs = []
        tlvs.append(ChassisIdTLV(ChassisIdTLV.Subtype.MAC_ADDRESS, self.mac_address))
        tlvs.append(PortIdTLV(PortIdTLV.Subtype.INTERFACE_NAME, self.interface_name))
        tlvs.append(TTLTLV(60))
        #tlvs.append(EndOfLLDPDUTLV())
        lldpdu = LLDPDU(*tlvs)

        # Construct Ethernet Frame
        
        frame =  b'\x01\x80\xc2\x00\x00\x0e' 
        frame += self.mac_address
        frame += b'\x88\xcc'
        frame += bytes(lldpdu)
        # Send frame
        self.socket.send(frame)
