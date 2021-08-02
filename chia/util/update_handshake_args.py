from chia.protocols.shared_protocol import Handshake
from chia.util.config import get_all_coin_config
from typing import List, Tuple
from chia.util.ints import uint16, uint8





def update_handshake_args(coin: str, **handshake_args):
    coin_config = get_all_coin_config()[coin]
    for arg, value in coin_config.items():
        handshake_args[arg] = value
    

    return handshake_args



