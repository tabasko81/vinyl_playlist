#!/bin/bash
echo "Instalando PyInstaller..."
pip install pyinstaller

echo ""
echo "Compilando aplicação para executável..."
python -m PyInstaller --onefile --windowed --name="M3U8_Parser" main.py

echo ""
echo "Compilação concluída!"
echo "O executável está em: dist/M3U8_Parser.exe"

