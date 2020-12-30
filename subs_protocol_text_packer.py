from subs_packet import SubsPacket, Type, Status
from subs_protocol_abstract_packer import SubsProtocolAbstractPacker
import errors


class SubsProtocolTextPacker(SubsProtocolAbstractPacker):
    """
    Packs and unpacks Subs Protocol packets into and from a textual format.
    """
    FIELD_VALUE_SEPARATOR = ": "

    VERSION_FIELD_NAME = "VERSION"
    TYPE_FIELD_NAME = "TYPE"
    STATUS_FIELD_NAME = "STATUS"
    X_COORD_FIELD_NAME = "X-COOR"
    Y_COORD_FIELD_NAME = "Y-COOR"

    NEWLINE = "\n"

    def get_field_string(self, name: str, value_string: str) -> str:
        """
        Returns a string representing a given field in the packet.

        :param str name: The field's name.
        :param str value_string: The field's value as a string.
        """
        return name + self.FIELD_VALUE_SEPARATOR + value_string

    def pack(self, subs_packet: SubsPacket) -> bytes:

        # Required Fields
        packed_fields = [
            self.get_field_string(self.VERSION_FIELD_NAME, subs_packet.version),
            self.get_field_string(self.TYPE_FIELD_NAME, subs_packet.packet_type.value)
        ]

        # Optional Fields - Only append if defined
        if subs_packet.status is not None:
            packed_fields.append(
                self.get_field_string(self.STATUS_FIELD_NAME, subs_packet.status.value))

        if subs_packet.x_coord is not None:
            packed_fields.append(
                self.get_field_string(self.X_COORD_FIELD_NAME, str(subs_packet.x_coord)))

        if subs_packet.y_coord is not None:
            packed_fields.append(
                self.get_field_string(self.Y_COORD_FIELD_NAME, str(subs_packet.y_coord)))

        return self.NEWLINE.join(packed_fields).encode()

    def unpack(self, data: bytes) -> SubsPacket:
        packed_fields = {name: value for (name, value) in
                         [field.split(self.FIELD_VALUE_SEPARATOR) for field in data.decode().split(self.NEWLINE)]}

        try:
            # Access required fields using indexer and optional fields using get(...):
            # An undefined required field will raise a KeyError, while an undefined
            # optional field will just return None.
            protocol_version = packed_fields[self.VERSION_FIELD_NAME]
            packet_type = Type(packed_fields[self.TYPE_FIELD_NAME])

            status = packed_fields.get(self.STATUS_FIELD_NAME)
            if status is not None:
                status = Status(status)

            x_coord = packed_fields.get(self.X_COORD_FIELD_NAME)
            if x_coord is not None:
                x_coord = int(x_coord)

            y_coord = packed_fields.get(self.Y_COORD_FIELD_NAME)
            if y_coord is not None:
                y_coord = int(y_coord)

            return SubsPacket(
                protocol_version,
                packet_type,
                status,
                x_coord,
                y_coord
            )
        except ValueError as error:
            raise errors.PacketUnpackError("Could not unpack packet: Invalid field types!") from error
        except KeyError as error:
            raise errors.PacketUnpackError("Could not unpack packet: Required fields missing!") from error
