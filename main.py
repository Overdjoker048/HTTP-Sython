#Import of the modules necessary for the proper functioning of the HTTP Server.
import os
import pyfiglet
from extention.protocol import *
from extention.config import Config

#Get the server's IP address from the configuration file.
server_ip = Config().info["ip"]

#Setting up of the grahical display.
os.system(f"title [{server_ip}] HTTP Server - Connection: 0")
if not os.path.exists("assets"):
    os.mkdir("assets")
if not os.path.exists("latest"):
    os.mkdir("latest")
pyfiglet.print_figlet("HTTP Server")
print("="*60)
print()

#Initialization of UDP and TCP protocols.
UDP().start()
print(f"UDP Protocol started on port 80")
TCP().start()
print(f"TCP Protocol started on port 80")
print(f"Server running\nhttp://{server_ip}/\n")

#mettre un compteur de connection a
#cmd tracker (créeer un fichier json avec la geolocalisation)
#ajouter un fichier de config