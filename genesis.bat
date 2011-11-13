@echo off

:: %~dp0 is shorthand for 'same dir as this .bat file'. Includes trailing '\'
python "%~dp0genesis-script.py" %*

