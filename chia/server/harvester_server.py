import asyncio
from chia.util.config import get_all_coin_config, load_config_cli
from chia.util.default_root import get_coin_root_path
from chia.server.ssl_context import chia_ssl_ca_paths, private_ssl_ca_paths, private_ssl_paths
import traceback

from aiohttp.http_websocket import WSCloseCode
from aiohttp import client_exceptions
from aiohttp.client import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ServerDisconnectedError
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from chia.server.ws_connection import WSChiaConnection
import time
from chia.types.peer_info import PeerInfo
from chia.server.introducer_peers import IntroducerPeers
from pathlib import Path
from chia.server.outbound_message import NodeType
from typing import Any, Callable, Dict, Optional, Tuple
from chia.server.server import ChiaServer, ssl_context_for_client
from ipaddress import IPv6Address, ip_address, ip_network, IPv4Network, IPv6Network
from cryptography import x509
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.util.errors import Err, ProtocolError
from chia.protocols.shared_protocol import protocol_version

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
        name: str = None, 
        introducer_peers: Optional[IntroducerPeers] = None,
    ):
        super().__init__(port, node, api, local_type, ping_interval, network_id, inbound_rate_limit_percent, outbound_rate_limit_percent, root_path, config, private_ca_crt_key, chia_ca_crt_key, name=name, introducer_peers=introducer_peers)



    async def start_client(
        self,
        coin: str,
        target_node: PeerInfo,
        on_connect: Callable = None,
        auth: bool = False,
        is_feeler: bool = False,
    ) -> bool:
        """
        Tries to connect to the target node, adding one connection into the pipeline, if successful.
        An on connect method can also be specified, and this will be saved into the instance variables.
        """
        if self.is_duplicate_or_self_connection(target_node):
            return False

        if target_node.host in self.banned_peers and time.time() < self.banned_peers[target_node.host]:
            self.log.warning(f"Peer {target_node.host} is still banned, not connecting to it")
            return False
        
        coin_root_path = get_coin_root_path(coin)
        coin_config = load_config_cli(coin_root_path, "config.yaml", "harvester")

        _private_cert_path, _private_key_path = private_ssl_paths(coin_root_path, coin_config)
        ca_private_crt_path, ca_private_key_path = private_ssl_ca_paths(coin_root_path, coin_config)
        
        # private_ca_crt, private_ca_key = private_ssl_ca_paths(coin_root_path, self.config)
        # chia_ca_crt, chia_ca_key = chia_ssl_ca_paths(coin, coin_root_path, self.config)


        if auth:
            ssl_context = ssl_context_for_client(
                ca_private_crt_path, ca_private_key_path, _private_cert_path, _private_key_path
                # self.ca_private_crt_path, self.ca_private_key_path, self._private_cert_path, self._private_key_path
            )
        else:
            ssl_context = ssl_context_for_client(
                self.chia_ca_crt_path, self.chia_ca_key_path, self.p2p_crt_path, self.p2p_key_path
            )
        session = None
        connection: Optional[WSChiaConnection] = None
        try:
            timeout = ClientTimeout(total=30)
            session = ClientSession(timeout=timeout)

            try:
                if type(ip_address(target_node.host)) is IPv6Address:
                    target_node = PeerInfo(f"[{target_node.host}]", target_node.port)
            except ValueError:
                pass

            url = f"wss://{target_node.host}:{target_node.port}/ws"
            self.log.debug(f"Connecting: {url}, Peer info: {target_node}")
            try:
                ws = await session.ws_connect(
                    url, autoclose=True, autoping=True, heartbeat=60, ssl=ssl_context, max_msg_size=50 * 1024 * 1024
                )
            except ServerDisconnectedError:
                self.log.debug(f"Server disconnected error connecting to {url}. Perhaps we are banned by the peer.")
                await session.close()
                return False
            except asyncio.TimeoutError:
                self.log.debug(f"Timeout error connecting to {url}")
                await session.close()
                return False
            if ws is not None:
                assert ws._response.connection is not None and ws._response.connection.transport is not None
                transport = ws._response.connection.transport  # type: ignore
                cert_bytes = transport._ssl_protocol._extra["ssl_object"].getpeercert(True)  # type: ignore
                der_cert = x509.load_der_x509_certificate(cert_bytes, default_backend())
                peer_id = bytes32(der_cert.fingerprint(hashes.SHA256()))
                if peer_id == self.node_id:
                    raise RuntimeError(f"Trying to connect to a peer ({target_node}) with the same peer_id: {peer_id}")

                connection = WSChiaConnection(
                    self._local_type,
                    ws,
                    # self._port,
                    target_node.port,
                    self.log,
                    True,
                    False,
                    target_node.host,
                    self.incoming_messages,
                    self.connection_closed,
                    peer_id,
                    self._inbound_rate_limit_percent,
                    self._outbound_rate_limit_percent,
                    session=session,
                )

                all_coin_config = get_all_coin_config()

                network_id = all_coin_config[coin]["network_id"]

                handshake = await connection.perform_handshake(
                    # self._network_id,
                    network_id,
                    protocol_version,
                    # self._port,
                    target_node.port,
                    self._local_type,
                )
                assert handshake is True
                await self.connection_added(connection, on_connect)
                connection_type_str = ""
                if connection.connection_type is not None:
                    connection_type_str = connection.connection_type.name.lower()
                self.log.info(f"Connected with {connection_type_str} {target_node}")
                if is_feeler:
                    asyncio.create_task(connection.close())
                return True
            else:
                await session.close()
                return False
        except client_exceptions.ClientConnectorError as e:
            self.log.info(f"{e}")
        except ProtocolError as e:
            if connection is not None:
                await connection.close(self.invalid_protocol_ban_seconds, WSCloseCode.PROTOCOL_ERROR, e.code)
            if e.code == Err.INVALID_HANDSHAKE:
                self.log.warning(f"Invalid handshake with peer {target_node}. Maybe the peer is running old software.")
            elif e.code == Err.INCOMPATIBLE_NETWORK_ID:
                self.log.warning("Incompatible network ID. Maybe the peer is on another network")
            elif e.code == Err.SELF_CONNECTION:
                pass
            else:
                error_stack = traceback.format_exc()
                self.log.error(f"Exception {e}, exception Stack: {error_stack}")
        except Exception as e:
            if connection is not None:
                await connection.close(self.invalid_protocol_ban_seconds, WSCloseCode.PROTOCOL_ERROR, Err.UNKNOWN)
            error_stack = traceback.format_exc()
            self.log.error(f"Exception {e}, exception Stack: {error_stack}")

        if session is not None:
            await session.close()

        return False