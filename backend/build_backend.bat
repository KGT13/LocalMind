call ..\venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r ..\requirements.txt

echo Building backend...
pyinstaller -y --name backend --onedir --clean ^
--hidden-import uvicorn ^
--hidden-import fastapi ^
--hidden-import sse_starlette ^
--hidden-import pydantic ^
--hidden-import chromadb ^
--hidden-import langchain_community ^
--hidden-import langchain_ollama ^
--collect-all chromadb ^
--collect-all onnxruntime ^
--collect-all posthog ^
--collect-all langchain ^
--collect-all langchain_community ^
--collect-all sse_starlette ^
main.py
