from ceres.cmds.init_funcs import init_by_coin
import click
from ceres.util.keychain import supports_keyring_passphrase


@click.command("init", short_help="Create or migrate the configuration")
@click.option("-n", "--name", type=str, help="Input coin name")
@click.option(
    "--create-certs",
    "-c",
    default=None,
    help="Create new SSL certificates based on CA in [directory]",
    type=click.Path(),
)
@click.option(
    "--fix-ssl-permissions",
    is_flag=True,
    help="Attempt to fix SSL certificate/key file permissions",
)
@click.option("--set-passphrase", "-s", is_flag=True, help="Protect your keyring with a passphrase")
@click.pass_context
def init_cmd(ctx: click.Context, name: str, create_certs: str, fix_ssl_permissions: bool, **kwargs):
    """
    Create a new configuration or migrate from previous versions to current

    \b
    Follow these steps to create new certificates for a remote harvester:
    - Make a copy of your Farming Machine CA directory: ~/.ceres/[version]/config/ssl/ca
    - Shut down all ceres daemon processes with `ceres stop all -d`
    - Run `ceres init -c [directory]` on your remote harvester,
      where [directory] is the the copy of your Farming Machine CA directory
    - Get more details on remote harvester on Ceres wiki:
      https://github.com/Ceres-Network/ceres-blockchain/wiki/Farming-on-many-machines
    """
    from pathlib import Path
    from .init_funcs import init
    from ceres.cmds.passphrase_funcs import initialize_passphrase

    set_passphrase = kwargs.get("set_passphrase")
    if set_passphrase:
        initialize_passphrase()

    # init(Path(create_certs) if create_certs is not None else None, ctx.obj["root_path"], fix_ssl_permissions)

    print(name, create_certs)
    # init(Path(create_certs) if name is not None and create_certs is not None else None, ctx.obj["root_path"])
    init_by_coin(name, Path(create_certs) if name is not None and create_certs is not None else None)



if not supports_keyring_passphrase():
    from ceres.cmds.passphrase_funcs import remove_passphrase_options_from_cmd

    # TODO: Remove once keyring passphrase management is rolled out to all platforms
    remove_passphrase_options_from_cmd(init_cmd)
    # from .init_funcs import init

if __name__ == "__main__":
    from .init_funcs import chia_init
    from ceres.util.default_root import DEFAULT_ROOT_PATH

    chia_init(DEFAULT_ROOT_PATH)
