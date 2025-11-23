@echo off
REM ========================================
REM Retail Analytics Copilot - Package Script
REM Run this to prepare delivery package
REM ========================================

echo.
echo ============================================
echo  Retail Analytics Copilot - Packaging
echo ============================================
echo.

REM Step 1: Clean up unnecessary files
echo [1/4] Cleaning up unnecessary files...
if exist __pycache__ rmdir /s /q __pycache__
if exist agent\__pycache__ rmdir /s /q agent\__pycache__
if exist agent\rag\__pycache__ rmdir /s /q agent\rag\__pycache__
if exist agent\tools\__pycache__ rmdir /s /q agent\tools\__pycache__
del /q *.pyc 2>nul
del /q check_dspy.py 2>nul
del /q find_ollama.py 2>nul
del /q inspect_dspy.py 2>nul
del /q test_agent.py 2>nul
echo    Cleanup complete!

REM Step 2: Create delivery folder
echo.
echo [2/4] Creating delivery folder...
if exist ..\Retail_Analytics_Copilot_Delivery rmdir /s /q ..\Retail_Analytics_Copilot_Delivery
mkdir ..\Retail_Analytics_Copilot_Delivery
echo    Folder created!

REM Step 3: Copy essential files
echo.
echo [3/4] Copying files...
xcopy /s /i /q agent ..\Retail_Analytics_Copilot_Delivery\agent
xcopy /s /i /q data ..\Retail_Analytics_Copilot_Delivery\data
xcopy /s /i /q docs ..\Retail_Analytics_Copilot_Delivery\docs
copy requirements.txt ..\Retail_Analytics_Copilot_Delivery\
copy run_agent_simple.py ..\Retail_Analytics_Copilot_Delivery\
copy run_agent_hybrid.py ..\Retail_Analytics_Copilot_Delivery\
copy optimize_dspy.py ..\Retail_Analytics_Copilot_Delivery\
copy create_views.py ..\Retail_Analytics_Copilot_Delivery\
copy run_project.ps1 ..\Retail_Analytics_Copilot_Delivery\
copy sample_questions_hybrid_eval.jsonl ..\Retail_Analytics_Copilot_Delivery\
copy outputs_hybrid.jsonl ..\Retail_Analytics_Copilot_Delivery\
copy CLIENT_README.md ..\Retail_Analytics_Copilot_Delivery\README.md
copy PROJECT_SUMMARY.md ..\Retail_Analytics_Copilot_Delivery\
copy DELIVERY_GUIDE.md ..\Retail_Analytics_Copilot_Delivery\
echo    Files copied!

REM Step 4: Create ZIP
echo.
echo [4/4] Creating ZIP file...
powershell -command "Compress-Archive -Path '..\Retail_Analytics_Copilot_Delivery\*' -DestinationPath '..\Retail_Analytics_Copilot_v1.0.zip' -Force"
echo    ZIP created!

echo.
echo ============================================
echo  PACKAGING COMPLETE!
echo ============================================
echo.
echo Delivery package created at:
echo   ..\Retail_Analytics_Copilot_v1.0.zip
echo.
echo Folder also available at:
echo   ..\Retail_Analytics_Copilot_Delivery\
echo.
echo Next steps:
echo   1. Test the ZIP on another machine
echo   2. Send to client with CLIENT_README.md
echo   3. Follow DELIVERY_GUIDE.md for handoff
echo.
pause
