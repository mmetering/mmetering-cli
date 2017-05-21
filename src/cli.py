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
    """mmetering-cli - CLI tool used for shortening long commands"""
    nothing = None

@main.command()
@click.pass_context
def setup(ctx):
    """Setup where your mmetering_server installation and it's virtualenvironment lives"""

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
    """Checks status of redis, celery and apache"""

    click.secho('Checking redis...', bold=True)
    pipe = subprocess.Popen(['redis-cli', 'ping'], stdout=subprocess.PIPE)
    output = [line.replace('\n', '') for line in pipe.stdout]
    if output is [] and output[0] == 'PONG':
        click.secho('\tredis-server is running properly', fg='green')
    else:
        click.secho('\tredis-server is not working properly', fg='red')


    click.secho('Checking celery workers and beat...', bold=True)
    worker = subprocess.Popen(['sudo', '/usr/bin/supervisorctl', 'status', 'mmeteringcelery'], 
            stdout=subprocess.PIPE)
    printout(worker.stdout, char='\t')

    beat = subprocess.Popen(['sudo', '/usr/bin/supervisorctl', 'status', 'mmeteringcelerybeat'], 
            stdout=subprocess.PIPE)
    printout(beat.stdout, char='\t')


    click.secho('Checking the webserver...', bold=True)
    try:
        apache2 = subprocess.Popen(['/etc/init.d/apache2', 'status'], stdout=subprocess.PIPE)
        printout(apache2.stdout, char='\t')
    except OSError:
        click.secho('\tApache2 is not running or not available under /etc/init.d/apache2', fg='red')
        click.secho('\tCheck installation path under your system', fg='red')


@main.command()
@click.option('-w', '--webserver', default=True)
@click.option('-c', '--celery', default=True)
@click.option('-r', '--redis', default=True)
def restart(webserver, celery, redis):
    """
    Restarts all services (TODO: Implement)
    """
    nothing = None

@main.command()
@click.option('--version', expose_value=True, is_flag=True, is_eager=True, help='Show mmetering version')
@pass_config
def mmetering(config, version):
    """Check the version (--version)"""

    base_dir = config.get('mmetering', 'base_dir')
    venv = config.get('mmetering', 'venv')

    if base_dir and venv is not None:
        shell = Shell(venv, base_dir)
        output = shell.execute(['git', 'describe', '--tags'])
        printout(output, char='mmetering-server')

def printout(output_file, *args, **kwargs):
    for line in output_file:
        click.echo(kwargs.get('char', '') + line.replace('\n', ''))

