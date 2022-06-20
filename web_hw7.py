import socket
import time
import threading


def my_server(host, port):
    """Standart server
    """
    sock_serv = socket.socket()
    # context manager to avoid any bag
    with sock_serv:
        # Set a socket option.  See the Unix manual for level and option.
        sock_serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to a local address as tuple for IP
        sock_serv.bind((host, port))
        # wait connection  - 2 item in order
        sock_serv.listen(1)
        # we have connection - create this
        connect, addr = sock_serv.accept()
        print(f"Server echo - reqeust from {addr}, connect")
        # new socket object for exchange data
        with connect:
            while True:
                # 512 bytes for once because recv is block function
                data = connect.recv(512)
                print(f'From client: {data}')
                if not data:
                    break
                connect.sendall(b"Have done this session")


def my_client(host, port, data:str):
    """Standart client
    """
    sock_client = socket.socket()
    name_host = socket.gethostbyaddr(host)[0] # tuple return with name 
    # context manager to avoid any bag
    with sock_client:
        while True:
            try:
                # try to connect
                sock_client.connect((host, port))
                # send string
                sock_client.sendall(("Hello from client "+name_host).encode())
                sock_client.sendall(data.encode())
                # wait recieve data
                data = sock_client.recv(1024)
                print(f'From server: {data}')
                break
            except ConnectionRefusedError:
                # try to connect again
                time.sleep(0.5)


if __name__ == "__main__":
    # Constant write with uppercase!!!
    HOST = "127.0.0.1"
    PORT = 5000
    data_from_client = "  <My data from client>"
    # Create treads with server and client
    server_1 = threading.Thread(target=my_server, args=(HOST, PORT))
    client_1 = threading.Thread(target=my_client, args=(HOST, PORT,
                                                        data_from_client))
    server_1.start()
    client_1.start()
    server_1.join()
    client_1.join()
    
    print("Good job, isn`t it?")
    
