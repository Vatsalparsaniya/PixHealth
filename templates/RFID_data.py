import socket
import pickle
def client_program():
    host = '192.168.43.48' # as both code is running on same pc
    port = 5005  # socket server port number

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server

    data = client_socket.recv(1024)  # receive response
    data = pickle.loads(data)
    # print('Received from server: ' + str(data))  # show in terminal
    return data

print(client_program())