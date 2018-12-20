import click
import subprocess
from src.config import Config
from src.shell import Shell
from src.util import *

pass_config = click.make_pass_decorator(Config, ensure=True)


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

    ctx.obj = Config()
    ctx.obj.set('mmetering', 'base_dir', base_dir)

    click.echo('You\'re ready to go now!')


@main.command()
@pass_config
@click.option('-a', '--app', help='Test specific app')
def test(config, app):
    """Executes test for the whole project or specific apps"""

    base_dir = config.get('mmetering', 'base_dir')
    shell = Shell(base_dir)
    command = get_docker_bash('mmetering_django')

    if app is not None:
        click.echo('Executing tests for %s' % app)
        command.extend(['-c', '"python manage.py test ' + app + '"'])
        output = shell.execute(command)
    else:
        click.echo('Executing tests for the whole project')
        command.extend(['-c', '"python manage.py test"'])
        output = shell.execute(command)

    printout(output)


@main.command()
@pass_config
@click.argument('container')
@click.option('--all', is_flag=True, help='Set these ENVs in all mmetering containers')
@click.option('-e', '--env', help='List of ENVs of type NAME=VAR separated by commas.')
def setenv(config, container, all, env):
    base_dir = config.get('mmetering', 'base_dir')
    shell = Shell(base_dir)

    env_list = ["export " + var for var in env.split(',')]
    env_string = ''.join(exp + ' && ' for exp in env_list)[:-4]  # Remove last for chars ' && '

    # TODO: Docker container doesn't hold ENV's forever
    if all:
        mmetering_container = shell.execute(['docker', 'ps', '--filter', 'name=mmetering_', '--format', '{{.ID}}'])
        mmetering_container = [container_id.decode("utf-8").replace('\n', '') for container_id in mmetering_container]

        for container_id in mmetering_container:
            command = get_docker_bash(container_id)
            command.extend(['-c', env_string])
            shell.execute(command)
    else:
        if container is not None:
            command = get_docker_bash(container)
            command.extend(['-c', env_string])
            shell.execute(command)
        else:
            click.echo('Please specifiy a container.')


@main.command()
@click.option('--version', expose_value=True, is_flag=True, is_eager=True, help='Show mmetering version')
@pass_config
def mmetering(config, version):
    """Check the version (--version)"""

    base_dir = config.get('mmetering', 'base_dir')

    if base_dir is not None:
        shell = Shell(base_dir)
        output = shell.execute(['git', 'describe', '--tags'])
        printout(output, char='mmetering-server')


def printout(output_file, *args, **kwargs):
    for line in output_file:
        click.echo(kwargs.get('char', '') + line.decode('utf-8').replace('\n', ''))

