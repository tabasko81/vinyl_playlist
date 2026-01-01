"""
Gerador de HTML formatado e print-ready para lista de tracks

Este módulo gera ficheiros HTML formatados a partir de uma lista de tracks,
criando documentos otimizados para visualização e impressão. O HTML gerado
inclui formatação especial onde o nome da pasta aparece em negrito e o
nome do ficheiro aparece destacado em amarelo com fonte diferente.

Autor: Vinyl Playlist Parser
Versão: 1.0
"""

from datetime import datetime
from typing import List, Tuple


def generate_html(tracks: List[Tuple[str, str]], title: str = "Lista de Tracks") -> str:
    """
    Gera HTML formatado e print-ready a partir de uma lista de tracks.
    
    Cria um documento HTML completo com CSS inline, otimizado para impressão.
    Cada track é formatada com o nome da pasta em negrito e o nome do
    ficheiro destacado em amarelo com fonte monoespaçada.
    
    Args:
        tracks (List[Tuple[str, str]]): Lista de tuplas contendo:
            - folder (str): Nome do último diretório
            - filename (str): Nome do ficheiro
        title (str, optional): Título da página HTML. 
            Por padrão usa "Lista de Tracks".
        
    Returns:
        str: String contendo o HTML completo pronto para ser salvo
        
    Exemplo:
        >>> tracks = [
        ...     ("Album Name", "track1.flac"),
        ...     ("Album Name", "track2.flac")
        ... ]
        >>> html = generate_html(tracks, "Minha Playlist")
        >>> # html contém o HTML completo como string
    """
    # Gerar data e hora atual para exibir no documento
    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y %H:%M")  # Formato: DD/MM/YYYY HH:MM
    
    # Construir lista de items HTML
    # Cada track será um div com spans separados para folder e filename
    items_html = []
    for folder, filename in tracks:
        # Criar HTML para cada track:
        # - folder-name: span com nome da pasta (será formatado em negrito)
        # - file-name: span com nome do ficheiro (será destacado em amarelo)
        item_html = (
            f'        <div class="track-item">'
            f'<span class="folder-name">{folder}</span> - '
            f'<span class="file-name">{filename}</span>'
            f'</div>'
        )
        items_html.append(item_html)
    
    # Juntar todos os items em uma única string com quebras de linha
    items_content = "\n".join(items_html)
    
    # HTML completo com CSS inline para print-friendly
    # O CSS está inline para garantir que o ficheiro seja autocontido
    html = f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* Reset CSS básico */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        /* Estilos do corpo do documento */
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #000;
            background: #fff;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        /* Cabeçalho da página */
        .header {{
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #000;
        }}
        
        /* Título principal */
        h1 {{
            font-size: 24pt;
            margin-bottom: 10px;
            color: #000;
        }}
        
        /* Data de geração */
        .date {{
            font-size: 10pt;
            color: #333;
        }}
        
        /* Container da lista de tracks */
        .tracks-list {{
            margin-top: 20px;
        }}
        
        /* Item individual de track */
        .track-item {{
            padding: 8px 0;
            border-bottom: 1px solid #ddd;
            page-break-inside: avoid;  /* Evitar quebra de página dentro de um item */
        }}
        
        /* Remover borda do último item */
        .track-item:last-child {{
            border-bottom: none;
        }}
        
        /* Nome da pasta: negrito, fonte padrão */
        .folder-name {{
            font-weight: bold;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        /* Nome do ficheiro: fundo amarelo, fonte monoespaçada */
        .file-name {{
            background-color: #ffff00;  /* Amarelo */
            color: #000;
            font-family: 'Courier New', Courier, monospace;  /* Fonte diferente */
            font-weight: normal;  /* Não negrito */
            padding: 2px 4px;  /* Espaçamento interno para melhor legibilidade */
        }}
        
        /* Estilos específicos para impressão */
        @media print {{
            /* Ajustes de layout para impressão */
            body {{
                padding: 15mm;
                max-width: 100%;
            }}
            
            .header {{
                margin-bottom: 20px;
            }}
            
            h1 {{
                font-size: 20pt;
            }}
            
            .track-item {{
                padding: 6px 0;
                font-size: 11pt;
            }}
            
            /* Garantir que o fundo amarelo apareça na impressão */
            .file-name {{
                background-color: #ffff00;
                -webkit-print-color-adjust: exact;  /* Chrome/Safari */
                print-color-adjust: exact;  /* Firefox/Standard */
            }}
            
            /* Margens da página */
            @page {{
                margin: 15mm;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <div class="date">Gerado em: {date_str}</div>
    </div>
    
    <div class="tracks-list">
{items_content}
    </div>
</body>
</html>"""
    
    return html


def save_html(html_content: str, output_path: str) -> None:
    """
    Salva o conteúdo HTML num ficheiro.
    
    Escreve o conteúdo HTML fornecido num ficheiro no caminho especificado.
    O ficheiro é salvo com encoding UTF-8 para suportar caracteres especiais.
    
    Args:
        html_content (str): Conteúdo HTML completo como string
        output_path (str): Caminho completo onde salvar o ficheiro HTML
        
    Raises:
        IOError: Se houver erro ao escrever o ficheiro
        PermissionError: Se não tiver permissão para escrever no diretório
        
    Exemplo:
        >>> html = generate_html(tracks, "Minha Playlist")
        >>> save_html(html, "output.html")
    """
    # Abrir ficheiro para escrita com encoding UTF-8
    # 'w' = modo escrita (sobrescreve se o ficheiro existir)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
