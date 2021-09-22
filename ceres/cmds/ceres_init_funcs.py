from ipaddress import IPv6Address, ip_address, IPv4Address
from ceres.util.default_root import get_coin_root_path
from ceres.util.ceres_config import get_farmer_name, get_mining_coin_names
from ceres.util.path import mkdir
from ceres.util.config import initial_config_file, load_config
from pathlib import Path
import os

from pkg_resources import ensure_directory
from ceres.cmds.init_funcs import chia_init


def ceres_init(root_path: Path, coin: str="ceres", init_coins=False):
    if not init_coins:
        chia_init(root_path, coin)
        create_ceres_coins_config(root_path)
    else:
        create_ceres_all_ca_path(root_path)

        coins_config_file = root_path / "config" / "coins_config.yaml"
        if not coins_config_file.exists():
            print(f"coins_config.yaml NOT Found, run ceres init first")
        else:
            create_config_for_every_coins(root_path)



def create_config_for_every_coins(root_path: Path):
    coins_config_file = root_path / "config" / "coins_config.yaml"
    if not coins_config_file.exists():
        print(f"coins_config.yaml NOT Found, run ceres init first")
    else:
        all_coins_root_path = root_path / "all_coins"

        if not all_coins_root_path.exists():
            mkdir(all_coins_root_path)

        coin_names = get_mining_coin_names(root_path)
        for coin in coin_names:
            coin_root_path = get_coin_root_path(coin)
            chia_init(coin_root_path, coin)



def create_ceres_all_ca_path(root_path: Path):
    all_ca_path = root_path / "all_ca"
    if not all_ca_path.exists():
        mkdir(all_ca_path)
    
    coin_names = get_mining_coin_names(root_path)

    for coin in coin_names:
        ca_path = all_ca_path / f"{coin}_ca"
        if not ca_path.exists():
            mkdir(ca_path)
        print(f"Created ca directory: {ca_path}")


    # farmer_configs = load_config(root_path, filename="coins_config.yaml", sub_config="farmer_machine")
    # for farmer_peer in farmer_configs:
    #     farmer = farmer_peer["farmer_peer"]
    #     address = farmer["address"]

    #     farmer_name = get_farmer_name(address)

    #     # farmer_name = "localhost"

    #     # if not address == "localhost":
    #     #     # if not type(ip_address(address)) is IPv4Address or not type(ip_address(address)) is IPv6Address:
    #     #     address_type = type(ip_address(address))
    #     #     if not address_type is IPv4Address:
    #     #         print("Farmer peer address should be localhost, ipv4 or ipv6.")
    #     #         raise TypeError("Farmer peer address should be localhost, ipv4 or ipv6.")
    #     #     else:
    #     #         farmer_name = address.split(".")[-1]
    #     # farmer_name = farmer_name + "_ca"
        
    #     farmer_ca_path = all_ca_path / farmer_name

        # if not farmer_ca_path.exists():
        #     mkdir(farmer_ca_path)
        #     print(f"Created ca directory: {farmer_name}")
            
            















def create_ceres_coins_config(root_path: Path, filename: str="coins-config.yaml"):
    ceres_all_coins_config_path = root_path / "config"
    ceres_all_coins_config_file = ceres_all_coins_config_path / f"coins_config.yaml"

    if ceres_all_coins_config_path.is_dir() and ceres_all_coins_config_file.exists():
        print(
            f"{filename} already exists"
        )
        return -1

    mkdir(ceres_all_coins_config_path.parent)

    ceres_all_coins_config_data = initial_config_file('ceres', filename)

    with open(ceres_all_coins_config_file, "w") as f:
        f.write(ceres_all_coins_config_data)







# def chia_init(root_path: Path, coin: str="ceres", *, should_check_keys: bool = True, fix_ssl_permissions: bool = False):
#     """
#     Standard first run initialization or migration steps. Handles config creation,
#     generation of SSL certs, and setting target addresses (via check_keys).

#     should_check_keys can be set to False to avoid blocking when accessing a passphrase
#     protected Keychain. When launching the daemon from the GUI, we want the GUI to
#     handle unlocking the keychain.
#     """
#     if os.environ.get("CERES_ROOT", None) is not None:
# # def chia_init(root_path: Path, coin: str = "ceres"):
#     # if os.environ.get(f"{coin}_ROOT", None) is not None:
#         print(
#             f"warning, your CERES_ROOT is set to {os.environ['CERES_ROOT']}. "
#             f"Please unset the environment variable and run ceres init again\n"
#             f"or manually migrate config.yaml"
#         )

#     print(f"{coin} directory {root_path}")
#     if root_path.is_dir() and Path(root_path / "config" / "config.yaml").exists():
#         # This is reached if CERES_ROOT is set, or if user has run ceres init twice
#         # before a new update.
#         if fix_ssl_permissions:
#             fix_ssl(root_path)
#         if should_check_keys:
#             check_keys(root_path)
#         print(f"{root_path} already exists, no migration action taken")
#         return -1

#     # create_default_chia_config(root_path)
#     # create_all_ssl(root_path)
#     # if fix_ssl_permissions:
#     #     fix_ssl(root_path)
#     # if should_check_keys:
#     #     check_keys(root_path)
#     # create_default_chia_config(root_path)
#     # create_all_ssl(root_path)
#     create_default_coin_config(coin, root_path)
#     create_all_ssl(coin, root_path)
#     check_keys(root_path)

#     if fix_ssl_permissions:
#         fix_ssl(root_path)
#     if should_check_keys:
#         check_keys(root_path)


#     print("")
#     print("To see your keys, run 'ceres keys show --show-mnemonic-seed'")

#     return 0
