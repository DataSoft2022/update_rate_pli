from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in update_rate_pli/__init__.py
from update_rate_pli import __version__ as version

setup(
	name="update_rate_pli",
	version=version,
	description="ds",
	author="ds",
	author_email="mina.m@datasofteg.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
