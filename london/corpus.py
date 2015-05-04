

import os

from london.text import Text


class Corpus:


    es_index = 'london'
    es_doc_type = 'text'


    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True
        },
        'properties': {
            'body': {
                'type': 'string'
            }
        }
    }


    @classmethod
    def es_create(cls):

        """
        Set the Elasticsearch mapping.
        """

        config.es.indices.create(cls.es_index, {
            'mappings': { cls.es_doc_type: cls.es_mapping }
        })


    @classmethod
    def es_delete(cls):

        """
        Delete the index.
        """

        if config.es.indices.exists(cls.es_index):
            config.es.indices.delete(cls.es_index)


    @classmethod
    def es_count(cls):

        """
        Count the number of documents.
        Returns:
            int: The number of docs.
        """

        r = config.es.count(cls.es_index, cls.es_doc_type)
        return r['count']


    @classmethod
    def es_reset(cls):

        """
        Clear and recreate the index.
        """

        cls.es_delete()
        cls.es_create()


    def __init__(self, path):

        """
        Normalize the corpus path.

        Args:
            path (str): The corpus base path.
        """

        self.path = os.path.abspath(path)


    def file_names(self):

        """
        Generate text file names.

        Yields:
            str: The next file name.
        """

        for name in os.listdir(self.path):
            yield name


    def file_paths(self):

        """
        Generate fully paths for each file.

        Yields:
            str: The next file path.
        """

        for name in self.file_names():
            yield os.path.join(self.path, name)


    def texts(self):

        """
        Generate Text instances for each file.

        Yields:
            Text: The next text.
        """

        for path in self.file_paths():
            yield Text(path)
