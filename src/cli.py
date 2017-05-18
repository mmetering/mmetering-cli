from subprocess import Popen, call
import click


def pr_mmetering_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("v1.1.0")
    ctx.exit()

@click.group()
@click.version_option(help='Show mmetering-cli version')
def main():
    """mmetering-cli"""
    nothing = None

@main.command()
def setup():
    base_dir = click.prompt('Enter the absolute installation path to mmetering-server.', str)
    if click.confirm('Use mmetering-cli config file location: (~/.mmetering-cli)'):
        config_loc = '~/.mmetering-cli'
    else:
        config_loc = click.prompt('Enter new path for config file')

@main.command()
def check():
    click.echo("Checking redis...")
    click.echo("Checking celery workers and beat...")
    click.echo("Checking modwsgi...")

@main.command()
def sync(name):
    """Makes migrations and migrates changes"""
    click.echo("Starting Migration...")
    call()

@main.command()
@click.option('-w', '--webserver', default=True)
@click.option('-c', '--celery', default=True)
@click.option('-r', '--redis', default=True)
def restart(webserver, celery, redis):
    """Restarts all services"""
    nothing = None

@main.command()
@click.option('--version', is_flag=True, callback=pr_mmetering_version, 
        expose_value=False, is_eager=True, help='Show mmetering version')
def mmetering():
    nothing = None

