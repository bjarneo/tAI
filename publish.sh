#!/bin/bash

# Clean old builds
rm -rf build dist *.egg-info

# Ensure we're using pipenv environment
pipenv install setuptools twine wheel

# Build package
pipenv run python setup.py sdist bdist_wheel

# Upload to PyPI
pipenv run twine upload --repository pypi dist/*
