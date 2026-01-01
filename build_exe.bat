@echo off
echo Instalando PyInstaller...
pip install pyinstaller

echo.
echo Compilando aplicacao para executavel...
python -m PyInstaller --onefile --windowed --name="M3U8_Parser" main.py

echo.
echo Compilacao concluida!
echo O executavel esta em: dist\M3U8_Parser.exe
pause

