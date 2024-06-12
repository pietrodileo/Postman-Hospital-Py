@echo off
echo ""

:: Execute the first Python script
python daily_notification_big_message_generator.py

:: Check if the first script executed successfully
if %errorlevel% neq 0 (
    echo First script failed to execute.
    exit /b %errorlevel%
)

echo First script executed successfully.

:: Execute the second Python script
python send_post_request.py

:: Check if the second script executed successfully
if %errorlevel% neq 0 (
    echo Second script failed to execute.
    exit /b %errorlevel%
)

echo Second script executed successfully.

:: Execute the second Python script a second time in order to test the API error response
::python send_post_request.py

:: Check if the second script executed successfully
if %errorlevel% neq 0 (
    echo Error test failed to execute.
    exit /b %errorlevel%
)

echo Error test executed successfully.
echo ""