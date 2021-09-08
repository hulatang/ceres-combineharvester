import asyncio
from ceres.server.ssl_context import chia_ssl_ca_paths, private_ssl_ca_paths
from ceres.util.chia_logging import initialize_logging
from ceres.util.config import load_config, load_config_cli
from ceres.server.harvester_server import ChiaHarvesterServer
from ceres.util.ints import uint16
from ceres.server.upnp import UPnP
from ceres.types.peer_info import PeerInfo
from ceres.server.outbound_message import NodeType
from typing import Any, Callable, Dict, List, Optional, Tuple
from ceres.server.start_service import Service
from .reconnect_task import start_reconnect_task
from ceres.rpc.rpc_server import start_rpc_server
try:
    import uvloop
except ImportError:
    uvloop = None


class HarvesterService(Service):
    def __init__(
        self, 
        root_path, 
        node: Any, 
        peer_api: Any, 
        node_type: NodeType, 
        advertised_port: int, 
        service_name: str, 
        network_id: str, 
        upnp_ports: List[int] = [], 
        server_listen_ports: List[int] = [], 
        # connect_peers: List[PeerInfo], 
        connect_peers: Dict = [],
        auth_connect_peers: bool = True, 
        on_connect_callback: Optional[Callable] = None, 
        rpc_info: Optional[Tuple[type, int]] = None, 
        parse_cli_args = True, 
        connect_to_daemon = True,
    ) -> None:
        super().__init__(root_path, node, peer_api, node_type, advertised_port, service_name, network_id, upnp_ports=upnp_ports, server_listen_ports=server_listen_ports, connect_peers=[], auth_connect_peers=auth_connect_peers, on_connect_callback=on_connect_callback, rpc_info=rpc_info, parse_cli_args=parse_cli_args, connect_to_daemon=connect_to_daemon)
        self._connect_peers = connect_peers
        if parse_cli_args:
            service_config = load_config_cli(root_path, "config.yaml", service_name)
        else:
            service_config = load_config(root_path, "config.yaml", service_name)
        initialize_logging(service_name, service_config["logging"], root_path)

        ping_interval = self.config.get("ping_interval")
        inbound_rlp = self.config.get("inbound_rate_limit_percent")
        outbound_rlp = self.config.get("outbound_rate_limit_percent")
        private_ca_crt, private_ca_key = private_ssl_ca_paths(root_path, self.config)
        chia_ca_crt, chia_ca_key = chia_ssl_ca_paths(root_path, self.config)
        self._server = ChiaHarvesterServer(
            advertised_port,
            node,
            peer_api,
            node_type,
            ping_interval,
            network_id,
            inbound_rlp,
            outbound_rlp,
            root_path,
            service_config,
            (private_ca_crt, private_ca_key),
            (chia_ca_crt, chia_ca_key),
            name=f"{service_name}_server",
        )


    async def start(self, **kwargs) -> None:
        # we include `kwargs` as a hack for the wallet, which for some
        # reason allows parameters to `_start`. This is serious BRAIN DAMAGE,
        # and should be fixed at some point.
        # TODO: move those parameters to `__init__`
        if self._did_start:
            return None

        assert self.self_hostname is not None
        assert self.daemon_port is not None

        self._did_start = True

        self._enable_signals()

        await self._node._start(**kwargs)

        for port in self._upnp_ports:
            if self.upnp is None:
                self.upnp = UPnP()

            self.upnp.remap(port)

        await self._server.start_server(self._on_connect_callback)

        self._reconnect_tasks = [
            start_reconnect_task(self._server, coin, peer[0], self._log, self._auth_connect_peers) for coin, peer in self._connect_peers.items()
            # start_reconnect_task(self._server, _, self._log, self._auth_connect_peers) for _ in self._connect_peers
        ]
        self._log.info(f"Started {self._service_name} service on network_id: {self._network_id}")

        self._rpc_close_task = None
        if self._rpc_info:
            rpc_api, rpc_port = self._rpc_info
            self._rpc_task = asyncio.create_task(
                start_rpc_server(
                    rpc_api(self._node),
                    self.self_hostname,
                    self.daemon_port,
                    uint16(rpc_port),
                    self.stop,
                    self.root_path,
                    self.config,
                    self._connect_to_daemon,
                )
            )


async def async_run_harvester_service(*args, **kwargs) -> None:
    # service = Service(*args, **kwargs)
    service = HarvesterService(*args, **kwargs)
    return await service.run()


def run_harvester_service(*args, **kwargs) -> None:
    if uvloop is not None:
        uvloop.install()
    return asyncio.run(async_run_harvester_service(*args, **kwargs))
