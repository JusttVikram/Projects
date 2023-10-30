import socket
import threading

def handle_client(client_socket, remote_host, remote_port):
    # Connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    while True:
        # Receive data from the client
        data = client_socket.recv(4096)
        if not data:
            break

        # Send the data to the remote host
        remote_socket.sendall(data)

        # Receive data from the remote host
        data = remote_socket.recv(4096)
        if not data:
            break

        # Send the data back to the client
        client_socket.sendall(data)

    # Close the sockets
    client_socket.close()
    remote_socket.close()

def start_proxy_server(local_host, local_port, remote_host, remote_port):
    # Create a listening socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((local_host, local_port))
    server_socket.listen(5)

    print(f'[*] Listening on {local_host}:{local_port}')

    while True:
        # Accept incoming client connections
        client_socket, client_address = server_socket.accept()
        print(f'[*] Accepted connection from {client_address[0]}:{client_address[1]}')

        # Start a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, remote_host, remote_port))
        client_thread.start()

if __name__ == '__main__':
    # Change these values to match your requirements
    local_host = '0.0.0.0'
    local_port = 8080
    remote_host = 'www.google.com'
    remote_port = 80

    start_proxy_server(local_host, local_port, remote_host, remote_port)
