

import os
import re
import hashlib


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
    def es_id(self):

        """
        Provide a id for Elasticsearch.

        Returns: str
        """

        return os.path.basename(self.path)


    def es_paragraph_id(self, offset):

        """
        Provide an Elasticsearch id for an individual paragraph.

        Args:
            offset (int): A paragraph offset.

        Returns: str
        """

        name = (self.es_id+str(offset)).encode('utf8')
        return hashlib.sha1(name).hexdigest()


    def paragraphs(self):

        """
        Generate paragraphs from the text.

        Yields:
            str: The next paragraph.
        """

        for match in re.split('\n{2}', self.body):
            yield match
