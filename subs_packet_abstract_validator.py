import abc

from subs_packet import SubsPacket


class SubsPacketAbstractValidator(metaclass=abc.ABCMeta):
    """
    Interface that may be implemented to validate a given packet.
    """
    @abc.abstractmethod
    def is_packet_valid(self, packet: SubsPacket):
        """
        Checks and returns whether the given packet is valid.
        :param SubsPacket packet: The Subs Protocol packet to check.
        :return: True if the packet is valid.
        """
        pass
