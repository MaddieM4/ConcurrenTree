#!/usr/bin/env python

from distutils.core import setup

setup(
	name='ConcurrenTree',
	version='0.4',
	long_description=open('README.md').read(),
	packages = [
		'ConcurrenTree',
		'ConcurrenTree.model',
		'ConcurrenTree.model.context',
		'ConcurrenTree.model.mcp',
		'ConcurrenTree.model.node',
		'ConcurrenTree.model.validation',
		'ConcurrenTree.model.wrapper',
		'ConcurrenTree.storage',
	],
)
