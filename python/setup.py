 #! /usr/bin/env python

from distutils.core import setup

setup(name = 'rtree',
      version = '0.0.1',
      description = 'Python RTree implementation',
      author = 'Bhaskar Mookerji',
      author_email = 'mookerji@gmail.com',
      url = 'https://github.com/mookerji/pl2',
      packages = ['rtree', 
                  'rtree.rtree', 
                  'rtree.types', 
                  'rtree.tests.test_bench',
                  'rtree.tests.test_rtree',
                  'rtree.tests.test_types'],
      classifiers = ["Development Status :: 2 - Pre-Alpha",
                     "Environment :: Console"]
)
