import os
from datetime import datetime

def month():
    return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def logs(request: str) -> None:
    time_now = f"{datetime.today().year}/{month()[datetime.today().month-1]}/{datetime.today().day} {datetime.today().hour}:{datetime.today().minute}:{datetime.today().second}"
    print(f"[{time_now}] {request}")
    if not os.path.exists(os.path.join("assets", "latest")):
        os.mkdir(os.path.join("assets", "latest"))
    file = os.path.join("assets", "latest", f"{datetime.today().day}-{datetime.today().month}-{datetime.today().year}.log")
    with open(file, "a+") as f:
        f.write(f"[{time_now}] {request}\n")

def header(file: str, data: bytes, message: str = "HTTP/1.1 200 OK") -> bytes:
    return f"""{message}
Content-Length: {len(data)}
Content-Type: {format_file(file=file)}
Connection: close

""".encode("utf-8")+data

def format_file(file: str) -> str:
    ext = os.path.splitext(file)[1].replace(".", "").lower()
    if ext in ["html", "js", "css"]:
        format = "text"
    elif ext in ['jpg', 'jpeg', 'png', 'gif', "svg"]:
        format = "image"
    elif ext in ['mp4', 'avi', 'mov']:
        format = "video"
    elif ext in ["json"]:
        format = "application"
    else:
        format = "other"
    return f"{format}/{ext}"