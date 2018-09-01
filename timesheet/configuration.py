# -*- coding: utf-8 -*-
from pymlconf import Root
from os import path, mkdir
from appdirs import user_data_dir, user_config_dir

__author__ = 'vahid'

data_dir = path.abspath(path.join(user_data_dir(), 'timesheet'))
user_config_file = path.abspath(path.join(user_config_dir(), 'timesheetrc'))

__builtin_config__ = """
db:
  uri: sqlite:///%(data_dir)s/timesheet.sqlite
  echo: false

datetime_format: %(time_format)s
date_format: %(date_format)s

"""

_cfg = None


def init_config(config_file=None):
    global _cfg
    if not path.exists(data_dir):
        mkdir(data_dir)

    _cfg = Root(
        __builtin_config__,
        context=dict(
            data_dir=data_dir,
            time_format='"%Y-%m-%d %H:%M"',
            date_format='"%Y-%m-%d"'
        )
    )

    if path.exists(user_config_file):
        _cfg.load_file(user_config_file)

    if config_file:
        _cfg.load_file(config_file)


class ConfigProxy(object):

    def __getattr__(self, key):
        if _cfg is None:
            raise Exception("Configuration not initialized yet.")
        return getattr(_cfg, key)

    def __setattr__(self, key, value):
        if _cfg is None:
            raise Exception("Configuration not initialized yet.")
        setattr(_cfg, key, value)


config = ConfigProxy()
