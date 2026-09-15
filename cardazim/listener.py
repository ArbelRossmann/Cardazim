from __future__ import annotations

import socket

from connection import Connection


class Listener:
    def __init__(self, host: str, port: int, backlog=1000) -> None:
        self.host = host
        self.port = port
        self.backlog = backlog
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __repr__(self) -> str:
        """ "
        Returns human-readable format of listener.
        """
        return f'Listener(port={self.port}, host="{self.host}", backlog={self.backlog})'

    def start(self) -> None:
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)

    def stop(self) -> None:
        self.sock.close()

    def accept(self) -> Connection:
        return Connection(self.sock.accept()[0])

    def __enter__(self) -> Listener:
        """
        Context manager enter.
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """
        Context manager exit.
        """
        self.stop()
