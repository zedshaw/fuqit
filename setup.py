try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'package_data': {
    }, 
    'description': 'The Fuqit Web Framework: Shit files into dir, get some web.',
    'author': 'Zed A. Shaw',
    'url': 'http://pypi.python.org/pypi/fuqit',
    'download_url': 'http://pypi.python.org/pypi/fuqit',
    'author_email': 'zedshaw@zedshaw.com',
     'version': '1.0',
     'scripts': ['bin/fuqit'],
     'install_requires': ['python-modargs', 'python-lust'],
     'packages': ['fuqit', 'fuqit.db'],
     'name': 'fuqit'
}

setup(**config)
