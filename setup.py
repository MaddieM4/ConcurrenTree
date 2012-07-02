#!/usr/bin/env python

from distutils.core import setup

setup(
	name='ConcurrenTree',
	version='0.5.0',
	long_description=open('README.md').read(),
	packages = [
		'ConcurrenTree',
		'ConcurrenTree.context',
		'ConcurrenTree.mcp',
		'ConcurrenTree.node',
		'ConcurrenTree.validation',
		'ConcurrenTree.wrapper',
	],
)
