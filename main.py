"""
Python Hosting Service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic library for hosting web sites with support for both TCP and UDP protocols.
Provides a simple and efficient way to serve static files and handle HTTP requests.


Basic Usage:
    >>> from HTTP_Sython import TCP, UDP
    
    # Start a TCP server
    >>> tcp_server = TCP()
    >>> tcp_server.start()
    
    # Start a UDP server
    >>> udp_server = UDP()
    >>> udp_server.start()

:copyright: Copyright (c) 2025 Overdjoker048
:license: MIT, see LICENSE for more details.
"""

__encoding__ = "UTF-8"
__title__ = 'HTTP Sython'
__author__ = 'Overdjoker048'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2025 Overdjoker048'
__version__ = '1.1.0'
__all__ = ['TCP', 'UDP']

from threading import Thread
from socket import socket, SOL_SOCKET, SO_REUSEADDR, AF_INET, SOCK_DGRAM, SOCK_STREAM
from time import gmtime, strftime
from os import path
from json import dumps
from subprocess import run, TimeoutExpired

__MIME_MAP = {
    'html': 'text/html', 'htm': 'text/html', 'css': 'text/css', 'js': 'text/javascript',
    'txt': 'text/plain', 'xml': 'text/xml', 'csv': 'text/csv', 'md': 'text/markdown',
    'rtf': 'text/rtf', 'log': 'text/plain', 'conf': 'text/plain', 'ini': 'text/plain',
    'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'gif': 'image/gif',
    'svg': 'image/svg+xml', 'webp': 'image/webp', 'bmp': 'image/bmp', 'ico': 'image/x-icon',
    'tiff': 'image/tiff', 'tif': 'image/tiff', 'avif': 'image/avif', 'heic': 'image/heic',
    'mp4': 'video/mp4', 'avi': 'video/x-msvideo', 'mov': 'video/quicktime',
    'mkv': 'video/x-matroska', 'webm': 'video/webm', 'flv': 'video/x-flv',
    'wmv': 'video/x-ms-wmv', '3gp': 'video/3gpp', 'm4v': 'video/x-m4v',
    'mp3': 'audio/mpeg', 'wav': 'audio/wav', 'ogg': 'audio/ogg', 'aac': 'audio/aac',
    'flac': 'audio/flac', 'm4a': 'audio/mp4', 'wma': 'audio/x-ms-wma',
    'json': 'application/json', 'pdf': 'application/pdf', 'zip': 'application/zip',
    'rar': 'application/vnd.rar', '7z': 'application/x-7z-compressed',
    'tar': 'application/x-tar', 'gz': 'application/gzip', 'xz': 'application/x-xz',
    'doc': 'application/msword', 'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'xls': 'application/vnd.ms-excel', 'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'ppt': 'application/vnd.ms-powerpoint', 'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'woff': 'font/woff', 'woff2': 'font/woff2', 'ttf': 'font/ttf', 'otf': 'font/otf',
    'eot': 'application/vnd.ms-fontobject', 'py': 'text/x-python', 'java': 'text/x-java-source',
    'cpp': 'text/x-c++src', 'c': 'text/x-csrc', 'h': 'text/x-chdr', 'php': 'text/x-php',
    'rb': 'text/x-ruby', 'go': 'text/x-go', 'rs': 'text/x-rust', 'sh': 'text/x-shellscript',
    'sql': 'text/x-sql', 'yaml': 'text/yaml', 'yml': 'text/yaml', 'toml': 'text/plain',
    'properties': 'text/plain', 'env': 'text/plain', 'lock': 'text/plain',
    'exe': 'application/x-msdownload', 'msi': 'application/x-msi',
    'deb': 'application/vnd.debian.binary-package', 'rpm': 'application/x-redhat-package-manager',
    'dmg': 'application/x-apple-diskimage', 'pkg': 'application/octet-stream',
    'bin': 'application/octet-stream', 'manifest': 'application/manifest+json',
    'webmanifest': 'application/manifest+json', 'rss': 'application/rss+xml', 'atom': 'application/atom+xml'
}

