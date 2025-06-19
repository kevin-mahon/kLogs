echo "Make sure to increase the version number and delete the dist directory"
rm dist/*
python -m build
python -m twine upload --verbose --repository testpypi dist/*
