@echo off

REM Check if the virtual environment directory exists
IF NOT EXIST "base" (
    echo Môi trường ảo không tồn tại. Đang tạo môi trường ảo...
    python -m venv base
    IF %ERRORLEVEL% NEQ 0 (
        echo Không thể tạo môi trường ảo
        exit /b 1
    )
)

REM Activate the virtual environment
call base\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    echo Không thể kích hoạt môi trường ảo
    exit /b 1
)

REM Install the requirements
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo Không thể cài đặt các thư viện
    exit /b 1
)

echo Starting...
REM Uncomment the next line if you want to clear data_lake before running the app
REM del /Q /F /S data_lake\*

REM Start the streamlit application
streamlit run app.py
IF %ERRORLEVEL% NEQ 0 (
    echo Không thể khởi chạy ứng dụng Python
    exit /b 1
)

REM Deactivate the virtual environment
call base\Scripts\deactivate.bat
IF %ERRORLEVEL% NEQ 0 (
    echo Không thể tắt môi trường ảo
    exit /b 1
)
