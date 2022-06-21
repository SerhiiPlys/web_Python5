import socket


# Constant write with uppercase!!!
HOST = "127.0.0.1"
PORT = 5000

def my_server(host, port):
    sock_serv = socket.socket()
    name_host = socket.gethostbyaddr(HOST)[0] # tuple return with name
    print(f"Server on host {name_host}")
    # context manager to avoid any bag
    with sock_serv:
        # Set a socket option.  See the Unix manual for level and option.
        sock_serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to a local address as tuple for IP
        sock_serv.bind((HOST, PORT))
        while True:
            sock_serv.listen(5)
            connect, addr = sock_serv.accept()
            print(f"Server echo - reqeust from {addr}, connect")
            data  = connect.recv(1024)
            if not data:
                continue;
            print(f'From client: {data}')
            if data == "good bye".encode():
                connect.sendall(b"Have done this session")
                break
            elif data =="answer".encode():
                connect.sendall(b"Here you go")
            else:
                connect.sendall(b"Okay")
                    
                
if __name__ == "__main__":
    my_server(HOST, PORT)
