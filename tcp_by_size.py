__author__ = "Idan"


SIZE_HEADER_FORMAT = "000000000|"  # n digits for data size + one delimiter
size_header_size = len(SIZE_HEADER_FORMAT)
TCP_DEBUG = True
LEN_TO_PRINT = 100


def recv_by_size(sock):
    """
    Process: Receives data of any size and returns it as bytes (still encoded)
    :parameter: sock (socket)
    :return: data (bytes)
    """

    size_header = b''
    data_len = 0
    while len(size_header) < size_header_size:
        _s = sock.recv(size_header_size - len(size_header))
        if _s == b'':
            size_header = b''
            break
        size_header += _s
    data = b''
    if size_header != b'':
        data_len = int(size_header[:size_header_size - 1])
        while len(data) < data_len:
            _d = sock.recv(data_len - len(data))
            if _d == b'':
                data = b''
                break
            data += _d

    if TCP_DEBUG and size_header != b'':
        print("\nRecv(%s)>>>" % (size_header,), end='')
        print("%s" % (data[:min(len(data), LEN_TO_PRINT)],))
    if data_len != len(data):
        data = b''  # Partial data is like no data !
    return data


def send_with_size(sock, bdata):
    """
    Process: Sends encoded data of any size
    :parameter: sock (socket), bdata (bytes / string)
    :return: nothing
    """

    if type(bdata) == str:
        bdata = bdata.encode()
    len_data = len(bdata)
    header_data = str(len(bdata)).zfill(size_header_size - 1) + "|"

    bytea = bytearray(header_data, encoding='utf8') + bdata

    sock.send(bytea)
    if TCP_DEBUG and len_data > 0:
        print("\nSent(%s)>>>" % (len_data,), end='')
        print("%s" % (bytea[:min(len(bytea), LEN_TO_PRINT)],))
