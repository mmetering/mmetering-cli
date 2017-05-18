import click
from src.config import Config
from subprocess import Popen, call


pass_config = click.make_pass_decorator(Config)

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
@click.pass_context
def setup(ctx):
    base_dir = click.prompt('Enter the absolute installation path to mmetering-server.', str)
    if click.confirm('Use mmetering-cli config file location: (~/.mmetering-cli)'):
        config_loc = '~/.mmetering-cli'
    else:
        config_loc = click.prompt('Enter new path for config file')
    
    # Init the config file
    ctx.obj = Config(config_loc)
    ctx.obj.set_base_dir(base_dir)



@main.command()
@pass_config
def sync(config):
    """Makes migrations and migrates changes"""
    click.echo("Starting Migration...")

@main.command()
def status():
    click.echo("Checking redis...")
    click.echo("Checking celery workers and beat...")
    click.echo("Checking modwsgi...")

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

