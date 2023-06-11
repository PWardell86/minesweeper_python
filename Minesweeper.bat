@echo off

echo Launching game...
cd .\src && SET PYTHONPATH=$PYTHONPATH;..\ && python -m main.game %* && cd ../