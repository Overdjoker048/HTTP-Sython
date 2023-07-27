import json
import requests
import os

default = {
    "ip": requests.get('https://api.ipify.org').text,
    "default_page": "index.html",
    "404_page": "error_404.html",
    "request": 0,
}

class Config:
    def __init__(self) -> None:
        try:
            with open(os.path.join("assets", "config.json"), "r") as file:
                self.info = json.load(fp=file)["format"]
                if self.info["ip"] == default["ip"]:
                    self.info["ip"] = requests.get('https://api.ipify.org').text
                    self.save()
        except:
            with open(os.path.join("assets", "config.json"), "w") as file:
                json.dump(default, file, indent=2)
                self.info = default
    
    def save(self) -> None:
        with open(os.path.join("assets", "config.json"), "w") as file:
            json.dump(self.info, file, indent=2)