# Simple proxy server
A simple http(s) proxy server implementation in Python.
## Example

![](https://github.com/kirill-ivanov-a/https-proxy/blob/main/examples/httpbin.gif)
## Requirements
- Python 3.x
- http_parser

## Installation
1. Clone this repository:
```bash
git clone https://github.com/kirill-ivanov-a/https-proxy.git
```
2. Go to project directory:
```bash
cd https-proxy/
```
3. Install requirements:
```bash
pip install -r requirements.txt
```
## Usage
```bash
usage: python -m proxy [-h] [--host HOST] [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           host to listen (default: 0.0.0.0)
  --port PORT, -p PORT  port to listen (default: 9000)
```
