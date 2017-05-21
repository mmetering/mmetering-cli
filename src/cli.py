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
@click.option('-a', '--app', help='Test specific app')
@pass_config
def test(config, app):
    """Executes test for the whole project or specific apps"""
    base_dir = config.get('mmetering', 'base_dir')
    venv = config.get('mmetering', 'venv')
    
    if base_dir and venv is not None:
        shell = Shell(venv, base_dir)

        if app is not None:
            click.echo('Executing tests for %s' % app)
            output = shell.execute(['python3', 'manage.py', 'test', app])
        else:
            click.echo('Executing tests for the whole project')
            output = shell.execute(['python3', 'manage.py', 'test'])

        printout(output)


@main.command()
@pass_config
def migrate(config):
    """Makes migrations and migrates changes"""
    base_dir = config.get('mmetering', 'base_dir')
    venv = config.get('mmetering', 'venv')

    if base_dir and venv is not None:
        click.echo('Starting Migration in %s' % base_dir)
        shell = Shell(venv, base_dir)
        output = shell.execute(['python3', 'manage.py', 'makemigrations'])
        
        printout(output)
        
        output = shell.execute(['python3', 'manage.py', 'migrate'])
        printout(output)


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

def printout(output_file):
    for line in output_file:
        click.echo(line.replace('\n', ''))

