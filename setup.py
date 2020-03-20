#########################################
# setup.py                              #
# Setup for PyBKT                       #
#                                       #
# @author Anirudhan Badrinath           #
# Last edited: 09 March 2020            #
#########################################

from setuptools import setup

setup(
	name="pyBKT",
	version="1.3",
	author="Anirudhan Badrinath",
	author_email="abadrinath@berkeley.edu",
	description="PyBKT",
	url="https://github.com/CAHLR/pyBKT",
	packages=['pyBKT', 'pyBKT.generate', 'pyBKT.fit', 'pyBKT.util'],
	classifiers=[
	    "Programming Language :: Python :: 3",
	    "License :: OSI Approved :: MIT License",
	    "Operating System :: OS Independent",
	],
	install_requires = ["numpy"],
)
