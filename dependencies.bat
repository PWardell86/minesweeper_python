@echo off
For /F "tokens=1* delims==" %%A IN (defaults.properties) DO (
    IF "%%A"=="pyglet" SET pyglet_version=%%B
    IF "%%A"=="jproperties" SET jproperties=%%B
)
python -m pip install pyglet==%pyglet_version%
python -m pip install jproperties==%jproperties%