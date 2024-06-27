__author__ = "Idan"


SIZE_HEADER_FORMAT = "000000000|"  # n digits for data size + one delimiter
size_header_size = len(SIZE_HEADER_FORMAT)
TCP_DEBUG = False
LEN_TO_PRINT = 100


def recv_by_size(sock):
    """
    Extracts the size of the received data and then extracts the remaining relevant data until the size that was stated. Then return the data (still in bytes).

    Args:
        sock (socket): The socket to recieve data from.

    Returns:
        bytes: The received data.
    """

    size_header = b''
    data_len = 0
    
    # extract the size of the data
    while len(size_header) < size_header_size:
        _s = sock.recv(size_header_size - len(size_header))
        if _s == b'':
            size_header = b''
            break
        size_header += _s
    data = b''
    # if a size header was extracted
    if size_header != b'':
        # extact the data until the full size of the size header was reached
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
    Sends encoded data, and pads the size of the data to the start of the data chunk.

    Args:
        sock (socket): The socket in which to send the data.
        bdata (bytes | str): The data to send. If the data is str it will be encoded before sending it.
    """

    if type(bdata) == str:
        bdata = bdata.encode()
    len_data = len(bdata)
    # pad the size as a header to the data
    header_data = str(len(bdata)).zfill(size_header_size - 1) + "|"

    bytea = bytearray(header_data, encoding='utf8') + bdata

    sock.send(bytea)
    if TCP_DEBUG and len_data > 0:
        print("\nSent(%s)>>>" % (len_data,), end='')
        print("%s" % (bytea[:min(len(bytea), LEN_TO_PRINT)],))
