

class Text:


    @classmethod
    def from_file(cls, path):

        """
        Create a text from a file.

        Args:
            path (str): The file path.
        """

        with open(path, 'r', errors='replace') as f:
            return cls(f.read())


    def __init__(self, text):

        """
        Store the raw text.

        Args:
            text (str): The text string.
        """

        self.text = text


    @property
    def es_doc(self):

        """
        Provide a document for Elasticsearch.

        Returns: dict
        """

        return {}
