from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "cere_harvester cere_timelord_launcher cere_timelord cere_farmer cere_full_node cere_wallet".split(),
    "node": "cere_full_node".split(),
    "harvester": "ceres_harvester".split(),
    "farmer": "cere_harvester cere_farmer cere_full_node cere_wallet".split(),
    "farmer-no-wallet": "cere_harvester cere_farmer cere_full_node".split(),
    "farmer-only": "cere_farmer".split(),
    "timelord": "cere_timelord_launcher cere_timelord cere_full_node".split(),
    "timelord-only": "cere_timelord".split(),
    "timelord-launcher-only": "cere_timelord_launcher".split(),
    "wallet": "cere_wallet cere_full_node".split(),
    "wallet-only": "cere_wallet".split(),
    "introducer": "cere_introducer".split(),
    "simulator": "cere_full_node_simulator".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
