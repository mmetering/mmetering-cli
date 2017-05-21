import click
import subprocess
from src.config import Config
from src.shell import Shell


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
    venv = click.prompt('Enter the path to your virtual environment activation script', str)
    
    ctx.obj = Config()
    ctx.obj.set('mmetering', 'base_dir', base_dir)
    ctx.obj.set('mmetering', 'venv', venv)

    click.echo('You\'re ready to go now!')

@main.command()
@pass_config
def migrate(config):
    """Makes migrations and migrates changes"""
    base_dir = config.get('mmetering', 'base_dir')
    venv = config.get('mmetering', 'venv')

    if base_dir and venv is not None:
        click.echo("Starting Migration in %s" % base_dir)
        shell = Shell(venv, base_dir)
        output = shell.execute(['python3', 'manage.py', 'makemigrations'])
        
        for line in output:
            print line.replace('\n', '')

        output = shell.execute(['python3', 'manage.py', 'migrate'])

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

