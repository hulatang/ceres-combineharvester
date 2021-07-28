from chia.server.introducer_peers import IntroducerPeers
from pathlib import Path
from chia.server.outbound_message import NodeType
from typing import Any, Dict, Optional, Tuple
from chia.server.server import ChiaServer


class ChiaHarvesterServer(ChiaServer):
    def __init__(
        self, port: int, 
        node: Any, 
        api: Any, 
        local_type: NodeType, 
        ping_interval: int, 
        network_id: str, 
        inbound_rate_limit_percent: int, 
        outbound_rate_limit_percent: int, 
        root_path: Path, 
        config: Dict, 
        private_ca_crt_key: Tuple[Path, Path], 
        chia_ca_crt_key: Tuple[Path, Path], 
        name: str, 
        introducer_peers: Optional[IntroducerPeers]
    ):
        super().__init__(port, node, api, local_type, ping_interval, network_id, inbound_rate_limit_percent, outbound_rate_limit_percent, root_path, config, private_ca_crt_key, chia_ca_crt_key, name=name, introducer_peers=introducer_peers)
