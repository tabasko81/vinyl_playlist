"""
Parser para ficheiros .m3u8
Extrai o último diretório e nome do ficheiro de cada track
"""
import os
import re
from typing import List, Tuple


def parse_m3u8(file_path: str) -> List[Tuple[str, str]]:
    """
    Lê um ficheiro .m3u8 e extrai o último diretório e nome do ficheiro de cada track.
    
    Args:
        file_path: Caminho para o ficheiro .m3u8
        
    Returns:
        Lista de tuplas (folder, filename) para cada track encontrada
    """
    tracks = []
    
    # Tentar diferentes encodings
    encodings = ['utf-8', 'utf-8-sig', 'windows-1252', 'latin-1']
    content = None
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.readlines()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    if content is None:
        raise ValueError(f"Não foi possível ler o ficheiro {file_path} com nenhum encoding suportado")
    
    # Processar linha a linha
    i = 0
    while i < len(content):
        line = content[i].strip()
        
        # Procurar linhas #EXTINF:
        if line.startswith('#EXTINF:'):
            # A próxima linha não vazia deve ser o caminho do ficheiro
            i += 1
            while i < len(content) and not content[i].strip():
                i += 1
            
            if i < len(content):
                file_path_line = content[i].strip()
                
                # Verificar se é um caminho válido (não começa com #)
                if file_path_line and not file_path_line.startswith('#'):
                    # Extrair último diretório e nome do ficheiro
                    folder, filename = extract_folder_and_filename(file_path_line)
                    if folder and filename:
                        tracks.append((folder, filename))
        
        i += 1
    
    return tracks


def extract_folder_and_filename(full_path: str) -> Tuple[str, str]:
    """
    Extrai o último diretório e o nome do ficheiro de um caminho completo.
    
    Args:
        full_path: Caminho completo do ficheiro
        
    Returns:
        Tupla (folder, filename)
    """
    # Normalizar o caminho (remover espaços no início/fim)
    full_path = full_path.strip()
    
    # Remover aspas se existirem
    if full_path.startswith('"') and full_path.endswith('"'):
        full_path = full_path[1:-1]
    
    # Usar os.path para separar diretório e ficheiro
    directory = os.path.dirname(full_path)
    filename = os.path.basename(full_path)
    
    # Extrair apenas o último diretório
    if directory:
        folder = os.path.basename(directory)
    else:
        folder = ""
    
    return (folder, filename)

