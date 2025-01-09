import tkinter as tk
from tkinter import ttk
import pyperclip
import threading
import time
import pyautogui
import darkdetect

class GerenciadorClipboard:
    def __init__(self):
        self.historico_clipboard = []
        self.conteudo_atual = ""

    def monitorar_clipboard(self):
        while True:
            try:
                conteudo_clipboard = pyperclip.paste()
                if conteudo_clipboard and conteudo_clipboard != self.conteudo_atual:
                    self.conteudo_atual = conteudo_clipboard
                    if conteudo_clipboard not in self.historico_clipboard:
                        self.historico_clipboard.append(conteudo_clipboard)
                        app.atualizar_lista()
            except Exception as erro:
                print(f"Erro ao acessar o clipboard: {erro}")
            time.sleep(0.5)

class AplicacaoClipboard:
    def __init__(self, janela, gerenciador):
        self.janela = janela
        self.gerenciador = gerenciador

        # Remover barra de título padrão
        self.janela.overrideredirect(True)

        # Posicionar a janela onde o mouse está
        pos_x, pos_y = pyautogui.position()
        self.janela.geometry(f"400x300+{pos_x}+{pos_y}")

        # Configurar tema com base no sistema
        self.tema_escuro = darkdetect.isDark()
        bg_color = "#333333" if self.tema_escuro else "#e0e0e0"
        fg_color = "#ffffff" if self.tema_escuro else "#333333"
        self.janela.configure(bg=bg_color)

        self.configurar_estilo(fg_color, bg_color)
        self.criar_widgets(fg_color, bg_color)

        # Fechar com tecla ESC
        self.janela.bind("<Escape>", self.fechar_janela)

    def fechar_janela(self, event=None):
        self.janela.destroy()

    def configurar_estilo(self, fg_color, bg_color):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TButton", padding=5, font=("Arial", 10), background=bg_color, foreground=fg_color)
        estilo.configure("TLabel", font=("Arial", 14, "bold"), foreground=fg_color, background=bg_color)
        estilo.configure("TFrame", background=bg_color)

    def criar_widgets(self, fg_color, bg_color):
        # Frame para barra de título personalizada
        self.frame_titulo = tk.Frame(self.janela, bg=bg_color, relief="raised", bd=2)
        self.frame_titulo.pack(fill=tk.X)

        # Botão para fechar (X pequeno)
        self.botao_fechar = tk.Button(
            self.frame_titulo,
            text="X",
            font=("Arial", 10, "bold"),
            command=self.fechar_janela,
            bg=bg_color,
            fg=fg_color,
            bd=0,
            relief="flat"
        )
        self.botao_fechar.pack(side=tk.RIGHT, padx=5, pady=2)

        # Título personalizado
        self.label_titulo = tk.Label(
            self.frame_titulo,
            text="Gerenciador de Clipboard",
            font=("Arial", 12, "bold"),
            bg=bg_color,
            fg=fg_color
        )
        self.label_titulo.pack(side=tk.LEFT, padx=10)

        # Lista do histórico
        self.frame_lista = ttk.Frame(self.janela, padding=10)
        self.frame_lista.pack(fill=tk.BOTH, expand=True)

        self.lista = tk.Listbox(
            self.frame_lista,
            height=12,
            font=("Arial", 10),
            bg="#222222" if self.tema_escuro else "#ffffff",
            fg=fg_color,
            selectbackground="#4CAF50",
            selectforeground="#ffffff",
            relief="flat",
            borderwidth=0
        )
        self.lista.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.lista.bind("<Double-1>", self.copiar_e_fechar)

        # Botões de controle
        self.frame_botoes = ttk.Frame(self.janela)
        self.frame_botoes.pack(fill=tk.X, pady=10)

        # Botão de lixeira para limpar histórico
        self.botao_lixeira = tk.Button(
            self.frame_botoes,
            height=20,
            text="🗑️ limpar lista",  # Emoji de lixeira
            font=("Arial", 10, "bold"),
            command=self.limpar_historico,
            bg=bg_color,
            fg=fg_color,
            bd=0,
            relief="flat"
        )
        self.botao_lixeira.pack(side=tk.LEFT, padx=20)

        self.atualizar_lista()

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for item in reversed(self.gerenciador.historico_clipboard):
            self.lista.insert(tk.END, item)

    def copiar_e_fechar(self, evento):
        try:
            item_selecionado = self.lista.get(self.lista.curselection())
            pyperclip.copy(item_selecionado)
            self.fechar_janela()
        except Exception as erro:
            print(f"Erro ao copiar: {erro}")

    def limpar_historico(self):
        self.gerenciador.historico_clipboard.clear()
        self.atualizar_lista()

if __name__ == "__main__":
    gerenciador = GerenciadorClipboard()

    raiz = tk.Tk()
    app = AplicacaoClipboard(raiz, gerenciador)

    threading.Thread(target=gerenciador.monitorar_clipboard, daemon=True).start()

    raiz.mainloop()
