from ceres.util.default_root import DEFAULT_CERES_ROOT_PATH, get_coin_root_path
from ceres.util.config import load_config, load_config_cli
from pathlib import Path
from ipaddress import IPv6Address, ip_address, IPv4Address



# TODO: should check if coin name is supported
def get_mining_coin_names(root_path: Path=DEFAULT_CERES_ROOT_PATH):
    farmer_configs = load_config(root_path, filename="coins_config.yaml", sub_config="farmer_machine")

    coin_names = []

    for farmer in farmer_configs:
        coins = farmer["farmer_peer"]["coins"]
        coin_names.extend(coins)
    
    return coin_names


def get_valid_coin_names(root_path: Path=DEFAULT_CERES_ROOT_PATH):
    return load_config(root_path, filename="coins_config.yaml", sub_config="coin_names")



def get_coin_config(coin: str, subconfig: str):
    coin_root_path = get_coin_root_path(coin)
    config = load_config(coin_root_path, "config.yaml", subconfig)

    return config



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