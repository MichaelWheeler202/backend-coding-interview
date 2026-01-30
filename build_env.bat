@echo off
SET VENV_NAME=.venv

REM Check if the virtual environment already exists
IF EXIST "%VENV_NAME%\Scripts\activate.bat" (
    ECHO Virtual environment already exists.
) ELSE (
    ECHO Creating virtual environment...
    python -m venv %VENV_NAME%
    IF ERRORLEVEL 1 (
        ECHO Failed to create virtual environment. Make sure Python is installed and added to PATH.
        PAUSE
        EXIT /B 1
    )
)

REM Activate the virtual environment and run commands
ECHO Activating virtual environment and installing dependencies...

REM Use CALL to run the activate script and return to the main script
CALL "%VENV_NAME%\Scripts\activate.bat"

REM Update pip
ECHO Updating pip...
python -m pip install --upgrade pip

REM Install requirements from requirements.txt
ECHO Installing packages from requirements.txt...
pip install -r requirements.txt


ECHO Environment setup complete.
PAUSE