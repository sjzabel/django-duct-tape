#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages
    
import os

setup(
    name = "django-duct-tape",
    version = "0.3",
    url = 'https://github.com/sjzabel/django-duct-tape',
    download_url = 'https://github.com/sjzabel/django-duct-tape',
    license = 'BSD',
    description = "Duct tape is a collection of tools and utilites that I find helpful for a django app",
    author = 'Stephen J. Zabel',
    author_email = 'sjzabel@gmail.com',
    #packages = ['duct_tape'],
    packages = find_packages('django-duct-tape'),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
