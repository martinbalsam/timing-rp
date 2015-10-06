from distutils.core import setup

setup(
    name='timing-rp',
    version='0.1dev',
    author='Giulio Rasi'
    author_email='giuliorasi@gmail.com'
    url='http://github.com/martinbalsam/timing-rp'
    packages=['timingrp','timingrp.test'],
    license='GNU General Public License version 2',
    long_description=open('README.txt').read(),
)