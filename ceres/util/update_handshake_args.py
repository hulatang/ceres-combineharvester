from ceres.util.default_root import DEFAULT_CERES_ROOT_PATH
from ceres.util.config import load_config
from ceres.util.ceres_all_coins_config import get_all_coins_config_constants
from ceres.protocols.shared_protocol import Handshake
# from ceres.util.config import get_all_coin_config
from typing import List, Tuple
from ceres.util.ints import uint16, uint8





def update_handshake_args(coin: str, **handshake_args):
    # coin_config = get_all_coins_config_constants()[coin]
    network_ids = load_config(DEFAULT_CERES_ROOT_PATH, filename="coins_config.yaml", sub_config="network_ids")

    for arg, value in network_ids[coin].items():
        handshake_args[arg] = value
    

    return handshake_args



