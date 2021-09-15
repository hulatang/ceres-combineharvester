from ceres.consensus.constants import ConsensusConstants
import os
import pathlib
from ceres.util.config import get_all_coin_names, load_config_cli


COIN_NAMES = get_all_coin_names()

def get_all_coins_config(service_name: str, coin_names=COIN_NAMES):

    all_coins_configs = {}


    for coin in COIN_NAMES:
            coin_root_path = pathlib.Path(os.path.expanduser(os.getenv(f"{coin.upper()}_ROOT", f"~/.{coin.lower()}/mainnet"))).resolve()
            coin_config = load_config_cli(coin_root_path, "config.yaml", service_name)
            # connect_peers[coin] = [PeerInfo(coin_config["farmer_peer"]["host"], coin_config["farmer_peer"]["port"])]
            overrides = coin_config["network_overrides"]["constants"][coin_config["selected_network"]]
            coin_updated_constants = ConsensusConstants.replace_str_to_bytes(**overrides)
            all_coins_configs[coin] = {}
            all_coins_configs[coin]["config"] = coin_config
            all_coins_configs[coin]["constants"] = coin_updated_constants
    
    return all_coins_configs
        



def get_all_coins_default_constants(coin_names=COIN_NAMES):
    import importlib

    pkg_name = f"ceres.consensus.all_coins_default_constants"
    all_coins_default_constants = {}
    for coin in coin_names:
        coin_constant_file_name = f".{coin}_default_constants"
        coin_default_constant = importlib.import_module(coin_constant_file_name, pkg_name)
        all_coins_default_constants[coin] = coin_default_constant.DEFAULT_CONSTANTS
    
    return all_coins_default_constants
