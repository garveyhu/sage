@echo off
chcp 65001

set PROJECT_NAME=sage

:: 查找并检查 Python 版本
for %%i in (python3, python) do (
    %%i --version > NUL 2>&1
    if NOT ERRORLEVEL 1 (
        set PYTHON_CMD=%%i
        goto checkVersion
    )
)
echo ❌ Python 未安装，请安装 Python。
goto end

:checkVersion
%PYTHON_CMD% -c "import sys; sys.exit(not (sys.version_info >= (3, 10)))"
if ERRORLEVEL 1 (
    echo ❌ Python 3.10 或更高版本是必需的。
    goto end
)

:: 检查并安装 Poetry
%PYTHON_CMD% -m poetry --version > NUL 2>&1
if ERRORLEVEL 1 (
    echo 🚀 Poetry 未安装，正在安装 Poetry...
    %PYTHON_CMD% -m pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple
    if ERRORLEVEL 1 (
        echo ❌ Poetry 安装失败，请检查网络或配置。
        goto end
    )
)

echo 🐍 安装依赖包...
%PYTHON_CMD% -m poetry install --without dev
echo ✅ 完成安装依赖包！启动中...
%PYTHON_CMD% -m poetry run python -m %PROJECT_NAME%

:end
pause
