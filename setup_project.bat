@echo off
setlocal EnableDelayedExpansion

REM ============================================================
REM Usage: setup_project.bat (run from the repository folder)
REM Installs the VS Code Python and Microsoft Foundry extensions, logs
REM in to Azure, searches the current directory and its subfolders for
REM requirements files, asks which to use, then creates a virtual
REM environment in that folder and installs the requirements.
REM ============================================================

set "ROOT=%CD%"

REM --- Check prerequisites ---
where python >nul 2>&1 || (echo [ERROR] python not found in PATH & exit /b 1)
where code >nul 2>&1 || (echo [ERROR] VS Code "code" command not found in PATH & exit /b 1)
where az >nul 2>&1 || (echo [ERROR] Azure CLI "az" not found in PATH & exit /b 1)

REM --- 1. Install VS Code extensions (Python + Foundry Toolkit) ---
echo [1/5] Installing VS Code extensions...
call code --install-extension ms-python.python --force
if errorlevel 1 (echo [ERROR] Python extension install failed & exit /b 1)
call code --install-extension ms-windows-ai-studio.windows-ai-studio --force
if errorlevel 1 (echo [ERROR] Foundry Toolkit for VS Code extension install failed & exit /b 1)

REM --- 2. Azure login ---
echo [2/5] Checking Azure CLI login...
call az account show >nul 2>&1
if errorlevel 1 (
echo Not logged in. Launching az login...
call az login
if errorlevel 1 (echo [ERROR] az login failed & exit /b 1)
) else (
echo Already logged in.
)
echo Active Azure account:
call az account show --query "{Name:name, Subscription:id, User:user.name}" -o table

REM --- 3. Find requirements files in current directory and subfolders ---
echo [3/5] Searching "%ROOT%" and subfolders for requirements files...
set COUNT=0
for /r "%ROOT%" %%f in (requirements*.txt) do (
set "P=%%f"
REM Skip virtual envs and node_modules
if "!P:\.venv\=!"=="!P!" if "!P:\venv\=!"=="!P!" if "!P:\node_modules\=!"=="!P!" (
set /a COUNT+=1
set "D=%%~dpf"
set "REQ_DIR_!COUNT!=!D:~0,-1!"
set "REQ_FILE_!COUNT!=%%~nxf"
set "REL=!P:%ROOT%\=!"
echo !COUNT!^) !REL!
)
)

if %COUNT%==0 (
echo [ERROR] No requirements files found under %ROOT%.
exit /b 1
)

set "CHOICE="
set /p "CHOICE=Enter the number of the requirements file to use [1-%COUNT%]: "
if not defined REQ_DIR_%CHOICE% (
echo [ERROR] Invalid selection: %CHOICE%
exit /b 1
)

set "WORK_DIR=!REQ_DIR_%CHOICE%!"
set "REQ_FILE=!REQ_FILE_%CHOICE%!"
echo Using: !WORK_DIR!\!REQ_FILE!
cd /d "!WORK_DIR!"

REM --- 4. Create virtual environment ---
echo [4/5] Creating virtual environment (.venv) in !WORK_DIR!...
python -m venv .venv
if errorlevel 1 (echo [ERROR] venv creation failed & exit /b 1)

REM --- 5. Install requirements ---
echo [5/5] Installing requirements...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r "!REQ_FILE!"
if errorlevel 1 (echo [ERROR] pip install failed & exit /b 1)

echo.
echo Done. Activate with: !WORK_DIR!\.venv\Scripts\activate.bat
echo.

REM --- Launch VS Code at this location (with confirmation) ---
choice /c YN /m "Launch VS Code in !WORK_DIR!?"
if errorlevel 2 (
echo Skipping VS Code launch.
) else (
call code "!WORK_DIR!"
)
endlocal
