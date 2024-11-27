import socket
import threading
import random



def create_backend_servers(port, queue_con, backend_host):
    backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (backend_host, port)
    backend_socket.bind(address)
    backend_socket.listen(queue_con)
    print(f"Backend server started on {backend_host} {port}")
    while True:
        client_socket, client_add = backend_socket.accept() # rerturns client socket
        print("Client address for backend", client_add)
        client_data = client_socket.recv(2048).decode()
        response = "HTTP/1.1 200 OK\r\n\r\nHello from the backend server on " + str(port)
        client_socket.sendall(response.encode())
        client_socket.close()

def create_loadbalancer(lb_port, lb_host, queue_con):
    lb_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    lb_add = (lb_host, lb_port)
    lb_socket.bind(lb_add)
    lb_socket.listen(queue_con)
    print(f"Load Balancer started on {lb_host} {lb_port}")
    while True:
        client_socket, client_add = lb_socket.accept()
        print("Client address for LB", client_add)
        threading.Thread(target=server_client, args=(client_socket,)).start()


def server_client(client_socket):
    client_data = client_socket.recv(2048).decode()
    backend_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend_add = rebalance()
    backend_sock.connect(backend_add)
    backend_sock.sendall(client_data.encode()) #sending data received from client to backend
    backend_response = backend_sock.recv(1024) #getting resonse from backend
    client_socket.sendall(backend_response)  #sending the same reponse to client.
    client_socket.close()


def rebalance():
    return random.choice(backend_servers)




if __name__ == "__main__":
    backend_servers = [('localhost', 9086), ('localhost', 9087), ('localhost', 9089)]
    queue_con = 10
    for server in backend_servers:
        threading.Thread(target=create_backend_servers, args=(server[1], queue_con, server[0]),).start()
    lb_port = 9090
    lb_host = 'localhost'
    create_loadbalancer(lb_port, lb_host, queue_con)
        



