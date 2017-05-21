mmetering-cli
#############################


.. image:: https://travis-ci.org/chrisonntag/mmetering-cli.svg?branch=master
   :target: https://travis-ci.org/chrisonntag/mmetering-cli

This is a simple CLI tool used for shortening long commands around `mmetering-server`_.

.. _`mmetering-server`: https://mmetering.chrisonntag.com

Install
-------

Make sure you have at least Python 2.7 installed. To install the application for all users, run::

  $ sudo ./setup.py install


This requires setuptools to be available. The setup script will automatically install all prerequisites and add 
the mmetering-cli executable to $PATH.

Then you can simply do::

  $ mmetering-cli <operation>

Usage
_____

Usage: mmetering-cli [OPTIONS] COMMAND [ARGS]...

  mmetering-cli - CLI tool used for shortening long commands

Options:
  --version  Show mmetering-cli version
  --help     Show this message and exit.

Commands:
  migrate    Makes migrations and migrates changes
  mmetering  Check the version (--version)
  restart    Restarts all services (TODO: Implement)
  setup      Setup where your mmetering_server...
  status     Checks status of redis, celery and apache
  test       Executes test for the whole project or an app


License
-------

This code is licensed under the `MIT License`_.

.. _`MIT License`: https://github.com/chrisonntag/mmetering-cli/blob/master/LICENSE
