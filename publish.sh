# compile
python setup.py sdist bdist_wheel
# publish
twine check dist/*
#python -m twine upload dist/*