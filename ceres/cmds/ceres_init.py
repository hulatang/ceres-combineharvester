from ceres.cmds.ceres_init_funcs import ceres_init
import click





@click.command("init", short_help="Create or migrate the configuration")
# @click.option("-n", "--name", type=str, default="ceres", help="Input coin name")
# @click.option(
#     "--create-certs",
#     "-c",
#     default=None,
#     help="Create new SSL certificates based on CA in [directory]",
#     type=click.Path(),
# )
@click.option("--coins", "-c", is_flag=True, help="Init all coins structure")
@click.pass_context
def ceres_init_cmd(ctx: click.Context, coins: bool, **kwargs):
    print('ceres init cmd')
    ceres_init(ctx.obj["root_path"], init_coins=coins)