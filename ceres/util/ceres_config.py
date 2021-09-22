from ceres.util.default_root import DEFAULT_CERES_ROOT_PATH
from ceres.util.config import load_config
from pathlib import Path
from ipaddress import IPv6Address, ip_address, IPv4Address



def get_mining_coin_names(root_path: Path=DEFAULT_CERES_ROOT_PATH):
    farmer_configs = load_config(root_path, filename="coins_config.yaml", sub_config="farmer_machine")

    coin_names = []

    for farmer in farmer_configs:
        coins = farmer["farmer_peer"]["coins"]
        coin_names.extend(coins)
    
    return coin_names



def get_farmer_name(address):
    farmer_name = "localhost"

    if not address == "localhost":
        # if not type(ip_address(address)) is IPv4Address or not type(ip_address(address)) is IPv6Address:
        address_type = type(ip_address(address))
        if address_type is IPv4Address or address_type is IPv6Address:
            farmer_name = address.split(".")[-1]
        else:
            print("Farmer peer address should be localhost, ipv4 or ipv6.")
            raise TypeError("Farmer peer address should be localhost, ipv4 or ipv6.")

    farmer_name = farmer_name + "_ca"

    return farmer_name