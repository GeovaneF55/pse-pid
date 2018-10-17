""" Bibliotecas externas. """
from setuptools import setup, find_packages

setup(
    name='PSE',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
        'opencv-python',
        'pyqt5 >= 5.11.3',
    ],
)