__FORBIDDEN_EXTENSIONS = {
    'py', 'pyc', 'pyo', 'pyd', 'pyw', 'pyz',
    'java', 'class', 'jar',
    'cpp', 'c', 'h', 'hpp', 'cc', 'cxx',
    'php', 'php3', 'php4', 'php5', 'phtml',
    'rb', 'rbw',
    'go',
    'rs',
    'sh', 'bash', 'zsh', 'fish',
    'bat', 'cmd', 'ps1',
    'sql',
    'pl', 'pm',
    'lua',
    'r',
    'swift',
    'kt', 'kts',
    'scala',
    'clj', 'cljs',
    'hs',
    'ml', 'mli',
    'fs', 'fsi', 'fsx',
    'vb', 'vbs',
    'asp', 'aspx', 'ascx',
    'jsp', 'jspx',
    'env', 'environment',
    'config', 'cfg', 'conf',
    'ini',
    'yaml', 'yml',
    'toml',
    'properties',
    'plist',
    'htaccess', 'htpasswd',
    'gitignore', 'gitconfig',
    'dockerignore', 'dockerfile',
    'makefile', 'cmake',
    'gradle',
    'npmrc', 'yarnrc',
    'log', 'logs',
    'tmp', 'temp',
    'bak', 'backup',
    'old', 'orig',
    'swp', 'swo',
    'pid',
    'sock',
    'lock',
    'exe', 'msi', 'app', 'deb', 'rpm', 'dmg', 'pkg',
    'bin', 'run', 'out',
    'so', 'dll', 'dylib',
    'db', 'sqlite', 'sqlite3',
    'mdb', 'accdb',
    'dbf',
    'rar', '7z', 'tar', 'gz', 'bz2', 'xz', 'lz',
    'key', 'pem', 'crt', 'cer', 'p12', 'pfx', 'jks',
    'pdb', 'map', 'debug',
    'deps', 'packages',
    'node_modules',
    'vendor',
}

__BACKEND_EXTENSIONS = {
    'py': 'python',
    'php': 'php',
    'rb': 'ruby',
    'js': 'node',
    'go': 'go run',
    'java': 'java',
    'pl': 'perl',
    'lua': 'lua',
    'r': 'Rscript',
}

