

import os
import re


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


    def paragraphs(self):

        """
        Generate paragraphs from the text.

        Yields:
            str: The next paragraph.
        """

        for match in re.split('\n{2}', self.body):
            yield match
