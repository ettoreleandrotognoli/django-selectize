#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from distutils.core import setup

from setuptools import find_packages

setup(
    name='django-selectize',
    version='0.0.0',
    description='Django + Selectize',
    author='Éttore Leandro Tognoli',
    author_email='ettore.leandro.tognoli@gmail.com',
    packages=find_packages(
        "src/python/"
    ),
    package_dir={
        "": "src/python/",
    },
    include_package_data=True,
)
