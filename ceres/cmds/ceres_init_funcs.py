from ipaddress import IPv6Address, ip_address, IPv4Address
from logging import root
import shutil
from ceres.util.default_root import get_coin_root_path
from ceres.util.ceres_config import get_farmer_name, get_mining_coin_names
from ceres.util.path import mkdir
from ceres.util.config import initial_config_file, load_config
from pathlib import Path
import os

from pkg_resources import ensure_directory
from ceres.cmds.init_funcs import chia_init, copy_cert_files, create_all_ssl


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




def ceres_generate_ssl_for_all_coins(root_path: Path):
    mining_coins = get_mining_coin_names(root_path)

    all_ca_path = root_path / "all_ca"

    for coin in mining_coins:
        create_certs = all_ca_path / f"{coin}_ca" / "ca"

        if not create_certs.exists():
            print(f"{create_certs} does not exist")
            continue
        
        # TODO: should check ssl before continue

        coin_root_path = get_coin_root_path(coin)

        # chia_init()
        ca_dir: Path = coin_root_path / "config/ssl/ca"
        if ca_dir.exists():
            print(f"Deleting your OLD CA in {ca_dir}")
            shutil.rmtree(ca_dir)
        print(f"Copying your CA from {create_certs} to {ca_dir}")
        copy_cert_files(create_certs, ca_dir)
        create_all_ssl(coin, coin_root_path)







