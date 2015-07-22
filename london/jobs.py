

from london.config import config


def query(toponym, size=10000, frag_size=5000):

    """
    Query the paragraph index for a toponym.

    Args:
        toponym (str)
    """

    results = config.es.search('london', 'text', body={
        'size': size,
        'fields': [],
        'query': {
            'match_phrase': {
                'text': {
                    'query': toponym,
                    'slop': 3
                }
            }
        },
        'highlight': {
            'fields': {
                'text': {
                    'fragment_size': frag_size,
                    'number_of_fragments': 1
                }
            }
        }
    })

    for hit in results['hits']['hits']:
        print(hit)
