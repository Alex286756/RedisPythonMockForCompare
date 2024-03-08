import socket
import fakeredis

HOST = "0.0.0.0"
PORT = 6379  

if __name__ == "__main__":
    server = fakeredis.FakeServer()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_to_out:
        server_to_out.bind((HOST, PORT))
        server_to_out.listen()
        server_to_fakeredis = fakeredis.FakeRedis(
            host="localhost",
            port=6380,
            db=0,
            username="",
            password=""
        )
        redis_socket = fakeredis.FakeConnection()
        while True:
            out_client_socket, addr = server_to_out.accept()
            with out_client_socket:
                data = out_client_socket.recv(1024).decode('utf-8')
                if data.strip() == 'shutdown':
                    break

                redis_socket.send_command(data.strip())
                response = redis_socket.read_response()
                if type(response) == bytes:
                    out_client_socket.send(response)
                    out_client_socket.send(b'\r\n')
                elif type(response) == list:
                    for el in response:
                        out_client_socket.send(el)
                        out_client_socket.send(b'\r\n')