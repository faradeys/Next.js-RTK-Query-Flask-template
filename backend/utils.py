"""Main projects infrastructure utils."""
import os


def get_config(name):
    """Get value from top level config.py."""
    return getattr(__import__('instance.config',
                              fromlist=[name]),
                   name)


def get_env(name):
    """Get environment var."""
    return os.environ.get(name)
