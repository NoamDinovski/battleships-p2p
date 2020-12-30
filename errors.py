class PacketPackError(Exception):
    """
    Raised when a packing operation on a packet fails.
    """
    pass


class PacketUnpackError(Exception):
    """
    Raised when an unpacking operation on a packet fails.
    """
    pass


class InvalidPacketError(Exception):
    """
    Raised when a packet is found invalid.
    """
    pass
