import argparse
import sys
import threading

import connection
import listener

###########################################################
####################### YOUR CODE #########################
###########################################################


def handle_connection(conn: connection.Connection):
    """
    Handles the connection.

    :param conn: socket representing the connection
    :type conn: socket
    """
    with conn:
        while True:
            message = conn.receive_message()
            if not message:
                break
            print(f"Received data: {message}")


def run_server(ip, port):
    """
    Receive data sent to ip:port and print to screen.

    :param ip: ip to host server on
    :type ip: ip number
    :param port: port to host on
    :type port: number
    """
    with listener.Listener(ip, port) as l:
        t = threading.Thread(target=handle_connection, args=(l.accept(),))
        t.start()


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
        print("Done.")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
