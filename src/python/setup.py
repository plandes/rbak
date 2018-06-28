from setuptools import setup, find_packages

setup(
    name = "zensols.rbak",
    packages = ['zensols', 'zensols.rbak'],
    version = '0.1',
    description = 'Simple program to mount file systems and backup directories',
    author = 'Paul Landes',
    author_email = 'landes@mailc.net',
    url = 'https://github.com/plandes/rbak',
    download_url = 'https://github.com/plandes/rbak/releases/download/v0.0.1/zensols.rbak-0.1-py3-none-any.whl',
    keywords = ['tooling'],
    classifiers = [],
    entry_points={
        'console_scripts': [
            'rbak=zensols.rbak.cli:main'
        ]
    }
)
