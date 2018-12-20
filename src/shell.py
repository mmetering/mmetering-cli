import os
import subprocess


class Shell:
    def __init__(self, wdir):
        self.wdir = wdir

    def set_source(self, source):
        pipe = subprocess.Popen(". %s; env" % source, stdout=subprocess.PIPE, shell=True)
        output = pipe.communicate()[0]
        env = dict((line.split("=", 1) for line in output.splitlines()))
        os.environ.update(env)

    def execute(self, commands):
        output = subprocess.Popen(commands, cwd=self.wdir, stdout=subprocess.PIPE)
        return output.stdout

