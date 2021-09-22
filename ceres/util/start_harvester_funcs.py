from ceres.server.server import ssl_context_for_client
from ceres.server.ssl_context import private_ssl_ca_paths, private_ssl_paths
from ceres.types.peer_info import PeerInfo
from ceres.util.default_root import get_coin_root_path
from ceres.util.config import load_config, load_config_cli
from typing import Dict
from ceres.util.ceres_config import get_coin_config, get_mining_coin_names
from ceres.server.server import ssl_context_for_client

def get_harvester_connect_peers(root_path) -> Dict:

    connect_peers = {}

    farmer_configs = load_config(root_path, filename="coins_config.yaml", sub_config="farmer_machine")
    for farmer in farmer_configs:
        coins = farmer["farmer_peer"]["coins"]

        farmer_peer = farmer["farmer_peer"]
        farmer_ip = farmer_peer["address"]

        # TODO: should check duplicated coin name
        for coin in coins:
            coin_root_path = get_coin_root_path(coin)
            coin_harvester_config = get_coin_config(coin, "harvester")
            farmer_port = coin_harvester_config["farmer_peer"]["port"]
            peer_info = PeerInfo(farmer_ip, farmer_port)

            connect_peers[coin] = peer_info
    
    return connect_peers


def ssl_context_for_coin(coin: str):

    coin_root_path = get_coin_root_path(coin)
    coin_config = get_coin_config(coin, "harvester")

    _private_cert_path, _private_key_path = private_ssl_paths(coin_root_path, coin_config)
    ca_private_crt_path, ca_private_key_path = private_ssl_ca_paths(coin_root_path, coin_config)

    ssl_context = ssl_context_for_client(
        ca_private_crt_path, ca_private_key_path, _private_cert_path, _private_key_path
    )

    return ssl_context