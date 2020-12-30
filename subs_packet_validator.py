import subs_packet_abstract_validator
from subs_packet import SubsPacket, Type, Status

ANSWER_CODES = (Status.ANSWER_CORRECT, Status.ANSWER_VICTORY,
                Status.ANSWER_INCORRECT, Status.ANSWER_FULL_SUB)

ERROR_CODES = (Status.ERROR_CLOSED, Status.ERROR_UNEXPECTED,
               Status.ERROR_ATTEMPT_NOT_IN_TURN, Status.ERROR_OUT_OF_RANGE)


def is_ready_packet_valid(packet: SubsPacket):
    return True


def is_attempt_packet_valid(packet: SubsPacket):
    return packet.x_coord is not None and packet.y_coord is not None


def is_answer_packet_valid(packet: SubsPacket):
    return \
        packet.x_coord is not None and \
        packet.y_coord is not None and \
        packet.status in ANSWER_CODES


def is_error_packet_valid(packet: SubsPacket):
    return packet.status in ERROR_CODES


PACKET_TYPE_TO_VALIDATOR = {
    Type.READY: is_ready_packet_valid,
    Type.ERROR: is_error_packet_valid,
    Type.ATTEMPT: is_attempt_packet_valid,
    Type.ANSWER: is_answer_packet_valid
}


class SubsPacketValidator(subs_packet_abstract_validator.SubsPacketAbstractValidator):
    """
    Validates Subs Protocol packets by checking their fields
    based on their specified version and type.
    """

    def __init__(self, protocol_version: str):
        self.protocol_version = protocol_version

    def is_packet_valid(self, packet: SubsPacket):
        if packet.version != self.protocol_version:
            return False

        packet_type_validator = PACKET_TYPE_TO_VALIDATOR.get(packet.packet_type)
        if packet_type_validator is None:
            return False

        return packet_type_validator(packet)
