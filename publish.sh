
# remove previous releases
rm -rf build/ dist/ slovakrailways.egg-info/ __pycache__/
# compile
python setup.py sdist bdist_wheel
# publish
#twine check dist/*
python -m twine upload dist/*