
from ceres.util.path import mkdir
from ceres.util.config import initial_config_file
from pathlib import Path
import os

from pkg_resources import ensure_directory
from ceres.cmds.init_funcs import chia_init


def ceres_init(root_path: Path, coin: str="ceres"):
    chia_init(root_path, coin)

    create_ceres_coins_config(root_path)




def create_ceres_coins_config(root_path: Path, filename: str="coins-config.yaml"):
    ceres_all_coins_config_path = root_path / "config"
    ceres_all_coins_config_file = ceres_all_coins_config_path / f"coins_config"

    if ceres_all_coins_config_path.is_dir() and ceres_all_coins_config_file.exists():
        print(
            f"{filename} already exists"
        )
        return -1

    mkdir(ceres_all_coins_config_path.parent)

    ceres_all_coins_config_data = initial_config_file('ceres', filename)

    with open(ceres_all_coins_config_file, "w") as f:
        f.write(ceres_all_coins_config_data)







# def chia_init(root_path: Path, coin: str="ceres", *, should_check_keys: bool = True, fix_ssl_permissions: bool = False):
#     """
#     Standard first run initialization or migration steps. Handles config creation,
#     generation of SSL certs, and setting target addresses (via check_keys).

#     should_check_keys can be set to False to avoid blocking when accessing a passphrase
#     protected Keychain. When launching the daemon from the GUI, we want the GUI to
#     handle unlocking the keychain.
#     """
#     if os.environ.get("CERES_ROOT", None) is not None:
# # def chia_init(root_path: Path, coin: str = "ceres"):
#     # if os.environ.get(f"{coin}_ROOT", None) is not None:
#         print(
#             f"warning, your CERES_ROOT is set to {os.environ['CERES_ROOT']}. "
#             f"Please unset the environment variable and run ceres init again\n"
#             f"or manually migrate config.yaml"
#         )

#     print(f"{coin} directory {root_path}")
#     if root_path.is_dir() and Path(root_path / "config" / "config.yaml").exists():
#         # This is reached if CERES_ROOT is set, or if user has run ceres init twice
#         # before a new update.
#         if fix_ssl_permissions:
#             fix_ssl(root_path)
#         if should_check_keys:
#             check_keys(root_path)
#         print(f"{root_path} already exists, no migration action taken")
#         return -1

#     # create_default_chia_config(root_path)
#     # create_all_ssl(root_path)
#     # if fix_ssl_permissions:
#     #     fix_ssl(root_path)
#     # if should_check_keys:
#     #     check_keys(root_path)
#     # create_default_chia_config(root_path)
#     # create_all_ssl(root_path)
#     create_default_coin_config(coin, root_path)
#     create_all_ssl(coin, root_path)
#     check_keys(root_path)

#     if fix_ssl_permissions:
#         fix_ssl(root_path)
#     if should_check_keys:
#         check_keys(root_path)


#     print("")
#     print("To see your keys, run 'ceres keys show --show-mnemonic-seed'")

#     return 0
