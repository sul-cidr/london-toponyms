

import os
import anyconfig
import logging

from rq import Queue
from elasticsearch import Elasticsearch
from redis import StrictRedis


# Throttle logging.
logging.getLogger('elasticsearch.trace').propagate = False
anyconfig.set_loglevel('WARNING')


class Config:


    @classmethod
    def from_env(cls):

        """
        Get a config instance with the default file precedence.
        """

        return cls([
            os.path.join(os.path.dirname(__file__), 'london.yml'),
            '~/.london.yml',
        ])


    def __init__(self, paths):

        """
        Initialize the configuration object.

        Args:
            paths (list): YAML paths, from the most to least specific.
        """

        self.paths = paths
        self.read()


    def __getitem__(self, key):

        """
        Get a configuration value.

        Args:
            key (str): The configuration key.

        Returns:
            The option value.
        """

        return self.config[key]


    def read(self):

        """
        Load the configuration files, set connections.
        """

        self.config = anyconfig.load(self.paths, ignore_missing=True)
        self.es = self.get_es()
        self.rq = self.get_rq()


    def get_es(self):

        """
        Get an Elasticsearch connection.

        Returns:
            elasticsearch.Elasticsearch
        """

        if 'elasticsearch' in self.config:
            return Elasticsearch([self['elasticsearch']])


    def get_rq(self):

        """
        Get an RQ instance.

        Returns:
            rq.Queue
        """

        if 'redis' in self.config:
            redis = StrictRedis(**self['redis'])
            return Queue(connection=redis)


# Global instance.
config = Config.from_env()
