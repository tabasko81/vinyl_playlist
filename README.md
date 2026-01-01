# Parser M3U8 para Lista HTML

Aplicação desktop em Python que lê ficheiros `.m3u8`, extrai informações sobre as tracks e gera uma lista formatada em HTML, pronta para impressão.

## Funcionalidades

- Lê ficheiros `.m3u8` e `.m3u`
- Extrai o último diretório e nome do ficheiro de cada track
- Formata como: `[Último Diretório] - [Nome do Ficheiro]`
- Gera HTML formatado e otimizado para impressão
- Interface gráfica intuitiva com tkinter
- **Processo de 1 clique**: Processa, gera HTML e abre automaticamente no navegador
- Título do HTML baseado no nome do ficheiro `.m3u8`

## Requisitos

- Python 3.6 ou superior
- tkinter (geralmente incluído com Python no Windows e Linux)

## Instalação

1. Certifique-se de que tem Python instalado:
   ```bash
   python --version
   ```

2. Clone ou descarregue este projeto

3. Não são necessárias dependências externas - o projeto utiliza apenas bibliotecas padrão do Python

## Utilização

1. Execute a aplicação:
   ```bash
   python main.py
   ```

2. Na interface gráfica:
   - Clique em "Selecionar .m3u8" para escolher o seu ficheiro
   - **Processo rápido (1 clique)**: Clique em "⚡ Processar e Abrir HTML (1 Clique)" para processar automaticamente, gerar o HTML e abrir no navegador
   - **Processo manual**: Use os botões individuais:
     - "Processar Ficheiro" para extrair as tracks
     - "Gerar HTML" para criar o ficheiro HTML
     - "Abrir HTML" para visualizar no navegador

## Formato de Saída

O ficheiro HTML gerado contém:
- Título da página
- Data e hora de geração
- Lista formatada: `[Último Diretório] - [Nome do Ficheiro]`
- CSS otimizado para impressão (margens adequadas, fontes legíveis)

## Exemplo

**Input (ficheiro .m3u8):**
```
#EXTINF:376,Spiller Feat. Sophie Ellis-Bextor - A1) Groove Jet pn
O:\My Music\My Vinyl Rips\Spiller - _Mighty Miami E.P. [K089] (2000)\A1) Groove Jet_pn.flac
```

**Output (HTML):**
```
Spiller - _Mighty Miami E.P. [K089] (2000) - A1) Groove Jet_pn.flac
```

## Estrutura do Projeto

```
Vinyl_playlist/
├── main.py              # Aplicação principal com UI
├── parser.py            # Lógica de parsing do .m3u8
├── html_generator.py    # Geração do HTML formatado
├── requirements.txt     # Dependências (vazio - usa biblioteca padrão)
└── README.md            # Este ficheiro
```

## Notas

- A aplicação suporta diferentes encodings de ficheiro (UTF-8, Windows-1252, Latin-1)
- O HTML gerado é otimizado para impressão com CSS `@media print`
- A interface mostra um preview das primeiras 10 tracks após o processamento
- O título do HTML é automaticamente definido como o nome do ficheiro `.m3u8` (sem extensão)
- O ficheiro HTML é salvo automaticamente no mesmo diretório do ficheiro `.m3u8` com o nome `[nome_do_ficheiro]_lista.html`
- A interface é redimensionável para melhor usabilidade

## Licença

Este projeto é fornecido como está, sem garantias.

