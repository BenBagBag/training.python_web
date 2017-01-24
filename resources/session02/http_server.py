import socket
import sys


def response_ok():
    """this function returns the simple http response"""
    # sockets only accept bytes
    return b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nthis is a pretty minimal response"


def parse_request(req):
    first_line = req.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    print("request is ok", file=sys.stderr)
    return uri


def response_method_not_allowed():
    return b"HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\n\r\nthis method is not allowed"


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                request = ""
                while True:
                    data = conn.recv(1024)
                    request += data.decode("utf8")
                    print('received "{0}"'.format(data), file=log_buffer)
                    if len(data) < 1024:
                        msg = 'no more data from {0}:{1}'.format(*addr)
                        print(msg, log_buffer)
                        break
                try:
                    uri = parse_request(request)
                    response = response_ok()
                except NotImplementedError:
                    response = response_method_not_allowed()
                else:
                    try:
                        content, mime_type = resolve_uri(url)
                    except NameError:
                        response = response_not_found()
                    else:
                        response = response_ok(content, mime_type)
                conn.sendall(response)
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
