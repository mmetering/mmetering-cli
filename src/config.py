import os
import ConfigParser as configparser

class Config(object):
    def __init__(self, configfile):
        self.config = configparser.RawConfigParser()
        self.configfile = os.path.expanduser(configfile)

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
        return self.config.get('mmetering', 'base_dir')

    def set_base_dir(self, path):
        self.read()
        self.config.set('mmetering', 'base_dir', path)

        self.write()

