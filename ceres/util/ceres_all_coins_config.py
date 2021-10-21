from ceres.util.ceres_config import get_mining_coin_names
from ceres.util.default_root import DEFAULT_CERES_ROOT_PATH, get_coin_root_path
from ceres.consensus.constants import ConsensusConstants
from ceres.consensus.all_coins_default_constants import *
import ceres.consensus.all_coins_default_constants
# from ceres.consensus.all_coins_default_constants import chia_default_constants
import os
from pathlib import Path
from ceres.util.config import load_config_cli


# COIN_NAMES = get_all_coin_names()
# COIN_NAMES = get_mining_coin_names()


COIN_NAMES = get_mining_coin_names()

def get_all_coins_config_constants(service_name: str, coin_names=COIN_NAMES):

    all_coins_configs = {}
    farmer_peer_port_map_coin = {}


    for coin in COIN_NAMES:
            # coin_root_path = Path(os.path.expanduser(os.getenv(f"{coin.upper()}_ROOT", f"~/.{coin.lower()}/mainnet"))).resolve()
            coin_root_path = get_coin_root_path(coin)
            coin_config = load_config_cli(coin_root_path, "config.yaml", service_name)

            farmer_peer_port = coin_config["farmer_peer"]["port"] 
            farmer_peer_port_map_coin[farmer_peer_port] = coin

            # connect_peers[coin] = [PeerInfo(coin_config["farmer_peer"]["host"], coin_config["farmer_peer"]["port"])]
            overrides = coin_config["network_overrides"]["constants"][coin_config["selected_network"]]
            coin_default_constant = get_coin_default_constants(coin)
            coin_updated_constants = coin_default_constant.replace_str_to_bytes(**overrides)
            all_coins_configs[coin] = {}
            all_coins_configs[coin]["config"] = coin_config
            all_coins_configs[coin]["constants"] = coin_updated_constants
    
    return all_coins_configs, farmer_peer_port_map_coin
        




def get_coin_default_constants(coin: str):
    import importlib


    pkg_name = f"ceres.consensus.all_coins_default_constants"
    coin_constant_file_name = f".{coin}_default_constants"
    coin_default_constant_module = importlib.import_module(coin_constant_file_name, pkg_name)
    testnet_kwargs = coin_default_constant_module.testnet_kwargs

    return ConsensusConstants(**testnet_kwargs)



def get_all_coins_default_constants(coin_names=COIN_NAMES):

    all_coins_default_constants = {}
    for coin in coin_names:
        all_coins_default_constants[coin] = get_coin_default_constants(coin)
    
    return all_coins_default_constants





# def get_mining_coin_names(root_path: Path=DEFAULT_CERES_ROOT_PATH):
#     farmer_configs = load_config_cli(root_path, filename="coins_config.yaml", sub_config="farmer_machine")

#     coin_names = []

#     for farmer in farmer_configs:
#         coins = farmer["coins"]
#         coin_names.append(coins)
    
#     return coin_names


