@echo off
SET GAMEDIR=%~dp0
SET PYTHONPATH=%GAMEDIR%src;%PYTHONPATH%
start /d %GAMEDIR% /b python -m main.game %*