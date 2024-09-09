@echo off
echo.

:: Define the number of service requests
set NUM_SERVICE_REQUESTS=200000

:: Execute the first Python script with the defined number of service requests
python daily_notification_big_message_generator_hl7.py %NUM_SERVICE_REQUESTS%

:: Check if the first script executed successfully
if %errorlevel% neq 0 (
    echo First script failed to execute.
    exit /b %errorlevel%
)

echo First script executed successfully.
echo.

:: Execute the second Python script
python send_hl7_daily_notif_mllp.py

:: Check if the second script executed successfully
if %errorlevel% neq 0 (
    echo Second script failed to execute.
    exit /b %errorlevel%
)

echo Second script executed successfully.
echo.

:: Execute the second Python script a second time in order to test the API error response
python send_hl7_daily_notif_mllp.py

:: Check if the second script executed successfully
if %errorlevel% neq 0 (
    echo Error test failed to execute.
    exit /b %errorlevel%
)

echo Error test executed successfully.
echo.