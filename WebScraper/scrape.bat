call activate_venv.bat

@echo off
setlocal enabledelayedexpansion

rem set "urls=https://www.m-f.ch/software-engineering https://www.m-f.ch/ai https://www.m-f.ch/pruefsysteme https://www.industrie2025.ch/wissen-industrie-40/use-cases"
rem set "names=mf_software mf_ai mf_pruefsysteme i40_usecases"
set "urls=https://www.m-f.ch"
set "names=mf_ai"

for %%a in (%urls%) do (
    for /f "tokens=1* delims= " %%i in ("!names!") do (
        call clearresults.bat
        python scrape.py %%a --recursive
        ren result.md %%i.md
        set "names=%%j"
    )
)