from part3 import send_udp_message, create_message, find_ip_in_response
import csv
import pandas


def read_from_csv(file_name):
    name_addresses_arr = []
    name_addresses = pandas.read_csv(file_name)
    for name_address in name_addresses.itertuples():
        name_addresses_arr.append(name_address[1])

    return name_addresses_arr


def find_ip_from_arr(name_addresses_arr):
    ip_arr = []
    for name_address in name_addresses_arr:
        message = create_message("A", name_address, 1)
        DNS_server, port = "1.1.1.1", 53
        response = send_udp_message(message, DNS_server, port)
        ip_arr.append([str(find_ip_in_response(response, "A"))])

    return ip_arr


def write_csv(file_name, result_ips):
    with open(r'' + file_name, 'a') as file_write:
        writer = csv.writer(file_write)
        writer.writerows(result_ips)


if __name__ == "__main__":
    # extra point 1
    file_name = "name_address.csv"
    name_addresses_arr = read_from_csv(file_name)
    ip_arr = find_ip_from_arr(name_addresses_arr)
    print(ip_arr)
    write_csv("result_ips.csv", ip_arr)
