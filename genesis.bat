@echo off
:: %~dp0 is .bat file shorthand for same directory as this .bat file,
:: including trailing \
python "%~dp0genesis-script.py" %*

