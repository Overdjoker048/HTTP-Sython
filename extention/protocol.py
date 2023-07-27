import threading
import socket
import os
import apache
import extention.addon as addon
from extention.config import *

class UDP(threading.Thread):
    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.UDPsocket.bind(("", 80))

    def run(self) -> None:
        while True:
            self.UDPsocket.recv(8192).decode("utf-8").split("\n")[0].replace("\r", "")
            request, (ip, port) = self.UDPsocket.recvfrom(2048)
            threading.Thread(target=self.send_request, args=(request, ip, port), name=f"{ip}:{port} UDP").start()

    def send_request(self, request: bytes, ip: str, port: int) -> None:
        try:
            cf = Config()
            request = request.decode("utf-8").split("\n")[0].replace("\r", "")

            if request.split(" ")[0] == "GET":
                file = request.split(" ")[1]
                if file == "/":
                    file = cf.info["default_page"]
                if addon.format_file(file).split("/")[0] == "video":
                    data, error_code = addon.format_file(file=file)
                    if data is not None:
                        self.UDPsocket.sendto(data, (ip, port))
                        cf.info['request'] = int(cf.info['request'])+1
            
            elif request.split(" ")[0] == "HEAD":
                file = request.split(" ")[1]
                data, error_code = apache.head(file)
                self.UDPsocket.sendto(data, (ip, port))
            
            elif request.split(" ")[0] == "HEAD":
                self.UDPsocket.sendto(apache.head(), (ip, port))

            os.system(f"title [{cf.info['ip']}] HTTP Server - Connection: {cf.info['request']}")
        except Exception as e:
            self.UDPsocket.sendto("HTTP/1.1 503 Service Unavailable", (ip, port))
            error_code = 503
            print(e)

        cf.save()
        addon.logs(request=f"{ip}:{port} {request} {error_code} UDP")

class TCP(threading.Thread):
    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.socket_proto = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_proto.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_proto.bind(("", 80))

    def run(self):
        while True:
            self.socket_proto.listen(10)
            client, (ip, port) = self.socket_proto.accept()
            threading.Thread(target=self.send_request, args=(client, ip, port), name=f"{ip}:{port} TCP").start()
    
    def send_request(self, client:socket.socket, ip: str, port: int) -> None:
        try:
            cf = Config()
            request = client.recv(2048).decode("utf-8").split("\n")[0].replace("\r", "")
            if request.split(" ")[2] == "HTTP/1.1" or request.split(" ")[2] == "HTTP/1.0":
                if request.split(" ")[0] == "GET":
                    file = request.split(" ")[1]
                    if addon.format_file(file).split("/")[0] in ["text", "image", "other"] or file == "/":
                        data, error_code = apache.get(file=file)
                        client.send(data)

                elif request.split(" ")[0] == "HEAD":
                    file = request.split(" ")[1]
                    if addon.format_file(file).split("/")[0] in ["text", "image", "other"] or file == "/":
                        data, error_code = apache.head(file)
                        client.send(data)
                        print(data)
                
                elif request.split(" ")[0] == "OPTIONS":
                    data, error_code = apache.options()
                    client.send(data)

            else:
                client.send(b"HTTP/1.1 505 HTTP Version Not Supported")
                error_code = 505
        except Exception as e:
            print(e)
            client.send(b"HTTP/1.1 503 Service Unavailable")
            error_code = 503

        cf.info['request'] = int(cf.info['request'])+1
        cf.save()
        os.system(f"title [{cf.info['ip']}] HTTP Server - Connection: {cf.info['request']}")
        addon.logs(request=f"{ip}:{port} {request} {error_code} TCP")