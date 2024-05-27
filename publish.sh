# python3 -m build

rm -rf build dist tai_llama.egg-info cli.spec

python3 setup.py sdist bdist_wheel

pip install twine 
twine upload --repository pypi dist/*  # Or 'twine upload --repository testpypi ...'
