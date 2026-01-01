"""
Aplicação principal - Interface gráfica para parser de ficheiros .m3u8

Este módulo implementa a interface gráfica usando tkinter para processar
ficheiros .m3u8 e gerar listas HTML formatadas.

Autor: Vinyl Playlist Parser
Versão: 1.0
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import webbrowser
from parser import parse_m3u8
from html_generator import generate_html, save_html


class M3U8ParserApp:
    """
    Classe principal da aplicação com interface gráfica.
    
    Gerencia toda a interface do utilizador, processamento de ficheiros
    e geração de HTML através de uma interface gráfica intuitiva.
    
    Atributos:
        root (tk.Tk): Janela principal da aplicação
        m3u8_file_path (str): Caminho do ficheiro .m3u8 selecionado
        tracks (List[Tuple[str, str]]): Lista de tracks processadas (folder, filename)
        html_file_path (str): Caminho do ficheiro HTML gerado
        file_label (tk.Label): Label que mostra o ficheiro selecionado
        parse_btn (tk.Button): Botão para processar o ficheiro
        generate_btn (tk.Button): Botão para gerar HTML
        open_btn (tk.Button): Botão para abrir HTML no navegador
        one_click_btn (tk.Button): Botão para processo de 1 clique
        preview_text (scrolledtext.ScrolledText): Área de texto para preview/status
        status_label (tk.Label): Barra de status na parte inferior
    """
    
    def __init__(self, root):
        """
        Inicializa a aplicação e configura a interface gráfica.
        
        Args:
            root (tk.Tk): Janela principal do tkinter
        """
        self.root = root
        self.root.title("Parser M3U8 para HTML")
        self.root.geometry("700x600")
        # Define tamanho mínimo para permitir redimensionamento
        self.root.minsize(600, 500)
        
        # Variáveis de estado da aplicação
        self.m3u8_file_path = None  # Caminho do ficheiro .m3u8 selecionado
        self.tracks = []  # Lista de tracks extraídas: [(folder, filename), ...]
        self.html_file_path = None  # Caminho do ficheiro HTML gerado
        
        # Configurar interface gráfica
        self.setup_ui()
    
    def setup_ui(self):
        """
        Configura todos os componentes da interface gráfica.
        
        Cria e organiza todos os widgets da aplicação:
        - Título da aplicação
        - Seletor de ficheiro
        - Botão de processo de 1 clique
        - Botões de ação individuais
        - Área de preview/status
        - Barra de status
        """
        # Frame principal que contém todos os elementos
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título da aplicação
        title_label = tk.Label(
            main_frame,
            text="Parser M3U8 para Lista HTML",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para seleção de ficheiro
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        # Label que mostra o ficheiro selecionado
        self.file_label = tk.Label(
            file_frame,
            text="Nenhum ficheiro selecionado",
            font=("Arial", 10),
            anchor="w",  # Alinhamento à esquerda
            bg="#f0f0f0",  # Cor de fundo cinza claro
            relief=tk.SUNKEN,  # Efeito de relevo afundado
            padx=10,
            pady=5
        )
        self.file_label.pack(fill=tk.X, side=tk.LEFT, expand=True)
        
        # Botão para selecionar ficheiro .m3u8
        select_btn = tk.Button(
            file_frame,
            text="Selecionar .m3u8",
            command=self.select_file,  # Callback quando clicado
            bg="#4CAF50",  # Cor verde
            fg="white",  # Texto branco
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5
        )
        select_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Frame para o botão de 1-clique (destaque visual)
        one_click_frame = tk.Frame(main_frame)
        one_click_frame.pack(fill=tk.X, pady=15)
        
        # Botão principal: processo de 1 clique (processa, gera e abre)
        self.one_click_btn = tk.Button(
            one_click_frame,
            text="⚡ Processar e Abrir HTML (1 Clique)",
            command=self.one_click_process,
            bg="#FF5722",  # Cor laranja/vermelho para destaque
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=12,
            state=tk.DISABLED,  # Desabilitado até selecionar ficheiro
            cursor="hand2"  # Cursor de mão ao passar por cima
        )
        self.one_click_btn.pack(fill=tk.X)
        
        # Separador visual entre botão principal e botões secundários
        separator = tk.Frame(main_frame, height=2, bg="#ccc")
        separator.pack(fill=tk.X, pady=10)
        
        # Label informativo para botões manuais
        manual_label = tk.Label(
            main_frame,
            text="Ou use os botões individuais:",
            font=("Arial", 9),
            fg="#666"  # Cor cinza
        )
        manual_label.pack(pady=(0, 5))
        
        # Frame para botões de ação individuais
        action_frame = tk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=5)
        
        # Botão 1: Processar ficheiro (extrair tracks)
        self.parse_btn = tk.Button(
            action_frame,
            text="Processar Ficheiro",
            command=self.process_file,
            bg="#2196F3",  # Cor azul
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            state=tk.DISABLED  # Desabilitado até selecionar ficheiro
        )
        self.parse_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão 2: Gerar HTML a partir das tracks processadas
        self.generate_btn = tk.Button(
            action_frame,
            text="Gerar HTML",
            command=self.generate_html,
            bg="#FF9800",  # Cor laranja
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            state=tk.DISABLED  # Desabilitado até processar ficheiro
        )
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão 3: Abrir HTML gerado no navegador
        self.open_btn = tk.Button(
            action_frame,
            text="Abrir HTML",
            command=self.open_html,
            bg="#9C27B0",  # Cor roxa
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            state=tk.DISABLED  # Desabilitado até gerar HTML
        )
        self.open_btn.pack(side=tk.LEFT)
        
        # Label para a área de preview
        preview_label = tk.Label(
            main_frame,
            text="Preview / Status:",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        preview_label.pack(fill=tk.X, pady=(20, 5))
        
        # Área de texto com scroll para mostrar preview e status
        self.preview_text = scrolledtext.ScrolledText(
            main_frame,
            height=15,  # Altura inicial em linhas
            font=("Consolas", 9),  # Fonte monoespaçada para melhor leitura
            wrap=tk.WORD,  # Quebra de linha por palavra
            bg="#fafafa",  # Fundo branco suave
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Barra de status na parte inferior da janela
        self.status_label = tk.Label(
            main_frame,
            text="Pronto",
            font=("Arial", 9),
            anchor="w",  # Alinhamento à esquerda
            bg="#e0e0e0",  # Cor de fundo cinza
            relief=tk.SUNKEN,
            padx=10,
            pady=3
        )
        self.status_label.pack(fill=tk.X, pady=(10, 0))
    
    def select_file(self):
        """
        Abre diálogo para selecionar ficheiro .m3u8.
        
        Permite ao utilizador escolher um ficheiro .m3u8 ou .m3u através
        de um diálogo de seleção de ficheiro. Após seleção, atualiza a
        interface e habilita os botões de processamento.
        """
        # Abrir diálogo de seleção de ficheiro
        file_path = filedialog.askopenfilename(
            title="Selecionar ficheiro .m3u8",
            filetypes=[
                ("Ficheiros M3U8", "*.m3u8"),
                ("Ficheiros M3U", "*.m3u"),
                ("Todos os ficheiros", "*.*")
            ]
        )
        
        # Se um ficheiro foi selecionado
        if file_path:
            self.m3u8_file_path = file_path
            filename = os.path.basename(file_path)
            
            # Atualizar interface
            self.file_label.config(text=f"Ficheiro: {filename}")
            self.parse_btn.config(state=tk.NORMAL)  # Habilitar botão de processar
            self.one_click_btn.config(state=tk.NORMAL)  # Habilitar botão de 1 clique
            self.update_status(f"Ficheiro selecionado: {filename}")
            
            # Limpar e atualizar área de preview
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, f"Ficheiro selecionado: {filename}\n")
            self.preview_text.insert(tk.END, f"Caminho completo: {file_path}\n\n")
            self.preview_text.insert(tk.END, "Clique em 'Processar e Abrir HTML (1 Clique)' para processar automaticamente,\n")
            self.preview_text.insert(tk.END, "ou use os botões individuais abaixo.\n")
    
    def process_file(self):
        """
        Processa o ficheiro .m3u8 e extrai as tracks.
        
        Lê o ficheiro selecionado, extrai informações sobre cada track
        e mostra um preview das primeiras 10 tracks na área de texto.
        Habilita o botão de gerar HTML após processamento bem-sucedido.
        
        Raises:
            Exception: Se houver erro ao processar o ficheiro
        """
        # Verificar se há ficheiro selecionado
        if not self.m3u8_file_path:
            messagebox.showwarning("Aviso", "Por favor, selecione um ficheiro primeiro.")
            return
        
        try:
            # Atualizar status e interface
            self.update_status("A processar ficheiro...")
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, "A processar ficheiro...\n\n")
            self.root.update()  # Atualizar interface para mostrar mudanças
            
            # Processar ficheiro usando o parser
            self.tracks = parse_m3u8(self.m3u8_file_path)
            
            # Verificar se foram encontradas tracks
            if not self.tracks:
                messagebox.showwarning("Aviso", "Nenhuma track foi encontrada no ficheiro.")
                self.update_status("Nenhuma track encontrada")
                return
            
            # Mostrar preview das tracks encontradas
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, f"Tracks encontradas: {len(self.tracks)}\n\n")
            self.preview_text.insert(tk.END, "Preview das primeiras 10 tracks:\n")
            self.preview_text.insert(tk.END, "-" * 70 + "\n\n")
            
            # Mostrar primeiras 10 tracks
            for i, (folder, filename) in enumerate(self.tracks[:10], 1):
                line = f"{folder} - {filename}\n"
                self.preview_text.insert(tk.END, line)
            
            # Se houver mais de 10 tracks, mostrar contador
            if len(self.tracks) > 10:
                self.preview_text.insert(tk.END, f"\n... e mais {len(self.tracks) - 10} tracks\n")
            
            # Habilitar botão de gerar HTML
            self.generate_btn.config(state=tk.NORMAL)
            self.update_status(f"Processado com sucesso: {len(self.tracks)} tracks encontradas")
            messagebox.showinfo("Sucesso", f"Ficheiro processado com sucesso!\n{len(self.tracks)} tracks encontradas.")
            
        except Exception as e:
            # Tratar erros e mostrar mensagem
            error_msg = f"Erro ao processar ficheiro:\n{str(e)}"
            messagebox.showerror("Erro", error_msg)
            self.update_status("Erro ao processar")
            self.preview_text.insert(tk.END, f"\nERRO: {error_msg}\n")
    
    def generate_html(self):
        """
        Gera o ficheiro HTML a partir das tracks processadas.
        
        Abre um diálogo para o utilizador escolher onde salvar o HTML,
        gera o conteúdo HTML formatado e salva o ficheiro. Habilita o
        botão de abrir HTML após geração bem-sucedida.
        
        Raises:
            Exception: Se houver erro ao gerar ou salvar o HTML
        """
        # Verificar se há tracks processadas
        if not self.tracks:
            messagebox.showwarning("Aviso", "Por favor, processe o ficheiro primeiro.")
            return
        
        # Determinar nome padrão do ficheiro HTML
        default_filename = "lista_tracks.html"
        if self.m3u8_file_path:
            # Usar nome do ficheiro .m3u8 como base
            base_name = os.path.splitext(os.path.basename(self.m3u8_file_path))[0]
            default_filename = f"{base_name}_lista.html"
        
        # Abrir diálogo para salvar ficheiro
        output_path = filedialog.asksaveasfilename(
            title="Salvar HTML como",
            defaultextension=".html",
            filetypes=[("Ficheiros HTML", "*.html"), ("Todos os ficheiros", "*.*")],
            initialfile=default_filename
        )
        
        # Se o utilizador cancelou, sair
        if not output_path:
            return
        
        try:
            # Atualizar status
            self.update_status("A gerar HTML...")
            self.root.update()
            
            # Obter título do nome do ficheiro (sem extensão)
            title = "Lista de Tracks"
            if self.m3u8_file_path:
                base_name = os.path.splitext(os.path.basename(self.m3u8_file_path))[0]
                title = base_name
            
            # Gerar conteúdo HTML
            html_content = generate_html(self.tracks, title)
            
            # Salvar ficheiro HTML
            save_html(html_content, output_path)
            
            # Atualizar estado e interface
            self.html_file_path = output_path
            self.open_btn.config(state=tk.NORMAL)  # Habilitar botão de abrir
            self.update_status(f"HTML gerado com sucesso: {os.path.basename(output_path)}")
            messagebox.showinfo("Sucesso", f"Ficheiro HTML gerado com sucesso!\n\n{output_path}")
            
        except Exception as e:
            # Tratar erros
            error_msg = f"Erro ao gerar HTML:\n{str(e)}"
            messagebox.showerror("Erro", error_msg)
            self.update_status("Erro ao gerar HTML")
    
    def open_html(self):
        """
        Abre o ficheiro HTML gerado no navegador padrão do sistema.
        
        Verifica se o ficheiro existe e abre no navegador usando
        o módulo webbrowser do Python.
        
        Raises:
            Exception: Se houver erro ao abrir o ficheiro
        """
        # Verificar se há ficheiro HTML gerado
        if not self.html_file_path or not os.path.exists(self.html_file_path):
            messagebox.showwarning("Aviso", "Nenhum ficheiro HTML foi gerado ainda.")
            return
        
        try:
            # Abrir ficheiro no navegador usando protocolo file://
            webbrowser.open(f"file://{os.path.abspath(self.html_file_path)}")
            self.update_status("HTML aberto no navegador")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir HTML:\n{str(e)}")
    
    def one_click_process(self):
        """
        Processo automatizado de 1 clique: processa, gera HTML e abre no navegador.
        
        Executa automaticamente os três passos principais:
        1. Processa o ficheiro .m3u8 e extrai as tracks
        2. Gera o HTML automaticamente (salva no mesmo diretório do .m3u8)
        3. Abre o HTML no navegador
        
        Este método oferece uma experiência mais rápida para o utilizador,
        eliminando a necessidade de múltiplos cliques e diálogos.
        
        Raises:
            Exception: Se houver erro em qualquer etapa do processo
        """
        # Verificar se há ficheiro selecionado
        if not self.m3u8_file_path:
            messagebox.showwarning("Aviso", "Por favor, selecione um ficheiro primeiro.")
            return
        
        try:
            # ========== PASSO 1: Processar ficheiro ==========
            self.update_status("A processar ficheiro...")
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, "Processo de 1 clique iniciado...\n\n")
            self.preview_text.insert(tk.END, "1. A processar ficheiro...\n")
            self.root.update()  # Atualizar interface
            
            # Processar ficheiro
            self.tracks = parse_m3u8(self.m3u8_file_path)
            
            # Verificar se foram encontradas tracks
            if not self.tracks:
                messagebox.showwarning("Aviso", "Nenhuma track foi encontrada no ficheiro.")
                self.update_status("Nenhuma track encontrada")
                return
            
            self.preview_text.insert(tk.END, f"   ✓ {len(self.tracks)} tracks encontradas\n\n")
            self.root.update()
            
            # ========== PASSO 2: Gerar HTML automaticamente ==========
            self.update_status("A gerar HTML...")
            self.preview_text.insert(tk.END, "2. A gerar HTML...\n")
            self.root.update()
            
            # Determinar caminho de saída (mesmo diretório do .m3u8)
            m3u8_dir = os.path.dirname(self.m3u8_file_path)
            m3u8_basename = os.path.splitext(os.path.basename(self.m3u8_file_path))[0]
            output_path = os.path.join(m3u8_dir, f"{m3u8_basename}_lista.html")
            
            # Obter título do nome do ficheiro (sem extensão)
            title = m3u8_basename
            
            # Gerar HTML
            html_content = generate_html(self.tracks, title)
            
            # Salvar ficheiro
            save_html(html_content, output_path)
            self.html_file_path = output_path
            
            self.preview_text.insert(tk.END, f"   ✓ HTML gerado: {os.path.basename(output_path)}\n\n")
            self.root.update()
            
            # ========== PASSO 3: Abrir no navegador ==========
            self.update_status("A abrir no navegador...")
            self.preview_text.insert(tk.END, "3. A abrir no navegador...\n")
            self.root.update()
            
            # Abrir HTML no navegador
            webbrowser.open(f"file://{os.path.abspath(output_path)}")
            
            # Mostrar conclusão
            self.preview_text.insert(tk.END, f"   ✓ Aberto no navegador\n\n")
            self.preview_text.insert(tk.END, "✓ Processo concluído com sucesso!\n")
            self.preview_text.insert(tk.END, f"\nFicheiro HTML: {output_path}\n")
            self.preview_text.insert(tk.END, "O ficheiro está pronto para impressão.\n")
            
            # Habilitar botões para uso futuro
            self.generate_btn.config(state=tk.NORMAL)
            self.open_btn.config(state=tk.NORMAL)
            self.update_status(f"Concluído: {len(self.tracks)} tracks processadas e HTML aberto")
            
        except Exception as e:
            # Tratar erros
            error_msg = f"Erro no processo:\n{str(e)}"
            messagebox.showerror("Erro", error_msg)
            self.update_status("Erro no processo")
            self.preview_text.insert(tk.END, f"\n✗ ERRO: {error_msg}\n")
    
    def update_status(self, message: str):
        """
        Atualiza a mensagem na barra de status.
        
        Args:
            message (str): Nova mensagem a exibir na barra de status
        """
        self.status_label.config(text=message)


def main():
    """
    Função principal que inicia a aplicação.
    
    Cria a janela principal do tkinter, instancia a aplicação
    e inicia o loop de eventos da interface gráfica.
    """
    # Criar janela principal
    root = tk.Tk()
    
    # Criar instância da aplicação
    app = M3U8ParserApp(root)
    
    # Iniciar loop de eventos (bloqueia até fechar a janela)
    root.mainloop()


if __name__ == "__main__":
    # Executar apenas se o ficheiro for executado diretamente
    main()
