@echo off
if exist WPy64-3890 (
    goto installed
) else (
    if exist Winpython64-3.8.9.0dot.exe (
        goto install
    ) else (
        
        goto download
    )
)

:download
echo Downloading Python.
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/winpython/winpython/releases/download/4.1.20210417/Winpython64-3.8.9.0dot.exe', 'Winpython64-3.8.9.0dot.exe')"

:install
echo Installing Python.
call Winpython64-3.8.9.0dot.exe -y
del Winpython64-3.8.9.0dot.exe

:installed
echo Starting Python.
CLS
call "WPy64-3890\python-3.8.9.amd64\python.exe" "main.py" "%1" "%2" "%3" "%4" "%5"