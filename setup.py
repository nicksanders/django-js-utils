import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="django_js_utils",
    version="0.2",
    author="Matt Keeble",
    author_email="mattkeeble@gmail.com",
    description=("dutils is a small utility library that aims to provide JavaScript/Django developers with a few "
                 "utilities that will help the development of RIA on top of a Django Backend."),
    license="BSD",
    keywords="javascript routing js django templating",
    url="https://github.com/beldougie/django-js-utils",
    packages=find_packages(),
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
