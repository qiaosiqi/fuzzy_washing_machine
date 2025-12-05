@echo off
echo Starting Streamlit App...

REM 如果虚拟环境不存在就创建
IF NOT EXIST venv (
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate

REM 如果你要做依赖检查，加这一行（不想检查可以删掉）
pip install -r requirements.txt --quiet

REM 启动 Streamlit
streamlit run app.py

pause
