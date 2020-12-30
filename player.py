import argparse

import socket

import errors
import subs_packet
import subs_protocol_text_packer
import subs_packet_validator
import subs_protocol
from subs_protocol_stream import SubsProtocolStream

ALL_INTERFACES = "0.0.0.0"

RECEIVED_PACKET_ERRORS = (errors.InvalidPacketError, errors.PacketUnpackError)

TERMINATING_PACKET_TYPES = (
    (subs_packet.Type.ANSWER, subs_packet.Status.ANSWER_VICTORY),
    (subs_packet.Type.ERROR, subs_packet.Status.ERROR_CLOSED)
)


def get_argument_parser():
    argument_parser = argparse.ArgumentParser(description="Play submarines!")
    argument_parser.add_argument('ip')
    argument_parser.add_argument('--host', action="store_true")
    return argument_parser


def is_terminating_packet(packet: subs_packet.SubsPacket):
    return (packet.packet_type, packet.status) in TERMINATING_PACKET_TYPES


def send_close_packet(stream: SubsProtocolStream):
    stream.send(subs_packet.SubsPacket.error(subs_protocol.VERSION, subs_packet.Status.ERROR_CLOSED))


def send_unexpected_error_packet(stream: SubsProtocolStream):
    stream.send(subs_packet.SubsPacket.error(subs_protocol.VERSION, subs_packet.Status.ERROR_UNEXPECTED))


def receive_packet(stream: SubsProtocolStream, of_type: subs_packet.Type):
    response = None
    while response is None:
        try:
            response = stream.receive()
            if is_terminating_packet(response) or response.packet_type == subs_packet.Type.ERROR:
                return response

            if response.packet_type != of_type:
                send_unexpected_error_packet(stream)
                response = None

        except RECEIVED_PACKET_ERRORS:
            send_unexpected_error_packet(stream)
            response = None
        except socket.error as error:
            send_close_packet(stream)
            response = None
    return response


def main():
    arguments = get_argument_parser().parse_args()

    is_host = arguments.host
    try:
        ip = socket.inet_aton(arguments.ip)
    except socket.error:
        print(f"\'{arguments.ip}\' is not a legal IP Address. Aborting.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as player_socket:
        if is_host:
            player_socket.bind((ALL_INTERFACES, subs_protocol.PORT))
            player_socket.listen()
            client_socket, _ = player_socket.accept()
        else:
            client_socket = player_socket
            client_socket.connect((arguments.ip, subs_protocol.PORT))

        stream = SubsProtocolStream(client_socket,
                                    subs_protocol_text_packer.SubsProtocolTextPacker(),
                                    subs_packet_validator.SubsPacketValidator(subs_protocol.VERSION))

        # TODO: Order board

        if not is_host:
            stream.send(subs_packet.SubsPacket.ready(subs_protocol.VERSION))

        response = receive_packet(stream, subs_packet.Type.READY)

        if is_host:
            stream.send(subs_packet.SubsPacket.ready(subs_protocol.VERSION))

        # Start Game

        start_by_receiving_attempt = is_host

        while not is_terminating_packet(response):

            if start_by_receiving_attempt:
                while True:
                    response = receive_packet(stream, subs_packet.Type.ATTEMPT)

                    # TODO: Implement sub check
                    answer_status = subs_packet.Status.ANSWER_INCORRECT

                    stream.send(subs_packet.SubsPacket.answer(subs_protocol.VERSION, answer_status,
                                                              response.x_coord, response.y_coord))

                    if answer_status not in (subs_packet.Status.ANSWER_CORRECT, subs_packet.Status.ANSWER_FULL_SUB):
                        break

            # TODO: Customize coords
            attempt_x, attempt_y = 0, 0

            stream.send(subs_packet.SubsPacket.attempt(subs_protocol.VERSION, attempt_x, attempt_y))

            response = receive_packet(stream, subs_packet.Type.ANSWER)

            start_by_receiving_attempt = response.status not in \
                                         (subs_packet.Status.ANSWER_CORRECT, subs_packet.Status.ANSWER_FULL_SUB)



if __name__ == "__main__":
    main()
