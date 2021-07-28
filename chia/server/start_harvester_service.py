import asyncio
from chia.util.ints import uint16
from chia.server.upnp import UPnP
from chia.types.peer_info import PeerInfo
from chia.server.outbound_message import NodeType
from typing import Any, Callable, List, Optional, Tuple
from chia.server.start_service import Service
from .reconnect_task import start_reconnect_task
from chia.rpc.rpc_server import start_rpc_server


class HarvesterService(Service):
    def __init__(
        self, root_path, 
        node: Any, 
        peer_api: Any, 
        node_type: NodeType, 
        advertised_port: int, 
        service_name: str, 
        network_id: str, 
        upnp_ports: List[int], 
        server_listen_ports: List[int], 
        connect_peers: List[PeerInfo], 
        auth_connect_peers: bool, 
        on_connect_callback: Optional[Callable], 
        rpc_info: Optional[Tuple[type, int]], 
        parse_cli_args, connect_to_daemon
    ) -> None:
        super().__init__(root_path, node, peer_api, node_type, advertised_port, service_name, network_id, upnp_ports=upnp_ports, server_listen_ports=server_listen_ports, connect_peers=connect_peers, auth_connect_peers=auth_connect_peers, on_connect_callback=on_connect_callback, rpc_info=rpc_info, parse_cli_args=parse_cli_args, connect_to_daemon=connect_to_daemon)


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
            start_reconnect_task(self._server, _, self._log, self._auth_connect_peers) for _ in self._connect_peers
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