# part 4
from part3 import send_udp_message, create_message, get_type, decode_message



def send_request_iterative(name_address):
    message = create_message("A", name_address, 0)
    root_DNS_server = "198.41.0.4"
    port = 53
    response_from_root = send_udp_message(message, root_DNS_server, port)
    ip_arr_from_root = decode_message(response_from_root)
    print("send message to ROOT DNS server(", root_DNS_server, ") and return IPs: \n", ip_arr_from_root)
    print("***************************************************************\n")
    TLD_DNS_server = ip_arr_from_root[1]
    response_from_TLD = send_udp_message(message, TLD_DNS_server, port)
    ip_arr_from_TLD = decode_message(response_from_TLD)
    print("send message to TLD DNS server(", TLD_DNS_server, ") and return IPs: \n", ip_arr_from_TLD)
    print("***************************************************************\n")
    authoritative_DNS_server = ip_arr_from_TLD[0]
    response_from_authoritative = send_udp_message(message, authoritative_DNS_server, port)
    ip_arr_from_authoritative = decode_message(response_from_authoritative)
    print("send message to authoritative DNS server(", authoritative_DNS_server, ") and return IP (final IP): \n",
          ip_arr_from_authoritative[0])
    print("***************************************************************")


if __name__ == "__main__":
    name_address = input("Enter name address: ")
    send_request_iterative(name_address)
