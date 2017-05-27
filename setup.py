from setuptools import setup, find_packages
from codecs import open
from os import path


def readme():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        return f.read()

exec (open('glpi/version.py').read())

setup(
    name='glpi',
    packages=["glpi"],
    version=__version__,
    description='GLPI API SDK',
    #long_description=readme(),
    url='https://github.com/truly-systems/glpi-sdk-python',
    download_url='https://github.com/truly-systems/glpi-sdk-python/archive/%s.tar.gz' % __version__,
    author='Marco Tulio R Braga',
    author_email='braga@mtulio.eng.br',
    license='Apache-2.0',
    classifiers=[],
    keywords=['GLPI', 'SDK'],
    install_requires=[
        'requests',
    ]
)
