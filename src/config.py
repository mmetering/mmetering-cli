import os
import ConfigParser as configparser

class Config(object):
    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.configfile = os.path.expanduser('~/.mmetering-clirc')

        if not os.path.isfile(self.configfile):
            # setup a new config file
            self.init_file()

    def init_file(self):
        self.config.add_section('mmetering')

        with open(self.configfile, 'a+') as configfile:
            self.config.write(configfile)

    def read(self):
        self.config.read(self.configfile)

    def write(self):
        with open(self.configfile, 'wb') as configfile:
            self.config.write(configfile)

    def set(self, section, name, value):
        val = os.path.expanduser(value)

        self.read()
        self.config.set(section, name, val)
        self.write()

    def get(self, section, name):
        self.read()
        try:
            return self.config.get(section, name)
        except configparser.NoOptionError:
            print 'No %s specified in %s' % (name, self.configfile)
            print 'Try \'mmetering-cli setup\''

