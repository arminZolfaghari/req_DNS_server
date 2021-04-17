from part3 import send_udp_message, create_message, find_ip_in_response, decode_message


if __name__ == "__main__":
    name_address = input("Enter name address: ")
    type_record = input("Type record: ")
    message = create_message(type_record, name_address, 1)
    print("Request:\n", message)

    DNS_server, port = "1.1.1.1", 53
    response = send_udp_message(message, DNS_server, port)
    print("response\n", response)
    print("IP address : ", decode_message(response))
