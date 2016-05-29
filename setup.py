#!/usr/bin/env python

from distutils.core import setup

setup(
  name='rHEALPixDGGS',
  version='0.5.1',
  author='Alexander Raichev',
  author_email='alex@raichev.net',
  packages=['rhealpix_dggs', 'rhealpix_dggs.tests'],
  url='http://code.scenzgrid.org/index.php/p/scenzgrid-py/',
  license='LICENSE.txt',
  long_description=open('README.rst').read(),
  description='An implementation of the rHEALPix discrete global grid system',
  install_requires=[
    'numpy>=1.11.0',
    'matplotlib>=1.5.1',
    'pyproj>=1.9.5',
    'scipy>=0.17.1',
  ],
)
