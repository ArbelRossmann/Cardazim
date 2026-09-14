from __future__ import annotations

import socket
import struct


class Connection:
    def __init__(self, connection: socket.socket):
        """
        Initializes connection object.
        """
        self.sock = connection

    def __repr__(self):
        """ "
        Returns human-readable format of connection.
        """
        remote_ip, remote_port = self.sock.getpeername()
        local_ip, local_port = self.sock.getsockname()
        return f"<Connection from {local_ip}:{local_port} to {remote_ip}:{remote_port}>"

    def send_message(self, message: bytes):
        """
        Sends message with correct formatting.
        """
        packet = struct.pack(f"<i{len(message)}s", len(message), message)
        self.sock.sendall(packet)

    def receive_message(self) -> str:
        """
        Receives message from socket, raises exception if closed.
        """
        data = self.sock.recv(1024)
        if not data:
            return None
        length = int.from_bytes(data[:4], byteorder="little")
        message = data[4 : 4 + length].decode()
        return message

    @classmethod
    def connect(cls, host: str, port: int) -> Connection:
        """
        Creates new connection to host:port.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return Connection(s)

    def close(self):
        """
        Closes the connection.
        """
        self.sock.close()

    def __enter__(self):
        """
        Context manager enter.
        """
        return self

    def __exit__(self, exc_type, exc, tb):
        """
        Context manager exit.
        """
        self.close()
