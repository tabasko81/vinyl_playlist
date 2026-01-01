"""
Parser para ficheiros .m3u8

Este módulo contém funções para ler e processar ficheiros .m3u8,
extraindo informações sobre cada track, especificamente o último
diretório e o nome do ficheiro de cada entrada na playlist.

Formato M3U8:
    O formato M3U8 é uma extensão do formato M3U (playlist de áudio).
    Cada track é definida por duas linhas:
    1. Linha #EXTINF: com metadados (duração, nome do artista, etc.)
    2. Linha com o caminho completo do ficheiro

Exemplo:
    #EXTINF:376,Spiller Feat. Sophie Ellis-Bextor - A1) Groove Jet pn
    O:\My Music\My Vinyl Rips\Spiller - _Mighty Miami E.P. [K089] (2000)\A1) Groove Jet_pn.flac

Autor: Vinyl Playlist Parser
Versão: 1.0
"""

import os
from typing import List, Tuple


def parse_m3u8(file_path: str) -> List[Tuple[str, str]]:
    """
    Lê um ficheiro .m3u8 e extrai o último diretório e nome do ficheiro de cada track.
    
    Esta função processa um ficheiro .m3u8 linha por linha, identifica as
    entradas de tracks (linhas #EXTINF: seguidas de caminhos de ficheiro) e
    extrai o último diretório e o nome do ficheiro de cada track.
    
    Args:
        file_path (str): Caminho completo para o ficheiro .m3u8 a processar
        
    Returns:
        List[Tuple[str, str]]: Lista de tuplas onde cada tupla contém:
            - folder (str): Nome do último diretório do caminho
            - filename (str): Nome do ficheiro (com extensão)
            
    Raises:
        ValueError: Se o ficheiro não puder ser lido com nenhum encoding suportado
        FileNotFoundError: Se o ficheiro não existir
        
    Exemplo:
        >>> tracks = parse_m3u8("playlist.m3u8")
        >>> print(tracks[0])
        ('Spiller - _Mighty Miami E.P. [K089] (2000)', 'A1) Groove Jet_pn.flac')
    """
    tracks = []  # Lista para armazenar as tracks extraídas
    
    # Lista de encodings a tentar (por ordem de preferência)
    # UTF-8 é o mais comum, mas alguns ficheiros podem usar Windows-1252 ou Latin-1
    encodings = ['utf-8', 'utf-8-sig', 'windows-1252', 'latin-1']
    content = None
    
    # Tentar ler o ficheiro com diferentes encodings
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.readlines()  # Ler todas as linhas do ficheiro
            break  # Se leitura bem-sucedida, sair do loop
        except (UnicodeDecodeError, UnicodeError):
            # Se falhar, tentar próximo encoding
            continue
    
    # Verificar se conseguiu ler o ficheiro
    if content is None:
        raise ValueError(
            f"Não foi possível ler o ficheiro {file_path} com nenhum encoding suportado"
        )
    
    # Processar o conteúdo linha a linha
    i = 0
    while i < len(content):
        line = content[i].strip()  # Remover espaços em branco no início/fim
        
        # Procurar linhas que começam com #EXTINF:
        # Estas linhas indicam o início de uma entrada de track
        if line.startswith('#EXTINF:'):
            # A próxima linha não vazia deve conter o caminho do ficheiro
            i += 1
            
            # Ignorar linhas vazias entre #EXTINF: e o caminho do ficheiro
            while i < len(content) and not content[i].strip():
                i += 1
            
            # Verificar se ainda há linhas para processar
            if i < len(content):
                file_path_line = content[i].strip()
                
                # Verificar se é um caminho válido (não começa com #)
                # Linhas que começam com # são comentários ou metadados
                if file_path_line and not file_path_line.startswith('#'):
                    # Extrair último diretório e nome do ficheiro
                    folder, filename = extract_folder_and_filename(file_path_line)
                    
                    # Adicionar à lista apenas se ambos os valores forem válidos
                    if folder and filename:
                        tracks.append((folder, filename))
        
        # Avançar para a próxima linha
        i += 1
    
    return tracks


def extract_folder_and_filename(full_path: str) -> Tuple[str, str]:
    """
    Extrai o último diretório e o nome do ficheiro de um caminho completo.
    
    Esta função processa um caminho de ficheiro completo e separa o último
    diretório do nome do ficheiro. Remove aspas se existirem e normaliza
    o caminho.
    
    Args:
        full_path (str): Caminho completo do ficheiro
            Exemplo: "O:\\My Music\\Album Name\\track.flac"
            Exemplo: '"O:\\My Music\\Album Name\\track.flac"'
        
    Returns:
        Tuple[str, str]: Tupla contendo:
            - folder (str): Nome do último diretório do caminho
            - filename (str): Nome do ficheiro (com extensão)
            
    Exemplo:
        >>> folder, filename = extract_folder_and_filename(
        ...     "O:\\My Music\\Album Name\\track.flac"
        ... )
        >>> print(folder)
        'Album Name'
        >>> print(filename)
        'track.flac'
    """
    # Normalizar o caminho (remover espaços no início/fim)
    full_path = full_path.strip()
    
    # Remover aspas se o caminho estiver entre aspas
    # Alguns ficheiros .m3u8 podem ter caminhos entre aspas
    if full_path.startswith('"') and full_path.endswith('"'):
        full_path = full_path[1:-1]  # Remover primeira e última aspas
    
    # Usar os.path para separar diretório e ficheiro
    # Esta abordagem funciona tanto para Windows quanto para Unix
    directory = os.path.dirname(full_path)  # Obter diretório completo
    filename = os.path.basename(full_path)  # Obter apenas o nome do ficheiro
    
    # Extrair apenas o último diretório (nome da pasta, não o caminho completo)
    if directory:
        # os.path.basename() em um diretório retorna o último componente
        folder = os.path.basename(directory)
    else:
        # Se não houver diretório (ficheiro na raiz), usar string vazia
        folder = ""
    
    return (folder, filename)
