from setuptools import setup
from os import path

nname, dname = None, path.abspath(path.join(path.dirname(__file__)))
while nname != dname:
    nname, dname = dname, path.abspath(path.join(dname, path.pardir))
    if path.exists(path.join(dname, 'README.md')):
        break
with open(path.join(dname, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "zensols.rbak",
    packages = ['zensols', 'zensols.rbak'],
    version = '0.4',
    description = 'Simple program to mount file systems and backup directories',
    author = 'Paul Landes',
    author_email = 'landes@mailc.net',
    url = 'https://github.com/plandes/rbak',
    download_url = 'https://github.com/plandes/rbak/releases/download/v0.0.4/zensols.rbak-0.4-py3-none-any.whl',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    keywords = ['tooling'],
    classifiers = [],
    entry_points={
        'console_scripts': [
            'rbak=zensols.rbak.cli:main'
        ]
    }
)
