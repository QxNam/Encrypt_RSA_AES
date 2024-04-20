#!/bin/bash

if [ ! -d "base" ]; then
    echo "Môi trường ảo không tồn tại. Đang tạo môi trường ảo..."
    python3 -m venv base || { echo "Không thể tạo môi trường ảo"; exit 1; }
    source base/bin/activate || { echo "Không thể kích hoạt môi trường ảo"; exit 1; }
    pip3 install -r requirements.txt || { echo "Không thể cài đặt các thư viện"; exit 1; }
fi

echo "Starting..."
# rm -rf data_lake/*
streamlit run app.py || { echo "Không thể khởi chạy ứng dụng Python"; exit 1; }

deactivate || { echo "Không thể tắt môi trường ảo"; exit 1; }