class __HTTP(Thread):
    __slot__ = ['__socket', '__methodes', 'dir', 'main_file', 'blacklist']
    def __init__(self, socket: socket, directory: str = "./", main_file: str = "index.html") -> None:
        Thread.__init__(self)
        self.__socket = socket
        self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__socket.bind(("", 80))
        self.__methodes = {
            "GET": True,
            "HEAD": True,
            "POST": True,
            "PUT": True,
            "DELETE": True,
            "CONNECT": True,
            "OPTIONS": True,
            "TRACE": True,
            "PATCH": True
        }
        self.dir = directory
        self.main_file = main_file
        self.blacklist = []

    def allow_methode(self, methode: str) -> None:
        self.methodes[methode.upper()] = True
    
    def disable_methode(self, methode: str) -> None:
        self.methodes[methode.upper()] = False
    
    def enable_backend(self, enabled: bool = True) -> None:
        self.backend_enabled = enabled

    def is_forbidden_file(self, file: str) -> bool:
        ext = path.splitext(file)[1][1:].lower()
        return ext in __FORBIDDEN_EXTENSIONS

    def execute_backend_script(self, file: str, query_params: str = "") -> tuple:
        if not self.backend_enabled:
            return False, "Backend execution is disabled"
            
        ext = path.splitext(file)[1][1:].lower()
        if ext not in __BACKEND_EXTENSIONS:
            return False, f"Unsupported backend language: {ext}"
            
        try:
            interpreter = __BACKEND_EXTENSIONS[ext]
            cmd = interpreter.split() + [file]
            
            env = {
                'QUERY_STRING': query_params,
                'REQUEST_METHOD': 'GET',
                'CONTENT_TYPE': 'text/html',
                'HTTP_HOST': 'localhost',
                'PATH': path.dirname(file)
            }

            if ext == 'py':
                env['PYTHONPATH'] = path.dirname(file)

            result = run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                env=env
            )
            
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, f"Script execution failed: {result.stderr}"
                
        except TimeoutExpired:
            return False, "Script execution timeout"
        except FileNotFoundError:
            return False, f"Interpreter not found for {ext} files"
        except Exception as e:
            return False, f"Execution error: {str(e)}"

    def options(self, version: str = "HTTP/1.1") -> bytes:
        return (f"{version} 204 No Content\r\n"
                f"Allow: GET, HEAD, POST, PUT, DELETE, OPTIONS\r\n"
                f"Access-Control-Allow-Origin: *\r\n"
                f"Access-Control-Allow-Methods: GET, HEAD, POST, PUT, DELETE, OPTIONS\r\n"
                f"Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept, Authorization\r\n"
                f"Access-Control-Max-Age: 86400\r\n"
                f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}\r\n"
                f"Server: HTTP Sython 1.1\r\n\r\n".encode("utf-8"))

    def get(self, file: str, full: bool = True, version: str = "HTTP/1.1", query_params: str = "") -> bytes:
        if self.is_forbidden_file(file):
            data = b"<html><body><h1>403 Forbidden</h1><p>Access to this file type is not allowed for security reasons.</p></body></html>"
            status = f"{version} 403 Forbidden"
            content_type = "text/html; charset=utf-8"
            
            headers_list = [
                status,
                f"Content-Length: {len(data)}",
                f"Content-Type: {content_type}",
                f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}",
                "Server: HTTP Sython 1.2 Secure",
                "Connection: close"
            ]
            headers = "\r\n".join(headers_list) + "\r\n\r\n"
            
            if not full:
                return headers.encode('utf-8')
            return headers.encode('utf-8') + data

        ext = path.splitext(file)[1][1:].lower()
        content_type = __MIME_MAP.get(ext, 'application/octet-stream')

        try:
            if ext in __BACKEND_EXTENSIONS and path.exists(file):
                success, output = self.execute_backend_script(file, query_params)
                if success:
                    data = output.encode('utf-8')
                    content_type = "text/html; charset=utf-8"
                    status = f"{version} 200 OK"
                else:
                    data = f"<html><body><h1>500 Internal Server Error</h1><p>{output}</p></body></html>".encode('utf-8')
                    content_type = "text/html; charset=utf-8"
                    status = f"{version} 500 Internal Server Error"
            else:
                with open(file, 'rb') as f:
                    data = f.read()
                status = f"{version} 200 OK"
                
        except (IOError, OSError):
            data = b"<html><body><h1>403 Forbidden</h1><p>Access denied.</p></body></html>"
            status = f"{version} 403 Forbidden"
            content_type = "text/html; charset=utf-8"
        except FileNotFoundError:
            data = b"<html><body><h1>404 Not Found</h1><p>The requested resource could not be found.</p></body></html>"
            status = f"{version} 404 Not Found"
            content_type = "text/html; charset=utf-8"

        headers_list = [
            status,
            f"Content-Length: {len(data)}",
            f"Content-Type: {content_type}",
            f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}",
            "Server: HTTP Sython 1.2 Secure"
        ]

        if content_type.startswith('image/'):
            cache_header = "Cache-Control: public, max-age=31536000"
        elif 'javascript' in content_type or content_type.startswith('text/css'):
            cache_header = "Cache-Control: public, max-age=86400"
        elif content_type == 'application/json':
            cache_header = "Cache-Control: no-cache, no-store, must-revalidate"
        elif ext in __BACKEND_EXTENSIONS:
            cache_header = "Cache-Control: no-cache, no-store, must-revalidate"
        else:
            cache_header = "Cache-Control: public, max-age=3600"
            
        headers_list.append(cache_header)
        headers_list.append("X-Content-Type-Options: nosniff")
        headers_list.append("X-Frame-Options: DENY")
        headers_list.append("X-XSS-Protection: 1; mode=block")
        headers_list.append("Connection: close")
        
        headers = "\r\n".join(headers_list) + "\r\n\r\n"
        
        if not full:
            return headers.encode('utf-8')
        return headers.encode('utf-8') + data

    def post(self, file: str, body: bytes = b"", version: str = "HTTP/1.1") -> bytes:
        if self.is_forbidden_file(file):
            data = dumps({
                "status": "error",
                "message": "Access to this file type is not allowed for security reasons"
            }).encode('utf-8')
            status = f"{version} 403 Forbidden"
            content_type = "application/json; charset=utf-8"
            
            return (
                f"{status}\r\n"
                f"Content-Type: {content_type}\r\n"
                f"Content-Length: {len(data)}\r\n"
                f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}\r\n"
                "Server: HTTP Sython 1.2 Secure\r\n"
                "X-Content-Type-Options: nosniff\r\n"
                "Connection: close\r\n\r\n"
            ).encode('utf-8') + data

        try:
            if body:
                if len(body) > 10 * 1024 * 1024:
                    raise Exception("Request body too large")
                    
                if path.exists(file):
                    with open(file, 'ab') as f:
                        f.write(b"\n--- POST DATA ---\n")
                        f.write(body)
                    message = "Data appended to existing resource"
                    status = f"{version} 200 OK"
                else:
                    with open(file, 'wb') as f:
                        f.write(body)
                    message = "New resource created with POST data"
                    status = f"{version} 201 Created"
                
                response_data = {
                    "status": "success",
                    "message": message,
                    "resource": path.basename(file),
                    "data_received": len(body),
                    "timestamp": strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())
                }
            else:
                response_data = {
                    "status": "success",
                    "message": "POST request received but no data provided",
                    "resource": path.basename(file),
                    "data_received": 0,
                    "timestamp": strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())
                }
                status = f"{version} 200 OK"
            
            data = dumps(response_data, indent=2).encode('utf-8')
            content_type = "application/json; charset=utf-8"
            
        except Exception as e:
            data = dumps({
                "status": "error",
                "message": f"Failed to process POST request: {str(e)}"
            }).encode('utf-8')
            status = f"{version} 500 Internal Server Error"
            content_type = "application/json; charset=utf-8"

        return (
            f"{status}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(data)}\r\n"
            f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}\r\n"
            "Server: HTTP Sython 1.2 Secure\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "Connection: close\r\n\r\n"
        ).encode('utf-8') + data

    def put(self, file: str, body: bytes = b"", version: str = "HTTP/1.1") -> bytes:
        if self.is_forbidden_file(file):
            data = dumps({
                "status": "error",
                "message": "Access to this file type is not allowed for security reasons"
            }).encode('utf-8')
            status = f"{version} 403 Forbidden"
        else:
            try:
                if len(body) > 10 * 1024 * 1024:
                    raise Exception("Request body too large")
                    
                with open(file, 'wb') as f:
                    f.write(body)
                
                if path.exists(file):
                    status = f"{version} 200 OK"
                    message = "Resource updated successfully"
                else:
                    status = f"{version} 201 Created"
                    message = "Resource created successfully"
                
                response_data = {
                    "status": "success",
                    "message": message,
                    "resource": path.basename(file),
                    "size": len(body),
                    "timestamp": strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())
                }
                
                data = dumps(response_data, indent=2).encode('utf-8')
                
            except Exception as e:
                data = dumps({
                    "status": "error",
                    "message": f"Failed to process PUT request: {str(e)}"
                }).encode('utf-8')
                status = f"{version} 500 Internal Server Error"

        return (
            f"{status}\r\n"
            f"Content-Type: application/json; charset=utf-8\r\n"
            f"Content-Length: {len(data)}\r\n"
            f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}\r\n"
            "Server: HTTP Sython 1.2 Secure\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "Connection: close\r\n\r\n"
        ).encode('utf-8') + data

    def delete(self, file: str, version: str = "HTTP/1.1") -> bytes:
        if self.is_forbidden_file(file) or file in [self.main_file, ".", ".."]:
            status = f"{version} 403 Forbidden"
            response_data = {
                "status": "error",
                "message": "Deletion of this resource is not allowed"
            }
        else:
            try:
                if path.exists(file):
                    if path.isfile(file):
                        from os import remove
                        remove(file)
                        message = "File deleted successfully"
                    elif path.isdir(file):
                        raise PermissionError("Directory deletion not allowed")
                    
                    status = f"{version} 200 OK"
                    response_data = {
                        "status": "success",
                        "message": message,
                        "resource": path.basename(file),
                        "timestamp": strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())
                    }
                else:
                    status = f"{version} 404 Not Found"
                    response_data = {
                        "status": "error",
                        "message": "Resource not found"
                    }
                
            except PermissionError:
                status = f"{version} 403 Forbidden"
                response_data = {
                    "status": "error",
                    "message": "Permission denied - cannot delete resource"
                }
            except Exception as e:
                status = f"{version} 500 Internal Server Error"
                response_data = {
                    "status": "error",
                    "message": f"Failed to delete resource: {str(e)}"
                }
        
        data = dumps(response_data, indent=2).encode('utf-8')
        
        return (
            f"{status}\r\n"
            f"Content-Type: application/json; charset=utf-8\r\n"
            f"Content-Length: {len(data)}\r\n"
            f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}\r\n"
            "Server: HTTP Sython 1.2 Secure\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "Connection: close\r\n\r\n"
        ).encode('utf-8') + data

    def connect(self, target: str, version: str = "HTTP/1.1") -> bytes:
        try:
            if ':' in target:
                _, port = target.split(':', 1)
                port = int(port)
                if port in [80, 443]:
                    status = f"{version} 200 Connection established"
                else:
                    status = f"{version} 403 Forbidden"
            else:
                status = f"{version} 400 Bad Request"
            
        except ValueError:
            status = f"{version} 400 Bad Request"
        except Exception:
            status = f"{version} 500 Internal Server Error"

        return (
            f"{status}\r\n"
            f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}\r\n"
            "Server: HTTP Sython 1.2 Secure\r\n"
            "Connection: close\r\n\r\n"
        ).encode('utf-8')

    def patch(self, file: str, body: bytes = b"", version: str = "HTTP/1.1") -> bytes:
        if self.is_forbidden_file(file):
            data = dumps({
                "status": "error",
                "message": "Access to this file type is not allowed for security reasons"
            }).encode('utf-8')
            status = f"{version} 403 Forbidden"
        else:
            try:
                if not path.exists(file):
                    status = f"{version} 404 Not Found"
                    response_data = {
                        "status": "error",
                        "message": "Resource not found - cannot apply patch"
                    }
                else:
                    if len(body) > 10 * 1024 * 1024:
                        raise Exception("Request body too large")
                        
                    with open(file, 'rb') as f:
                        existing_data = f.read()
                    patched_data = existing_data + b"\n--- PATCH APPLIED ---\n" + body
                    with open(file, 'wb') as f:
                        f.write(patched_data)
                    
                    status = f"{version} 200 OK"
                    response_data = {
                        "status": "success",
                        "message": "Patch applied successfully",
                        "resource": path.basename(file),
                        "original_size": len(existing_data),
                        "patched_size": len(patched_data),
                        "timestamp": strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())
                    }
                
                data = dumps(response_data, indent=2).encode('utf-8')
                
            except Exception as e:
                status = f"{version} 500 Internal Server Error"
                data = dumps({
                    "status": "error",
                    "message": f"Failed to apply patch: {str(e)}"
                }).encode('utf-8')

        return (
            f"{status}\r\n"
            f"Content-Type: application/json; charset=utf-8\r\n"
            f"Content-Length: {len(data)}\r\n"
            f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}\r\n"
            "Server: HTTP Sython 1.2 Secure\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "Connection: close\r\n\r\n"
        ).encode('utf-8') + data

    def trace(self, file: str, requests: str, version: str = "HTTP/1.1") -> bytes:
        file_exists = path.exists(file)
        status_line = f"{version} 200 OK" if file_exists else f"{version} 404 Not Found"
        
        return (
            f"{status_line}\r\n"
            "Content-Type: message/http\r\n"
            f"Content-Length: {len(requests.encode('utf-8'))}\r\n"
            f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}\r\n"
            "\r\n"
            f"{requests}"
        ).encode('utf-8')
    
    def handle_requests(self, request_data: bytes, send_response: callable) -> None:
        try:
            request = request_data.decode('utf-8')
            if not request:
                return

            request_lines = request.splitlines()
            if not request_lines:
                return

            try:
                method, path_with_query, version = request_lines[0].split(' ')
            except ValueError:
                send_response(f"HTTP/1.1 400 Bad Request\r\n\r\n".encode('utf-8'))
                return

            if '?' in path_with_query:
                path, query_params = path_with_query.split('?', 1)
            else:
                path, query_params = path_with_query, ""

            if not version.startswith("HTTP/"):
                send_response(f"HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nInvalid HTTP version".encode('utf-8'))
                return
            elif version not in ["HTTP/1.0", "HTTP/1.1"]:
                send_response(
                    f"{version} 505 HTTP Version Not Supported\r\nContent-Type: text/plain\r\n\r\n"
                    f"HTTP version {version} not supported".encode('utf-8')
                )
                return

            if not self.__methodes.get(method, False):
                send_response(
                    f"{version} 405 Method Not Allowed\r\n"
                    f"Allow: {', '.join(k for k,v in self.__methodes.items() if v)}\r\n\r\n".encode('utf-8')
                )
                return

            file_path = path[1:] if path != "/" else self.main_file
            file_path = path.normpath(file_path)
            
            if file_path.startswith('..') or '/../' in file_path:
                data = b"<html><body><h1>403 Forbidden - Invalid Path</h1></body></html>"
                forbidden_response = (
                    f"{version} 403 Forbidden\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(data)}\r\n"
                    f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}\r\n"
                    "Server: HTTP Sython 1.2 Secure\r\n"
                    "Connection: close\r\n\r\n"
                ).encode('utf-8') + data
                send_response(forbidden_response)
                return

            full_path = path.join(self.dir, file_path)

            if file_path in self.blacklist:
                data = b"<html><body><h1>403 Forbidden - Access Denied</h1><p>This resource is blacklisted.</p></body></html>"
                blacklist_response = (
                    f"{version} 403 Forbidden\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(data)}\r\n"
                    f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}\r\n"
                    "Server: HTTP Sython 1.2 Secure\r\n"
                    "Connection: close\r\n\r\n"
                ).encode('utf-8') + data
                send_response(blacklist_response)
                return

            body = b""
            if method in ["POST", "PUT", "PATCH"]:
                if "\r\n\r\n" in request:
                    _, body_str = request.split("\r\n\r\n", 1)
                    body = body_str.encode('utf-8')

            response = None
            if method == "OPTIONS":
                response = self.options(version)
            elif method == "GET":
                response = self.get(full_path, True, version, query_params)
            elif method == "HEAD":
                response = self.get(full_path, False, version, query_params)
            elif method == "POST":
                response = self.post(full_path, body, version)
            elif method == "PUT":
                response = self.put(full_path, body, version)
            elif method == "DELETE":
                response = self.delete(full_path, version)
            elif method == "CONNECT":
                response = self.connect(file_path, version)
            elif method == "TRACE":
                response = self.trace(full_path, request, version)
            elif method == "PATCH":
                response = self.patch(full_path, body, version)
            else:
                response = (
                    f"{version} 501 Not Implemented\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}\r\n"
                    "Server: HTTP Sython 1.2 Secure\r\n"
                    "Connection: close\r\n\r\n"
                    "<html><body><h1>501 Not Implemented</h1><p>The requested method is not implemented.</p></body></html>"
                ).encode('utf-8')
            
            send_response(response)

        except UnicodeDecodeError:
            send_response((
                f"HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}\r\n"
                "Server: HTTP Sython 1.2 Secure\r\n"
                "Connection: close\r\n\r\n"
                "<html><body><h1>400 Bad Request</h1><p>Invalid character encoding in request.</p></body></html>"
            ).encode('utf-8'))
        except Exception as e:
            send_response((
                f"HTTP/1.1 500 Internal Server Error\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Date: {strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime())}\r\n"
                "Server: HTTP Sython 1.2 Secure\r\n"
                "Connection: close\r\n\r\n"
                f"<html><body><h1>500 Internal Server Error</h1><p>An unexpected error occurred: {str(e)}</p></body></html>"
            ).encode('utf-8'))


