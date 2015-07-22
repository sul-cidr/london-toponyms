

from setuptools import setup, find_packages


setup(

    name='london-toponyms',
    version='0.1.0',
    description='Find references to London place names.',
    url='https://github.com/sul-cidr/london-toponyms',
    license='Apache',
    packages=find_packages(),
    scripts=['bin/london'],

    install_requires=[

        'ipython',
        'anyconfig',
        'PyYAML',
        'redis',
        'rq',
        'rq-dashboard',
        'click',
        'psycopg2',
        'peewee',
        'elasticsearch',
        'clint',
        'blessings',

    ]

)
