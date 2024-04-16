import re
import ipaddress

############################## Validation Function #############################
def is_valid_ip(ip):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    octets = ip.split('.')
    for octet in octets:
        if not (0 <= int(octet) <= 255):
            return False
        if len(octet) > 1 and octet.startswith('0'):
            return False
    return True

############################### CIDR Validation ################################
def is_valid_cidr(cidr):
    if cidr.isdigit():
        cidr_int = int(cidr)
        return 0 <= cidr_int <= 32
    else:
        return False

############################ Subnet Mask Calculation ###########################
def calculate_subnet_mask(cidr):
    return str(ipaddress.IPv4Network((0, cidr)).netmask)

############################### Network Class ##################################
def get_network_class(ip):
    first_octet = int(ip.split('.')[0])
    if first_octet < 128:
        return 8  # Class A
    elif first_octet < 192:
        return 16  # Class B
    elif first_octet < 224:
        return 24  # Class C
    elif first_octet < 240:
        return 28  # Class D
    else:
        return 32  # Class E

############################### Subnet Calculation #############################
def calculate_subnets(ip, cidr, partition_type, number):

    network = ipaddress.IPv4Network(f"{ip}/{cidr}", strict=False)
    
    if partition_type == "hosts":
        # Calculate the new prefix length for hosts
        number = int(number)
        new_prefix = 32 - (number + 2).bit_length()
        subnets = list(network.subnets(new_prefix=new_prefix))
    else:  # Partition by subnets
        number = int(number)
        # Calculate new prefix length based on the specified number of subnets
        prefixlen_diff = number.bit_length()
        #network.subnets(prefixlen_diff=) will generate a list of all possible subnets 
        subnets = list(network.subnets(prefixlen_diff=prefixlen_diff))
    
    print("\nOUTPUT")
    print("Subnet Mask:", str(network.netmask))
    print("CIDR:", f"/{network.prefixlen}")
    print("Number of Hosts:", network.num_addresses - 2)
    print("Number of Subnets:", len(subnets))
    print("First Two Subnets:", subnets[:2])
    print("Last Two Subnets:", subnets[-2:])

    
################################ Main Function #################################
def main():
    ip = input("Enter an IP address: ")
    if not is_valid_ip(ip):
        print("Invalid IP address.")
        return
    
    cidr_input = input("Enter a CIDR (optional): ")
    if cidr_input and is_valid_cidr(cidr_input):
        cidr = int(cidr_input)
    else:
        cidr = get_network_class(ip)
    
    partition_type = input("Partition by number of hosts or subnets? (hosts/subnets): ")
    if partition_type not in ["hosts", "subnets"]:
        print("Invalid partition type.")
        return
    
    number_input = input(f"Enter number of {partition_type}: ")
    if not number_input.isdigit() or int(number_input) < 1:
        print("Invalid number.")
        return
    
    calculate_subnets(ip, cidr, partition_type, number_input)
    

if __name__ == "__main__":
    main()
