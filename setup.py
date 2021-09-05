# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in thaisummit/__init__.py
from thaisummit import __version__ as version

setup(
	name='thaisummit',
	version=version,
	description='Customizations for Thai summit',
	author='TEAMPRO',
	author_email='erp@groupteampro.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
