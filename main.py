"""
Aplicação principal - Interface gráfica para parser de ficheiros .m3u8
"""
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import webbrowser
from parser import parse_m3u8
from html_generator import generate_html, save_html


class M3U8ParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parser M3U8 para HTML")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)  # Tamanho mínimo para UI expansível
        
        self.m3u8_file_path = None
        self.tracks = []
        self.html_file_path = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface gráfica"""
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="Parser M3U8 para Lista HTML",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para seleção de ficheiro
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        self.file_label = tk.Label(
            file_frame,
            text="Nenhum ficheiro selecionado",
            font=("Arial", 10),
            anchor="w",
            bg="#f0f0f0",
            relief=tk.SUNKEN,
            padx=10,
            pady=5
        )
        self.file_label.pack(fill=tk.X, side=tk.LEFT, expand=True)
        
        select_btn = tk.Button(
            file_frame,
            text="Selecionar .m3u8",
            command=self.select_file,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5
        )
        select_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Botão de 1-clique (destaque)
        one_click_frame = tk.Frame(main_frame)
        one_click_frame.pack(fill=tk.X, pady=15)
        
        self.one_click_btn = tk.Button(
            one_click_frame,
            text="⚡ Processar e Abrir HTML (1 Clique)",
            command=self.one_click_process,
            bg="#FF5722",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=12,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.one_click_btn.pack(fill=tk.X)
        
        # Separador
        separator = tk.Frame(main_frame, height=2, bg="#ccc")
        separator.pack(fill=tk.X, pady=10)
        
        # Label para botões manuais
        manual_label = tk.Label(
            main_frame,
            text="Ou use os botões individuais:",
            font=("Arial", 9),
            fg="#666"
        )
        manual_label.pack(pady=(0, 5))
        
        # Frame para botões de ação
        action_frame = tk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=5)
        
        self.parse_btn = tk.Button(
            action_frame,
            text="Processar Ficheiro",
            command=self.process_file,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            state=tk.DISABLED
        )
        self.parse_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.generate_btn = tk.Button(
            action_frame,
            text="Gerar HTML",
            command=self.generate_html,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            state=tk.DISABLED
        )
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.open_btn = tk.Button(
            action_frame,
            text="Abrir HTML",
            command=self.open_html,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            state=tk.DISABLED
        )
        self.open_btn.pack(side=tk.LEFT)
        
        # Área de preview/status
        preview_label = tk.Label(
            main_frame,
            text="Preview / Status:",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        preview_label.pack(fill=tk.X, pady=(20, 5))
        
        self.preview_text = scrolledtext.ScrolledText(
            main_frame,
            height=15,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#fafafa",
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_label = tk.Label(
            main_frame,
            text="Pronto",
            font=("Arial", 9),
            anchor="w",
            bg="#e0e0e0",
            relief=tk.SUNKEN,
            padx=10,
            pady=3
        )
        self.status_label.pack(fill=tk.X, pady=(10, 0))
    
    def select_file(self):
        """Abre diálogo para selecionar ficheiro .m3u8"""
        file_path = filedialog.askopenfilename(
            title="Selecionar ficheiro .m3u8",
            filetypes=[("Ficheiros M3U8", "*.m3u8"), ("Ficheiros M3U", "*.m3u"), ("Todos os ficheiros", "*.*")]
        )
        
        if file_path:
            self.m3u8_file_path = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=f"Ficheiro: {filename}")
            self.parse_btn.config(state=tk.NORMAL)
            self.one_click_btn.config(state=tk.NORMAL)
            self.update_status(f"Ficheiro selecionado: {filename}")
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, f"Ficheiro selecionado: {filename}\n")
            self.preview_text.insert(tk.END, f"Caminho completo: {file_path}\n\n")
            self.preview_text.insert(tk.END, "Clique em 'Processar e Abrir HTML (1 Clique)' para processar automaticamente,\n")
            self.preview_text.insert(tk.END, "ou use os botões individuais abaixo.\n")
    
    def process_file(self):
        """Processa o ficheiro .m3u8 e extrai as tracks"""
        if not self.m3u8_file_path:
            messagebox.showwarning("Aviso", "Por favor, selecione um ficheiro primeiro.")
            return
        
        try:
            self.update_status("A processar ficheiro...")
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, "A processar ficheiro...\n\n")
            self.root.update()
            
            # Parse do ficheiro
            self.tracks = parse_m3u8(self.m3u8_file_path)
            
            if not self.tracks:
                messagebox.showwarning("Aviso", "Nenhuma track foi encontrada no ficheiro.")
                self.update_status("Nenhuma track encontrada")
                return
            
            # Mostrar preview
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, f"Tracks encontradas: {len(self.tracks)}\n\n")
            self.preview_text.insert(tk.END, "Preview das primeiras 10 tracks:\n")
            self.preview_text.insert(tk.END, "-" * 70 + "\n\n")
            
            for i, (folder, filename) in enumerate(self.tracks[:10], 1):
                line = f"{folder} - {filename}\n"
                self.preview_text.insert(tk.END, line)
            
            if len(self.tracks) > 10:
                self.preview_text.insert(tk.END, f"\n... e mais {len(self.tracks) - 10} tracks\n")
            
            self.generate_btn.config(state=tk.NORMAL)
            self.update_status(f"Processado com sucesso: {len(self.tracks)} tracks encontradas")
            messagebox.showinfo("Sucesso", f"Ficheiro processado com sucesso!\n{len(self.tracks)} tracks encontradas.")
            
        except Exception as e:
            error_msg = f"Erro ao processar ficheiro:\n{str(e)}"
            messagebox.showerror("Erro", error_msg)
            self.update_status("Erro ao processar")
            self.preview_text.insert(tk.END, f"\nERRO: {error_msg}\n")
    
    def generate_html(self):
        """Gera o ficheiro HTML"""
        if not self.tracks:
            messagebox.showwarning("Aviso", "Por favor, processe o ficheiro primeiro.")
            return
        
        # Diálogo para salvar HTML
        default_filename = "lista_tracks.html"
        if self.m3u8_file_path:
            base_name = os.path.splitext(os.path.basename(self.m3u8_file_path))[0]
            default_filename = f"{base_name}_lista.html"
        
        output_path = filedialog.asksaveasfilename(
            title="Salvar HTML como",
            defaultextension=".html",
            filetypes=[("Ficheiros HTML", "*.html"), ("Todos os ficheiros", "*.*")],
            initialfile=default_filename
        )
        
        if not output_path:
            return
        
        try:
            self.update_status("A gerar HTML...")
            self.root.update()
            
            # Obter título do nome do ficheiro (sem extensão)
            title = "Lista de Tracks"
            if self.m3u8_file_path:
                base_name = os.path.splitext(os.path.basename(self.m3u8_file_path))[0]
                title = base_name
            
            # Gerar HTML
            html_content = generate_html(self.tracks, title)
            
            # Salvar ficheiro
            save_html(html_content, output_path)
            
            self.html_file_path = output_path
            self.open_btn.config(state=tk.NORMAL)
            self.update_status(f"HTML gerado com sucesso: {os.path.basename(output_path)}")
            messagebox.showinfo("Sucesso", f"Ficheiro HTML gerado com sucesso!\n\n{output_path}")
            
        except Exception as e:
            error_msg = f"Erro ao gerar HTML:\n{str(e)}"
            messagebox.showerror("Erro", error_msg)
            self.update_status("Erro ao gerar HTML")
    
    def open_html(self):
        """Abre o ficheiro HTML no navegador"""
        if not self.html_file_path or not os.path.exists(self.html_file_path):
            messagebox.showwarning("Aviso", "Nenhum ficheiro HTML foi gerado ainda.")
            return
        
        try:
            webbrowser.open(f"file://{os.path.abspath(self.html_file_path)}")
            self.update_status("HTML aberto no navegador")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir HTML:\n{str(e)}")
    
    def one_click_process(self):
        """Processo de 1 clique: processa, gera HTML e abre no navegador"""
        if not self.m3u8_file_path:
            messagebox.showwarning("Aviso", "Por favor, selecione um ficheiro primeiro.")
            return
        
        try:
            # Passo 1: Processar ficheiro
            self.update_status("A processar ficheiro...")
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, "Processo de 1 clique iniciado...\n\n")
            self.preview_text.insert(tk.END, "1. A processar ficheiro...\n")
            self.root.update()
            
            self.tracks = parse_m3u8(self.m3u8_file_path)
            
            if not self.tracks:
                messagebox.showwarning("Aviso", "Nenhuma track foi encontrada no ficheiro.")
                self.update_status("Nenhuma track encontrada")
                return
            
            self.preview_text.insert(tk.END, f"   ✓ {len(self.tracks)} tracks encontradas\n\n")
            self.root.update()
            
            # Passo 2: Gerar HTML automaticamente
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
            
            # Passo 3: Abrir no navegador
            self.update_status("A abrir no navegador...")
            self.preview_text.insert(tk.END, "3. A abrir no navegador...\n")
            self.root.update()
            
            webbrowser.open(f"file://{os.path.abspath(output_path)}")
            
            self.preview_text.insert(tk.END, f"   ✓ Aberto no navegador\n\n")
            self.preview_text.insert(tk.END, "✓ Processo concluído com sucesso!\n")
            self.preview_text.insert(tk.END, f"\nFicheiro HTML: {output_path}\n")
            self.preview_text.insert(tk.END, "O ficheiro está pronto para impressão.\n")
            
            self.generate_btn.config(state=tk.NORMAL)
            self.open_btn.config(state=tk.NORMAL)
            self.update_status(f"Concluído: {len(self.tracks)} tracks processadas e HTML aberto")
            
        except Exception as e:
            error_msg = f"Erro no processo:\n{str(e)}"
            messagebox.showerror("Erro", error_msg)
            self.update_status("Erro no processo")
            self.preview_text.insert(tk.END, f"\n✗ ERRO: {error_msg}\n")
    
    def update_status(self, message: str):
        """Atualiza a barra de status"""
        self.status_label.config(text=message)


def main():
    """Função principal"""
    root = tk.Tk()
    app = M3U8ParserApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

