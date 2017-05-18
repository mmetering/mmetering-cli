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

    def get_base_dir(self):
        self.read()
        try:
            return self.config.get('mmetering', 'base_dir')
        except configparser.NoOptionError:
            print 'No base_dir specified in %s' % self.configfile
            print 'Use mmetering-cli setup'

    def set_base_dir(self, path):
        base_dir = os.path.expanduser(path)

        self.read()
        self.config.set('mmetering', 'base_dir', base_dir)

        self.write()

