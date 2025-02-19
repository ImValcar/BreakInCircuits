import socket
import threading

port = 1337 # Puerto en el que se va a establecer el listener

# Creamos un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', port))
server_socket.listen(1)

print(f"Escuchando en 0.0.0.0:{port}")

def strip_message(data):
    return data[4:].decode("utf-8").split(";")

def receive_messages(connection):
    while True:
        try:
            data = connection.recv(256)
            if not data:
                continue
            message = strip_message(data)
            print("Recibido:", message)
        except Exception as e:
            print(f"Error al recibir datos: {e}")
            break
    connection.close()

def send_messages(connection):
    while True:
        try:
            msg = input("Escribe un mensaje: ")
            msg = msg.split(" ")
            command = msg.pop(0).lower()
            msg = " ".join(msg)
            if command == "exit":
                connection.sendall(b'\x03\x00\x01\x07')
                connection.close()
                break
            elif command == "send":
                encoded_message=msg.encode("utf-8")
                connection.sendall(b'\x02\x00\x00\x00'+encoded_message+b'\xff\xff')
                continue
        except Exception as e:
            print(f"Error al enviar datos: {e}")
            break

while True:
    print("Esperando conexión...")
    connection, client_address = server_socket.accept()
    print(f"Conectado a {client_address}")

    # Hilos para enviar y recibir al mismo tiempo
    recv_thread = threading.Thread(target=receive_messages, args=(connection,))
    send_thread = threading.Thread(target=send_messages, args=(connection,))

    recv_thread.start()
    send_thread.start()

    # Esperamos a que los hilos terminen antes de aceptar otra conexión
    recv_thread.join()
    send_thread.join()
