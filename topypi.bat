@echo off
echo j'espère que t'as bien changé la version konar
pause
python setup.py sdist bdist
pause
twine upload dist/*
pause
