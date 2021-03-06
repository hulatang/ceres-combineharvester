import os
from pathlib import Path

# DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("CERES_ROOT", "~/.chia/mainnet"))).resolve()
# DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("CHIA_KEYS_ROOT", "~/.chia_keys"))).resolve()

DEFAULT_CERES_ROOT_PATH = Path(os.path.expanduser(os.getenv("CERES_ROOT", "~/.ceres/mainnet"))).resolve()
DEFAULT_CERES_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("CERES_KEYS_ROOT", "~/.ceres_keys"))).resolve()


DEFAULT_ROOT_PATH = DEFAULT_CERES_ROOT_PATH 
DEFAULT_KEYS_ROOT_PATH = DEFAULT_CERES_KEYS_ROOT_PATH

def get_coin_root_path(coin: str="chia"):
    # return Path(os.path.expanduser(os.getenv(f"{coin.upper()}_ROOT", f"~/.{coin.lower()}/mainnet"))).resolve()
    return Path(DEFAULT_CERES_ROOT_PATH / f"all_coins" / f".{coin}"/"mainnet")
