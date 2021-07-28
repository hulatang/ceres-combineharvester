from chia.cmds.init_funcs import init_by_coin
import click


@click.command("init", short_help="Create or migrate the configuration")
@click.option("-n", "--name", type=str, help="Input coin name")
@click.option(
    "--create-certs",
    "-c",
    default=None,
    help="Create new SSL certificates based on CA in [directory]",
    type=click.Path(),
)
@click.pass_context
def init_cmd(ctx: click.Context, name: str, create_certs: str):
    """
    Create a new configuration or migrate from previous versions to current

    \b
    Follow these steps to create new certificates for a remote harvester:
    - Make a copy of your Farming Machine CA directory: ~/.chia/[version]/config/ssl/ca
    - Shut down all chia daemon processes with `chia stop all -d`
    - Run `chia init -c [directory]` on your remote harvester,
      where [directory] is the the copy of your Farming Machine CA directory
    - Get more details on remote harvester on Chia wiki:
      https://github.com/Chia-Network/chia-blockchain/wiki/Farming-on-many-machines
    """
    from pathlib import Path
    # from .init_funcs import init

    print(name, create_certs)
    # init(Path(create_certs) if name is not None and create_certs is not None else None, ctx.obj["root_path"])
    init_by_coin(name, Path(create_certs) if name is not None and create_certs is not None else None)


if __name__ == "__main__":
    from .init_funcs import chia_init
    from chia.util.default_root import DEFAULT_ROOT_PATH

    chia_init(DEFAULT_ROOT_PATH)
