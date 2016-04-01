import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "project",
    version = "0.0.1",
    author = "Dmitry Khodakov",
    author_email = "dmitryhd@gmail.com",
    description = ("Project"),
    license = "MIT",
    keywords = "",
    packages=['dashboard', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)