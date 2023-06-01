@echo off

if /I "%1" == "" (@echo off) else ( echo Mode not implemented... ignoring %1)

echo Launching game...
cd .\src && SET PYTHONPATH=$PYTHONPATH;..\ && python -m main.game && cd ../