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
    version=__version__,
    description='GLPI Python SDK',
    long_description=readme(),
    url='https://github.com/truly-systems/glpi-sdk-python',
    author='Marco Tulio R Braga',
    author_email='braga@mtulio.eng.br',
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache-2.0 License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='GLPI SDK Library',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    #packages = ["glpi"],
    install_requires=[
        'requests',
    ]
)
