import socket

import errors
from subs_packet import SubsPacket
from subs_packet_abstract_validator import SubsPacketAbstractValidator
from subs_protocol_abstract_packer import SubsProtocolAbstractPacker


class SubsProtocolStream:
    """
    Class used to send and receive Subs Protocol packets.
    """
    BUFFER_SIZE = 1024

    def __init__(self, stream_socket: socket.socket,
                 packer: SubsProtocolAbstractPacker,
                 validator: SubsPacketAbstractValidator):
        self.stream_socket = stream_socket
        self.packer = packer
        self.validator = validator

    def send(self, packet: SubsPacket):
        """
        Sends a Subs Protocol packet through the stream.
        :param SubsPacket packet: The packet to send.

        :raises InvalidPacketError: if the sent packet is found invalid for any reason.
        :raises PacketPackError: if failed to pack the given packet into raw data.
        :raises socket.error: if a socket or connection error has occurred.
        """

        if not self.validator.is_packet_valid(packet):
            raise errors.InvalidPacketError()

        try:
            self.stream_socket.send(self.packer.pack(packet))
        except (errors.PacketPackError, socket.error):
            raise

    def receive(self) -> SubsPacket:
        """
        Receives a Subs Protocol packet from the stream and returns it.

        :raises InvalidPacketError: if the received packet is invalid for any reason.
        :raises PacketUnpackError: if failed to unpack the received data into a Subs Protocol packet.
        :raises socket.error: if a socket or connection error has occurred.
        """
        try:
            packet = self.packer.unpack(self.stream_socket.recv(self.BUFFER_SIZE))

            if not self.validator.is_packet_valid(packet):
                raise errors.InvalidPacketError()

            return packet
        except (errors.PacketUnpackError, socket.error):
            raise
