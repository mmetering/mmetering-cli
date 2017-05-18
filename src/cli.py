import click


def pr_mmetering_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('mmetering v1.1')
    ctx.exit()

@click.group()
@click.version_option(help='Show mmetering-cli version')
def main():
    """mmetering-cli"""
    nothing = None

@main.command()
@click.option('-n', '--name',  help='Prints your name')
def sync(name):
    click.echo("%s" % name)

@main.command()
@click.option('--version', is_flag=True, callback=pr_mmetering_version, 
        expose_value=False, is_eager=True, help='Show mmetering version')
def mmetering():
    nothing = None
