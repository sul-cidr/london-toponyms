

import os


class Text:


    def __init__(self, path):

        """
        Store the file path.

        Args:
            path (str): The file path.
        """

        self.path = path


    @property
    def body(self):

        """
        Read the file contents.

        Returns:
            str: The text body.
        """

        with open(self.path, 'r', errors='replace') as f:
            return f.read()


    @property
    def es_doc(self):

        """
        Provide a document for Elasticsearch.

        Returns: dict
        """

        return {
            '_id': os.path.basename(self.path),
            'body': self.body
        }
