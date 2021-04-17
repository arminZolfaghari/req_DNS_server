from part3 import create_message, send_udp_message, find_ip_in_response

DNS_server, port = "1.1.1.1", 53
name_address_number_dict = {}
name_address_ip_dict = {}


def check_update_dicts(name_address):
    if name_address in name_address_ip_dict:
        if name_address_number_dict[name_address] >= 3:
            ip = name_address_ip_dict[name_address]
            print("get IP from cache")
        else:
            new_message = create_message("A", name_address, 1)
            response = send_udp_message(new_message, DNS_server, port)
            ip = find_ip_in_response(response, "A")
            name_address_ip_dict[name_address] = ip
            name_address_number_dict[name_address] = name_address_number_dict[name_address] + 1
            print("send request to DNS server")
    else:
        new_message = create_message("A", name_address, 1)
        response = send_udp_message(new_message, DNS_server, port)
        ip = find_ip_in_response(response, "A")
        name_address_ip_dict[name_address] = ip
        name_address_number_dict[name_address] = 1
        print("send request to DNS server")
    return ip


if __name__ == "__main__":
    flag = True
    while flag:
        print("*choose*\n1. Enter name address\n2. exit")
        command_input = input()
        if command_input == "2":
            flag = False
            print("exit")
            exit()
        else:
            print("Enter name address")
            name_address = input()
            ip = check_update_dicts(name_address)
            print("IP : ", ip)
