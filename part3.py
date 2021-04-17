# part3
import binascii
import socket
from collections import OrderedDict


def create_socket():
    created_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return created_socket


def send_udp_message(message, address, port):
    message = message.replace(" ", "").replace("\n", "")
    server_address = (address, port)
    created_socket = create_socket()

    try:
        created_socket.sendto(binascii.unhexlify(message), server_address)
        data, _ = created_socket.recvfrom(4096)
    finally:
        created_socket.close()
    return binascii.hexlify(data).decode("utf-8")


def create_message(type_record="A", name_address="", is_recursion=1):
    ID = 43690
    QR = 0
    OPCODE = 0
    AA = 0
    TC = 0
    RA = 0
    Z = 0
    RCODE = 0

    if is_recursion:
        RD = 1  # recursion
    else:
        RD = 0  # iterative

    query_params = str(QR)
    query_params += str(OPCODE).zfill(4)
    query_params += str(AA) + str(TC) + str(RD) + str(RA)
    query_params += str(Z).zfill(3)
    query_params += str(RCODE).zfill(4)
    query_params = "{:04x}".format(int(query_params, 2))

    QDCOUNT = 1  # Number of questions
    ANCOUNT = 0  # Number of answers
    NSCOUNT = 0  # Number of authority records
    ARCOUNT = 0  # Number of additional records

    message = ""
    message += "{:04x}".format(ID)
    message += query_params
    message += "{:04x}".format(QDCOUNT)
    message += "{:04x}".format(ANCOUNT)
    message += "{:04x}".format(NSCOUNT)
    message += "{:04x}".format(ARCOUNT)

    # QNAME is name_address split up by '.', preceded by int indicating length of part
    addr_parts = name_address.split(".")
    for part in addr_parts:
        addr_len = "{:02x}".format(len(part))
        addr_part = binascii.hexlify(part.encode())
        message += addr_len
        message += addr_part.decode()

    message += "00"  # Terminating bit for QNAME

    # Type of request
    QTYPE = get_type(type_record)
    message += QTYPE

    # Class for lookup. 1 is Internet
    QCLASS = 1
    message += "{:04x}".format(QCLASS)

    return message


def decode_message(message):
    ip_arr = []

    ANCOUNT = message[12:16]
    AN_count_int = int(ANCOUNT, 16)

    NSCOUNT = message[16:20]
    NS_count_int = int(NSCOUNT, 16)

    ARCOUNT = message[20:24]
    AR_count_int = int(ARCOUNT, 16)

    # Question section
    start = 24
    question_parts = parse_parts(message, start, [])
    QTYPE_STARTS = start + (len("".join(question_parts))) + (len(question_parts) * 2) + 2
    QCLASS_STARTS = QTYPE_STARTS + 4

    # Answer section
    ANSWER_SECTION_STARTS = QCLASS_STARTS + 4
    start = ANSWER_SECTION_STARTS

    size_of_each_part = 0
    if AN_count_int > 0:
        size_of_each_part = AN_count_int
    elif AR_count_int == 0:
        return 0
    else:
        # RDLENGTH = int(message[start + 20:start + 24], 16)
        # start += (AN_count_int) * (24 + (RDLENGTH * 2))
        for i in range(NS_count_int):
            ATYPE = message[start + 4: start + 8]
            # print(ATYPE)
            start += (24 + ((int(message[start + 20: start + 24], 16)) * 2))
        size_of_each_part = AR_count_int

    for index_AR in range(size_of_each_part):
        ATYPE = message[start + 4:start + 8]
        RDLENGTH = int(message[start + 20:start + 24], 16)
        RDDATA = message[start + 24:start + 24 + (RDLENGTH * 2)]

        if ATYPE == "{:04x}".format(1):
            octets = [RDDATA[i:i + 2] for i in range(0, len(RDDATA), 2)]
            RDDATA_decoded = ".".join(list(map(lambda x: str(int(x, 16)), octets)))
            # print(RDDATA_decoded)
            ip_arr.append(RDDATA_decoded)

        else:
            additional_parts = parse_parts(message, start, [])
            RDDATA_decoded = ".".join(
                map(lambda p: binascii.unhexlify(p).decode('iso8859-1'), additional_parts))
            ip_arr.append(RDDATA_decoded)

        start += 24 + (RDLENGTH * 2)

    return ip_arr


def get_type(type):
    types = ["ERROR", "A", "NS", "MD", "MF", "CNAME", "SOA", "MB", "MG", "MR", "NULL", "WKS", "PTS", "HINFO",
             "MINFO", "MX", "TXT"]
    if type in types:
        return "{:04x}".format(types.index(type)) if isinstance(type, str) else types[type]
    else:
        return "0000"


def parse_parts(message, start, parts):
    part_start = start + 2
    part_len = message[start:part_start]

    if len(part_len) == 0:
        return parts

    part_end = part_start + (int(part_len, 16) * 2)
    parts.append(message[part_start:part_end])

    if message[part_end:part_end + 2] == "00" or part_end > len(message):
        return parts
    else:
        return parse_parts(message, part_end, parts)


def find_ip_in_response(response, record_type="A"):
    if record_type == "A":
        ip_hex = response[-8:]
        ip_p1 = int(ip_hex[0:2], 16)
        ip_p2 = int(ip_hex[2:4], 16)
        ip_p3 = int(ip_hex[4:6], 16)
        ip_p4 = int(ip_hex[6:8], 16)
        ip_address = str(ip_p1) + "." + str(ip_p2) + "." + str(ip_p3) + "." + str(ip_p4)
    return ip_address


if __name__ == "__main__":
    # part 3-1
    name_address = input("Enter name address: ")
    message = create_message("A", name_address, 1)
    print("Request:\n", message)

    # part 3-2
    DNS_server, port = "1.1.1.1", 53
    response = send_udp_message(message, DNS_server, port)
    print("response\n", response)
    print("IP address : ", find_ip_in_response(response, "A"))
