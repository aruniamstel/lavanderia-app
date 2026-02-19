import customtkinter as ctk
from views import TelaClientes, TelaItens, TelaOS

# --- Classe Tela de Início ---

class TelaInicio(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Título
        titulo_frame = ctk.CTkFrame(self, fg_color="transparent")
        titulo_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=30)
        
        ctk.CTkLabel(titulo_frame, text="Bem-vindo, Luis! 👋", 
                    font=("Arial", 28, "bold")).pack()
        ctk.CTkLabel(titulo_frame, text="Sistema de Gestão - Caçula Lavanderia", 
                    font=("Arial", 14), text_color="#999999").pack(pady=(5, 0))
        
        # Cards de atalho
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        cards_frame.grid_rowconfigure(0, weight=1)
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Card Clientes
        card1 = self.criar_card(cards_frame, "👥 Clientes", 
                               "Gerencie seus clientes",
                               lambda: controller.mostrar_tela("clientes"))
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Card Itens
        card2 = self.criar_card(cards_frame, "📋 Itens/Preços", 
                               "Configure tabela de preços",
                               lambda: controller.mostrar_tela("itens"))
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Card OS
        card3 = self.criar_card(cards_frame, "📦 Ordens de Serviço", 
                               "Gerecie suas ordens",
                               lambda: controller.mostrar_tela("os"))
        card3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
    
    def criar_card(self, parent, titulo, descricao, comando):
        """Cria um card de atalho"""
        card = ctk.CTkFrame(parent, fg_color="#2a2a2a", corner_radius=10)
        
        btn = ctk.CTkButton(card, text=titulo, font=("Arial", 14, "bold"),
                          fg_color="transparent", hover_color="#3a3a3a",
                          command=comando)
        btn.pack(fill="both", expand=True, padx=15, pady=15)
        
        desc_label = ctk.CTkLabel(card, text=descricao, font=("Arial", 10),
                                 text_color="#999999")
        desc_label.pack(side="bottom", padx=10, pady=(0, 10))
        
        return card

# --- Janela Principal ---

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Caçula Lavanderia - Sistema de Gestão")
        self.geometry("1000x700")
        ctk.set_appearance_mode("dark")
        
        # 1. Navbar Superior
        self.navbar = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="#1a1a1a")
        self.navbar.pack(side="top", fill="x")
        self.navbar.pack_propagate(False)
        
        # Logo/Título na navbar
        ctk.CTkLabel(self.navbar, text="🧺 Caçula Lavanderia", 
                    font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=10)
        
        self.btn_home = ctk.CTkButton(self.navbar, text="🏠 Início", width=100, 
                                     command=lambda: self.mostrar_tela("inicio"))
        self.btn_home.pack(side="left", padx=5, pady=10)

        self.btn_cli = ctk.CTkButton(self.navbar, text="👥 Clientes", width=100, 
                                    command=lambda: self.mostrar_tela("clientes"))
        self.btn_cli.pack(side="left", padx=5, pady=10)

        self.btn_item = ctk.CTkButton(self.navbar, text="📋 Itens/Preços", width=120, 
                                     command=lambda: self.mostrar_tela("itens"))
        self.btn_item.pack(side="left", padx=5, pady=10)

        self.btn_os = ctk.CTkButton(self.navbar, text="📦 Ordens de Serviço", width=150, 
                                   command=lambda: self.mostrar_tela("os"))
        self.btn_os.pack(side="left", padx=5, pady=10)

        # 2. Container de Conteúdo
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.tela_atual = None
        self.mostrar_tela("inicio")

    def mostrar_tela(self, nome_tela):
        """Alterna entre telas"""
        # Remove tela anterior
        if self.tela_atual:
            self.tela_atual.destroy()

        # Cria nova tela
        if nome_tela == "inicio":
            self.tela_atual = TelaInicio(self.container, self)
        elif nome_tela == "clientes":
            self.tela_atual = TelaClientes(self.container)
        elif nome_tela == "itens":
            self.tela_atual = TelaItens(self.container)
        elif nome_tela == "os":
            self.tela_atual = TelaOS(self.container)

        self.tela_atual.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()