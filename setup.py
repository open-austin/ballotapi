import os
from setuptools import setup

from ballotapi import __version__

curdir = os.path.dirname(__file__)
long_description = open(os.path.join(curdir, "ballotapi", "README.md")).read()
requirements = open(os.path.join(curdir, "requirements.txt")).read().strip().split("\n")

setup(
    name="ballotapi",
    version=__version__,
    description="REST API server for U.S. election ballot information",
    keywords=["ballotapi", "ballot api", "election api"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ballotapi.org",
    project_urls={
        "Documentation": "https://ballotapi.org/docs",
        "Code": "https://github.com/open-austin/ballotapi",
        "Issue tracker": "https://github.com/open-austin/ballotapi/issues",
    },
    author="Daniel Roesler",
    author_email="diafygi@gmail.com",
    license="Public Domain",
    packages=["ballotapi"],
    package_dir={"ballotapi": "ballotapi"},
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*",
    install_requires=requirements,
    entry_points={"console_scripts": ["ballotapi = ballotapi.cli:main"],
    },
    classifiers = [
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: System Administrators",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)

