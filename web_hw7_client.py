import socket
import time


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
                print(f"Hello from client "+name_host)
                sock_client.sendall(data.encode())
                # wait recieve data
                data = sock_client.recv(1024)
                print(f'From server: {data}')
                break
            except ConnectionRefusedError:
                # try to connect again
                time.sleep(0.5)
    return data


if __name__ == "__main__":
    # Constant write with uppercase!!!
    HOST = "127.0.0.1"
    PORT = 5000
    print(f"Input your message, for exit type \ngood bye\nfor answer type\n\
answer\n")
    while True:
        data_from_client = input("Your message:\n")
        server_data = my_client(HOST, PORT, data_from_client)
        if server_data.decode() == "Have done this session":
            print("from server - good bye")
            break
        if data_from_client == "good bye":
            print("from client - exit")
            break 
        else:
           print(f"message - {server_data.decode()}")
    
    
