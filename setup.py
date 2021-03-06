import codecs
import re
from os import path
import sys
from setuptools import setup, find_packages


def read(*parts):
    file_content = codecs.open(path.join(path.dirname(__file__), *parts)).read()
    py2 = sys.version_info < (3, 0)

    if not py2 and not isinstance(file_content, str):
        file_content = file_content.decode("utf-8")

    return file_content


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-js-utils',
    version=find_version("django_js_utils", "__init__.py"),
    description='Small utility Django app that aims to provide JavaScript/Django developers with a few utilities \
    that will help the development of RIA on top of a Django Backend',
    long_description=read('README.rst'),
    author='Dimitri-Gnidash',
    maintainer='Dimitri-Gnidash',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'static/js': ['*.js']
    },
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
)
