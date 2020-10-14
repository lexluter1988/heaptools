# -*- encoding: utf-8 -*-
# !/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="web_tools-lexxsmith",
    version="0.0.1",
    author="Alexey Suponin",
    author_email="lexxsmith@gmail.com",
    description="Small tool to check auth.log and get info on visitors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    scripts=['auth_stat.py','domain_checker.py'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)