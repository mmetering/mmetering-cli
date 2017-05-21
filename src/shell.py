import os
import subprocess

class Shell():
    def __init__(self, source, wdir):
        self.source = source
        self.wdir = wdir

        self.set_source()

    def set_source(self):
        pipe = subprocess.Popen(". %s; env" % self.source, stdout=subprocess.PIPE, shell=True)
        output = pipe.communicate()[0]
        env = dict((line.split("=", 1) for line in output.splitlines()))
        os.environ.update(env)

    def execute(self, commands):
        output = subprocess.Popen(commands, cwd=self.wdir, stdout=subprocess.PIPE)
        return output.stdout