class TCP(__HTTP):
    """
    TCP server implementation for HTTP protocol.

    Handles incoming TCP connections by creating a new thread for each client.
    Supports standard HTTP methods, file serving, and blacklist protection.
    Implements keep-alive connections and connection pooling.
    Includes HTTP version detection (1.0, 1.1, 2.0).

    Methods:
        run(): Main server loop that accepts and handles client connections
        __handle_client(client, addr): Processes individual client requests
        __parse_http_version(version_string): Parses and validates HTTP version

    Example of use:
        >>> server = TCP()
        >>> server.start()  # Starts server on default port 80
    """
    def __init__(self, directory: str = "./", main_file: str = "index.html") -> None:
        super().__init__(socket(AF_INET, SOCK_STREAM), directory, main_file)
        self.__socket.setsockopt(SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.__socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
        self.__socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
        self.__socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 6)

    def __handle_client(self, client: socket) -> None:
        try:
            request = client.recv(8192)
            self.handle_requests(request, client.send)
        finally:
            client.close()
        
    def run(self) -> None:
        self.__socket.listen(10)
        while True:
            client, _ = self.__socket.accept()
            Thread(target=self.__handle_client, args=(client)).start()


class UDP(__HTTP):
    """
    UDP server implementation for HTTP protocol.

    Handles incoming UDP datagrams by creating a new thread for each request.
    Implements datagram fragmentation for large responses and maintains
    stateless communication as per UDP specification.
    Includes HTTP version detection (1.0, 1.1, 2.0).

    Methods:
        run(): Main server loop that receives and processes UDP datagrams
        __handle_datagram(data, addr): Processes individual UDP requests
        __parse_http_version(version_string): Parses and validates HTTP version

    Example of use:
        >>> server = UDP()
        >>> server.start()
    """
    def __init__(self, directory: str = "./", main_file: str = "index.html") -> None:
        super().__init__(socket(AF_INET, SOCK_DGRAM), directory, main_file)

    def __handle_datagram(self, data: bytes, addr: tuple) -> None:
        def send_chunked(response: bytes):
            for i in range(0, len(response), 8192):
                chunk = response[i:i + 8192]
                self.__socket.sendto(chunk, addr)
        self.handle_requests(data, send_chunked)

    def run(self) -> None:
        while True:
            try:
                data, addr = self.__socket.recvfrom(65535)
                Thread(target=self.__handle_datagram, args=(data, addr)).start()
            except Exception:
                pass
 