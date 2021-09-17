import click





@click.command("init", short_help="Create or migrate the configuration")
@click.option("-n", "--name", type=str, default="ceres", help="Input coin name")
@click.option(
    "--create-certs",
    "-c",
    default=None,
    help="Create new SSL certificates based on CA in [directory]",
    type=click.Path(),
)
@click.pass_context
def ceres_init_cmd(ctx: click.Context, name: str, create_certs: str, **kwargs):
    print('ceres init cmd')
    print(ctx)
    print(name)