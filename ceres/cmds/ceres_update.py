import os
from pathlib import Path
import shutil
from typing import Any, Dict, List, Union
import click
from ceres.util.config import config_path_for_filename, flatten_properties, initial_config_file, save_config
from ceres.util.default_root import DEFAULT_CERES_ROOT_PATH
import sys
import yaml
from collections import OrderedDict



@click.command("update", short_help="Update ceres default configuration")
@click.option("--sub_configs", "-sub", default=["coin_names", "network_ids"], help="sub config to update")
@click.pass_context
def ceres_update_cmd(ctx: click.Context, sub_configs: List[str]):

    filename = f"coins_config.yaml"

    ceres_all_coins_config_path = DEFAULT_CERES_ROOT_PATH / "config"
    ceres_all_coins_config_file = ceres_all_coins_config_path / filename

    if not ceres_all_coins_config_file.exists():
        print("coins config file not exists, run ceres init first.")
        return -1
    
    default_coins_config_filename = "coins-config.yaml"

    ceres_all_coins_config_str = initial_config_file('ceres', default_coins_config_filename)
    ceres_all_coins_config_data : Dict = yaml.safe_load(ceres_all_coins_config_str)

    reserved_lines = []

    with open(ceres_all_coins_config_file, "r") as f_coins_config:
        # lines = f_coins_config.readlines()
        # f_coins_config.write('')
        for l in f_coins_config:
            if "coin_names" in l:
                break
            reserved_lines.append(l)
        
    with open(ceres_all_coins_config_file, "w"): pass


    with open(ceres_all_coins_config_file, "a") as f_new_coins_config:
        f_new_coins_config.writelines(reserved_lines)


    

    
    with open(ceres_all_coins_config_file, "a") as f_coins_config:
        for sub_config in sub_configs:
            # f_coins_config.write(sub_config + ":" + os.linesep)
            # config_str = get_config_str(ceres_all_coins_config_data, sub_config)
            sub_data = ceres_all_coins_config_data.get(sub_config)
            data = {}
            data[sub_config] = sub_data

            config_str = yaml.dump(data)
            f_coins_config.write(config_str)
    


    print(f"Done ceres updating.")






    # ordered_config = OrderedDict()
    # config = {}

    # for sub_config in ceres_all_coins_config_data.keys():
    #     if sub_config in sub_configs:
    #         # ordered_config[sub_config] = ceres_all_coins_config_data[sub_config]
    #         config[sub_config] = ceres_all_coins_config_data[sub_config]
    #         continue

    #     default_data = load_user_config(filename, sub_config)

    #     # ceres_all_coins_config_data.update({sub_config, default_data})
    #     # ceres_all_coins_config_data[sub_config] = None
    #     # ceres_all_coins_config_data[sub_config] = default_data
    #     # ordered_config[sub_config] = default_data
    #     config[sub_config] = default_data
    #     print(f"updated {sub_config}")
    
    # flatterned_props = flatten_properties(ceres_all_coins_config_data)

    # with open(ceres_all_coins_config_file, "w") as f:
        # f.write(flatterned_props)

    # save_config(DEFAULT_CERES_ROOT_PATH, filename, ceres_all_coins_config_data)
    # save_config(DEFAULT_CERES_ROOT_PATH, filename, ordered_config)
    # save_config_keep_order(DEFAULT_CERES_ROOT_PATH, filename, config)

    
    

def get_config_str(config_data: Dict, sub_config: str):
    sub_data = config_data.get(sub_config)

    return yaml.dump(sub_data)



def save_config_keep_order(root_path: Path, filename: Union[str, Path], config_data: Any):
    path = config_path_for_filename(root_path, filename)
    with open(path.with_suffix("." + str(os.getpid())), "w") as f:
        yaml.safe_dump(config_data, f, default_flow_style=False, sort_keys=False)
    shutil.move(str(path.with_suffix("." + str(os.getpid()))), path)






def load_user_config(config: str, sub_config: str):
    user_config_path = DEFAULT_CERES_ROOT_PATH / "config"
    config_file_path = user_config_path / config

    if not config_file_path.is_file():
        raise ValueError(f"{config_file_path} not found")
        sys.exit(-1)
    
    r = yaml.safe_load(open(config_file_path, "r"))

    if sub_config is not None:
        r = r.get(sub_config)
    
    return r

    
    

