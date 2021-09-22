from ceres.util.default_root import DEFAULT_CERES_ROOT_PATH
from ceres.util.config import load_config
from pathlib import Path




def get_mining_coin_names(root_path: Path=DEFAULT_CERES_ROOT_PATH):
    farmer_configs = load_config(root_path, filename="coins_config.yaml", sub_config="farmer_machine")

    coin_names = []

    for farmer in farmer_configs:
        coins = farmer["farmer_peer"]["coins"]
        coin_names.extend(coins)
    
    return coin_names

