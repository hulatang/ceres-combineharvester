import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("CHIA_ROOT", "~/.chia/mainnet"))).resolve()



def get_coin_root_path(coin: str="chia"):
    return Path(os.path.expanduser(os.getenv(f"{coin.upper()}_ROOT", f"~/.{coin.lower()}/mainnet"))).resolve()