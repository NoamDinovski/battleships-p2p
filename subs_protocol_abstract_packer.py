import abc

from subs_packet import SubsPacket


class SubsProtocolAbstractPacker(metaclass=abc.ABCMeta):
    """
    Interface that can be implemented to provide custom packing and unpacking methods
    for a Subs Protocol packet.
    """
    @abc.abstractmethod
    def pack(self, packet: SubsPacket) -> bytes:
        """
        Packs the given packet into raw data and returns the data.
        :param SubsPacket packet: The packet to pack.
        :return: Raw packet data in bytes.
        """
        pass

    @abc.abstractmethod
    def unpack(self, data: bytes) -> SubsPacket:
        """
        Unpacks the given raw data into a packet and returns the packet.
        :param bytes data: The raw byte data.
        :return: Packet instance created from the raw data.
        """
        pass
