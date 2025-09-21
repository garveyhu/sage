#!/bin/bash

PROJECT_NAME="sage"

function find_and_check_python() {
    for cmd in python3 python; do
        if command -v $cmd &> /dev/null; then
            if $cmd -c "import sys; sys.exit(not (sys.version_info >= (3, 10)))"; then
                echo $cmd
                return
            else
                echo -e "❌ Python 3.10 或更高版本是必需的。"
                exit 1
            fi
        fi
    done
    echo -e "❌ Python 未安装，请安装 Python。"
    exit 1
}

function check_and_install_poetry() {
    if ! $1 -m poetry --version &> /dev/null; then
        echo -e "🚀 Poetry 未安装，正在安装 Poetry..."
        $1 -m pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple
        if [ $? -ne 0 ]; then
            echo -e "❌ Poetry 安装失败，请检查网络或配置。"
            exit 1
        fi
    fi
}

PYTHON_CMD=$(find_and_check_python)
check_and_install_poetry $PYTHON_CMD

echo -e "🐍 安装依赖包..."
$PYTHON_CMD -m poetry install --without dev
echo -e "✅ 完成安装依赖包！启动中..."
$PYTHON_CMD -m poetry run python -m $PROJECT_NAME
