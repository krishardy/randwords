#!/usr/bin/env python
from distutils.core import setup

setup(
    name='randwords',
    version='1.0',
    description='Utilities to generate random words and strings',
    author='Kris Hardy',
    author_email='kris@rkrishardy.com',
    packages=['randwords'],
    data_files={'randwords': 'randwords/words'},
    entry_points={
        'console_scripts': [
            'randstring = randwords.cmd.randstring:main',
            'randwords = randwords.cmd.randwords:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: Utilities',
    ]
)