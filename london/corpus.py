

import os

from london.config import config
from london.text import Text
from elasticsearch.helpers import bulk
from clint.textui.progress import bar


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
    def from_env(cls):

        """
        Get an instance for the ENV-defined corpus.
        """

        return cls(config['corpus'])


    def __init__(self, path):

        """
        Normalize the corpus path.

        Args:
            path (str): The corpus base path.
        """

        self.path = os.path.abspath(path)


    def file_paths(self):

        """
        Generate fully paths for each file.

        Yields:
            str: The next file path.
        """

        for dirname, _, filenames in os.walk(self.path):
            for filename in filenames:
                yield os.path.join(dirname, filename)


    @property
    def file_count(self):

        """
        How many texts are in the corpus?

        Returns:
            int: The total count.
        """

        return sum(1 for _ in self.file_paths())


    def texts(self):

        """
        Generate Text instances for each file.

        Yields:
            Text: The next text.
        """

        for path in self.file_paths():
            yield Text(path)


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


    def es_stream_docs(self):

        """
        Generate Elasticsearch documents.

        Yields:
            dict: The next document.
        """

        for text in self.texts():
            yield text.es_doc


    def es_insert(self):

        """
        Insert Elasticsearch documents.
        """

        # Batch-insert the documents.
        bulk(
            config.es,
            self.es_stream_docs(),
            raise_on_exception=False,
            doc_type=self.es_doc_type,
            index=self.es_index,
            chunk_size=100
        )

        # Commit the index.
        config.es.indices.flush(self.es_index)
