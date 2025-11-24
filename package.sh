#!/bin/bash

echo "Building PolyglotX package..."
echo "=============================="

echo "Cleaning previous builds..."
rm -rf build dist *.egg-info

echo "Building source distribution..."
python setup.py sdist

echo "Building wheel distribution..."
python setup.py bdist_wheel

echo "Package built successfully!"
echo "Files created in dist/ directory:"
ls -lh dist/

echo ""
echo "To upload to PyPI:"
echo "  twine upload dist/*"
echo ""
echo "To install locally:"
echo "  pip install dist/PolyglotX-1.0.0-py3-none-any.whl"
echo ""
echo "By MERO @QP4RM"
