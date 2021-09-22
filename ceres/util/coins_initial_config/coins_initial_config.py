from pathlib import Path
from typing import Union
import pkg_resources



def initial_coin_config_file(coin: str, filename: Union[str, Path]) -> str:
    return pkg_resources.resource_string(__name__, f"{coin}-initial-{filename}").decode()