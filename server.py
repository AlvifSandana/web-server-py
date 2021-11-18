import socket
import os

# define host and port
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000

# change directory
public_dir = os.path.join(os.path.dirname(__file__), 'public')
os.chdir(public_dir)

# define a new socket with address family and kind of socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set socket options (socket level, option name, )
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket
server_socket.bind((HOST, PORT))
# listening connection 
server_socket.listen()
print(f'Listening on http://{HOST}:{PORT} ...')

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)

    # Handling request by read url and method
    # Get request line by split the request with \r\n
    # (Carriage Return Line Feed => CRLF)
    split_req = request.split("\r\n")[0].split(' ')

    # get request url
    url = split_req[1]
    # get request method
    method = split_req[0]
    # handle by method
    if method == 'GET':
        if url == '/':
            # open file index.html
            with open('index.html', 'r') as file:
                html = file.read()
            # create response
            response = f"HTTP/1.1 200 OK\n\n{html}"
        else:
            # open file 404.html
            with open('404.html', 'r') as file:
                html = file.read()
            # create response
            response = f"HTTP/1.1 404 NOT FOUND\n\n{html}"

    # send response
    client_connection.sendall(response.encode())
    # close client connection
    client_connection.close()

# Close socket
server_socket.close()
