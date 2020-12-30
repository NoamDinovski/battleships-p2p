import enum


class Type(enum.Enum):
    """
    Enumeration for a Subs Protocol packet's type.
    """
    READY = "READY"
    ATTEMPT = "ATTEMPT"
    ANSWER = "ANSWER"
    ERROR = "ERROR"


class Status(enum.Enum):
    """
    Enumeration for a Subs Protocol packet's status, for either ANSWER or ERROR packets.
    """
    ANSWER_CORRECT = "CORRECT"
    ANSWER_INCORRECT = "INCORRECT"
    ANSWER_FULL_SUB = "FULL-SUB"
    ANSWER_VICTORY = "VICTORY"
    ERROR_OUT_OF_RANGE = "OUT-OF-RANGE"
    ERROR_ATTEMPT_NOT_IN_TURN = "ATTEMPT-NOT-IN-TURN"
    ERROR_CLOSED = "CLOSED"
    ERROR_UNEXPECTED = "UNEXPECTED"


class SubsPacket:
    """
    Represents a packet belonging to the Subs Protocol.
    """

    @staticmethod
    def ready(version: str):
        """
        Factory method that creates a Subs Protocol READY packet.

        :param str version: The protocol's version.
        :return: A new Subs Protocol READY packet.
        """
        return SubsPacket(version, Type.READY)

    @staticmethod
    def attempt(version: str, x_coord: int, y_coord: int):
        """
        Factory method that creates a Subs Protocol ATTEMPT packet.

        :param str version: The protocol's version.
        :param int x_coord: The X coordinate of the point that's being inspected.
        :param int y_coord: The Y coordinate of the point that's being inspected.
        :return: A new Subs Protocol ATTEMPT packet.
        """
        return SubsPacket(version, Type.ATTEMPT, x_coord=x_coord, y_coord=y_coord)

    @staticmethod
    def answer(version: str, status: Status, x_coord: int, y_coord: int):
        """
        Factory method that creates a Subs Protocol ANSWER packet.

        :param str version: The protocol's version.
        :param AnswerStatus status: The type of answer.
        :param int x_coord: The X coordinate of the point that's been inspected.
        :param int y_coord: The Y coordinate of the point that's been inspected.
        :return: A new Subs Protocol ANSWER packet.
        """

        return SubsPacket(version, Type.ANSWER, status=status, x_coord=x_coord, y_coord=y_coord)

    @staticmethod
    def error(version: str, status: Status):
        """
        Factory method that creates a Subs Protocol ERROR packet.

        :param str version: The protocol's version.
        :param ErrorStatus status: The type of error.
        :return: A new Subs Protocol ERROR packet.
        """
        return SubsPacket(version, Type.ERROR, status=status)

    def __init__(self, version: str, packet_type: Type, status=None, x_coord=None, y_coord=None):
        """
        Initializes a new Subs Protocol packet.

        :param str version: The protocol's version.
        :param Type packet_type: The type of the packet.
        :param Status status: The answer or error status of the packet, for ANSWER and ERROR type packets.
        :param int x_coord: The X coordinate of the inspected point, for ATTEMPT and ANSWER type packets.
        :param int y_coord: The Y coordinate of the inspected point, for ATTEMPT and ANSWER type packets.
        """
        self.version = version
        self.packet_type = packet_type
        self.status = status
        self.x_coord = x_coord
        self.y_coord = y_coord
