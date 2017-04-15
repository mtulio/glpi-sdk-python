"""A setuptools based setup module. """

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='glpi',
    version='0.1.0',
    description='GLPI Python SDK',
    long_description=long_description,
    url='https://github.com/truly-systems/glpi-sdk-python',
    author='The Python Packaging Authority',
    author_email='marco.tulio@predict-systems.com',
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache-2.0 License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='GLPI SDK for developers',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests'],
)
