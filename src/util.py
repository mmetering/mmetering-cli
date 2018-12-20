
def get_docker_bash(container):
    command = ['docker', 'exec', '-it', 'container', '/bin/bash']
    command[3] = container

    return command
