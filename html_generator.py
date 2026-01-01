"""
Gerador de HTML formatado e print-ready para lista de tracks
"""
from datetime import datetime
from typing import List, Tuple


def generate_html(tracks: List[Tuple[str, str]], title: str = "Lista de Tracks") -> str:
    """
    Gera HTML formatado e print-ready a partir de uma lista de tracks.
    
    Args:
        tracks: Lista de tuplas (folder, filename)
        title: Título da página HTML
        
    Returns:
        String com o HTML completo
    """
    # Gerar data/hora atual
    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y %H:%M")
    
    # Construir lista de items
    items_html = []
    for folder, filename in tracks:
        item_text = f"{folder} - {filename}"
        items_html.append(f'        <div class="track-item">{item_text}</div>')
    
    items_content = "\n".join(items_html)
    
    # HTML completo com CSS inline para print-friendly
    html = f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
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
        
        .header {{
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #000;
        }}
        
        h1 {{
            font-size: 24pt;
            margin-bottom: 10px;
            color: #000;
        }}
        
        .date {{
            font-size: 10pt;
            color: #333;
        }}
        
        .tracks-list {{
            margin-top: 20px;
        }}
        
        .track-item {{
            padding: 8px 0;
            border-bottom: 1px solid #ddd;
            page-break-inside: avoid;
        }}
        
        .track-item:last-child {{
            border-bottom: none;
        }}
        
        /* Estilos para impressão */
        @media print {{
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
    
    Args:
        html_content: Conteúdo HTML como string
        output_path: Caminho onde salvar o ficheiro
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

