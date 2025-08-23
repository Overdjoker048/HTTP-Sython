# HTTP-Sython
![Python Version](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-1.1.0-yellow)

A lightweight and efficient HTTP server implementation in Python that supports both TCP and UDP protocols.

## Features

- Dual protocol support (TCP/UDP)
- Multi-threaded request handling
- Compatible with HTTP/1.1 and HTTP/2.0
- Complete HTTP method support (GET, POST, PUT, DELETE, etc.)
- File blacklisting capabilities
- Automatic MIME type detection (150+ types supported)
- Request logging system
- Cache control headers
- Keep-alive connections (TCP)
- Datagram fragmentation handling (UDP)

## Installation

```bash
git clone https://github.com/Overdjoker048/HTTP-Sython.git
cd HTTP-Sython
```

## Quick Start

### Basic TCP Server

```python
from HTTP_Sython import TCP

server = TCP()
server.start()  # Starts server on default port 80
```

### Basic UDP Server

```python
from HTTP_Sython import UDP

server = UDP()
server.start()  # Starts server on default port 80
```

## Configuration

### Blacklist Configuration

```python
from HTTP_Sython import config

config["blacklist"] = [
    "private.txt",
    "config.ini",
    "admin/"
]
```

### Default Page Configuration

```python
from HTTP_Sython import config

config["/"] = "index.html"  # Set default page
```

## Supported HTTP Methods

- GET
- HEAD
- POST
- PUT
- DELETE
- CONNECT
- OPTIONS
- TRACE
- PATCH

## File Type Support

The server automatically detects and sets appropriate MIME types for:
- Web files (HTML, CSS, JavaScript)
- Images (JPEG, PNG, GIF, WEBP, etc.)
- Videos (MP4, AVI, WEBM, etc.)
- Audio (MP3, WAV, OGG, etc.)
- Documents (PDF, DOC, DOCX, etc.)
- Archives (ZIP, RAR, 7Z, etc.)
- And many more...

## Logging

Logs are automatically saved in the `latest` directory with the filename format `DD-MM-YYYY.log`

## Requirements

- Python 3.6 or higher
- No external dependencies required

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- **Overdjoker048**

## Version

Current version: 1.1.0

## Contributing

Contributions, issues, and feature requests are welcome!

## Copyright

Copyright (c) 2025 Overdjoker048
