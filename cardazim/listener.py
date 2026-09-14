from __future__ import annotations

import socket

import connection


class Listener:
    def __init__(self, host: str, port: int, backlog=1000):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __repr__(self):
        """ "
        Returns human-readable format of listener.
        """
        return f'Listener(port={self.port}, host="{self.host}", backlog={self.backlog})'

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)

    def stop(self):
        self.sock.close()

    def accept(self) -> connection.Connection:
        return connection.Connection(self.sock.accept()[0])

    def __enter__(self):
        """
        Context manager enter.
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        """
        Context manager exit.
        """
        self.stop()
