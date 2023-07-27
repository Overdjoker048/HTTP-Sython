from bs4 import BeautifulSoup
import os
import time
import extention.addon as addon
from extention.config import Config

def get(file: str) -> list:
    cf = Config()
    if file == "/":
        file = cf.info["default_page"]
    try:
        if os.path.splitext(file)[1].replace(".", "").lower() == "html":
            with open(file, "r") as f:
                content = f.read()
                charset = "utf-8"
                meta_charset = BeautifulSoup(content, 'html.parser').find('meta', charset=True)
                if meta_charset:
                    charset = meta_charset['charset']
                content = content.encode("latin-1").decode('utf-8')
                return (addon.header(file=file, data=content.encode(charset)), 200)
        elif addon.format_file(os.path.splitext(file)[1].replace(".", "").lower()).split("/")[0] == "image":
            with open(file[1:], "rb") as f:
                #bug a regler avec les images
                return (addon.header(file=file[1:], data=f.read()), 200)
        else:
            with open(file[1:], "r") as f:
                return (addon.header(file=file, data=f.read().encode("utf-8")), 200)
    except FileNotFoundError:
        with open(cf.info["404_page"], "r") as f:
            content = f.read()
            charset = "utf-8"
            meta_charset = BeautifulSoup(content, 'html.parser').find('meta', charset=True)
            if meta_charset:
                charset = meta_charset['charset']
            content = content.encode("latin-1").decode('utf-8')
            return (addon.header(file=cf.info["404_page"], data=content.encode(charset), message="HTTP/1.1 404 Not Found"), 404)

def head(file: str) -> bytes:
    cf = Config()
    if file == "/":
        file = cf.info["default_page"]
    try:
        with open(file, "r") as f:
            return (f"""HTTP/1.1 200 OK"
Content-Length: {len(f.read())}
Content-Type: {addon.format_file(file=file)}""".encode("utf-8"), 200)
    except FileNotFoundError:
        return ("HTTP/1.1 404 Not Found".encode("utf-8"), 404)

def options() -> str:
    return (f"""HTTP/1.1 200 OK
Allow: OPTIONS, GET, HEAD
Cache-Control: Indeterminate
Date: {time.strftime('%a, %d %b %Y %I:%M:%S %p %Z'), time.gmtime()}
Expires: Never
Server: HTTP Sython 1.0
Content-Length: 0""".encode("utf-8"), 200)