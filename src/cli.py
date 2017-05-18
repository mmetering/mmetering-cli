import click
import subprocess
from src.config import Config


pass_config = click.make_pass_decorator(Config, ensure=True)

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
    
    ctx.obj = Config()
    ctx.obj.set_base_dir(base_dir)

    click.echo('You\'re ready to go now!')


@main.command()
@pass_config
def sync(config):
    """Makes migrations and migrates changes"""
    base_dir = config.get_base_dir()

    if base_dir is not None:
        click.echo("Starting Migration in %s" % base_dir)
        subprocess.Popen('python3 manage.py makemigrations', cwd=base_dir, 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

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

