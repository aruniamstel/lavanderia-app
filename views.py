import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from decimal import Decimal
from models import Cliente, Item, OrdemServico, db

# --- Configuração de Estilos para Treeview ---

def configurar_estilo_treeview():
    """Configura o estilo do Treeview para tema dark"""
    style = ttk.Style()
    style.theme_use('clam')
    
    # Cores para tema dark
    bg_dark = "#1a1a1a"
    fg_dark = "#ffffff"
    bg_selected = "#2a2a2a"
    
    style.configure("Treeview",
                   background=bg_dark,
                   foreground=fg_dark,
                   fieldbackground=bg_dark,
                   borderwidth=0,
                   font=("Arial", 10))
    style.map("Treeview",
             background=[('selected', bg_selected)],
             foreground=[('selected', fg_dark)])
    
    style.configure("Treeview.Heading",
                   background="#2a2a2a",
                   foreground=fg_dark,
                   borderwidth=0,
                   font=("Arial", 10, "bold"))
    style.map("Treeview.Heading",
             background=[('active', '#3a3a3a')])


# --- CLASSE TELA DE CLIENTES ---

class TelaClientes(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        configurar_estilo_treeview()
        
        # Header
        self.criar_header()
        
        # Treeview Frame
        self.criar_treeview()
        
        # Botões de ação
        self.criar_botoes_acao()
        
        # Carrega dados
        self.carregar_clientes()
    
    def criar_header(self):
        """Cria barra superior com busca e botão Novo"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(header_frame, text="Gerenciamento de Clientes", 
                    font=("Arial", 20, "bold")).grid(row=0, column=0, sticky="w")
        
        # Busca
        ctk.CTkLabel(header_frame, text="Buscar:", font=("Arial", 11)).grid(row=0, column=1, sticky="e", padx=(0, 5))
        self.entry_busca = ctk.CTkEntry(header_frame, placeholder_text="Nome ou Telefone...", width=200)
        self.entry_busca.grid(row=0, column=2, sticky="e", padx=5)
        self.entry_busca.bind("<KeyRelease>", lambda e: self.buscar_clientes())
        
        # Botão Novo
        self.btn_novo = ctk.CTkButton(header_frame, text="+ Novo Cliente", 
                                     command=self.abrir_formulario_novo)
        self.btn_novo.grid(row=0, column=3, sticky="e", padx=5)
    
    def criar_treeview(self):
        """Cria a tabela de listagem"""
        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Nome", "Telefone", "Endereço"), 
                                 show="headings", yscrollcommand=scrollbar.set, height=15)
        scrollbar.config(command=self.tree.yview)
        
        # Definir colunas
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Nome", width=150, anchor="w")
        self.tree.column("Telefone", width=120, anchor="w")
        self.tree.column("Endereço", width=300, anchor="w")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Endereço", text="Endereço")
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<Double-1>", lambda e: self.abrir_formulario_editar())
    
    def criar_botoes_acao(self):
        """Cria botões de editar e excluir"""
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        self.btn_editar = ctk.CTkButton(btn_frame, text="✏️ Editar", 
                                       command=self.abrir_formulario_editar)
        self.btn_editar.pack(side="left", padx=5)
        
        self.btn_excluir = ctk.CTkButton(btn_frame, text="🗑️ Excluir", fg_color="#d32f2f",
                                        command=self.excluir_cliente)
        self.btn_excluir.pack(side="left", padx=5)
    
    def carregar_clientes(self):
        """Carrega clientes do banco de dados"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            clientes = Cliente.select()
            for cliente in clientes:
                self.tree.insert("", "end", values=(
                    cliente.id,
                    cliente.nome,
                    cliente.telefone,
                    cliente.endereco or "-"
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar clientes: {str(e)}")
    
    def buscar_clientes(self):
        """Busca clientes por nome ou telefone"""
        try:
            busca = self.entry_busca.get().lower()
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if not busca:
                self.carregar_clientes()
                return
            
            clientes = Cliente.select()
            for cliente in clientes:
                if busca in cliente.nome.lower() or busca in cliente.telefone.lower():
                    self.tree.insert("", "end", values=(
                        cliente.id,
                        cliente.nome,
                        cliente.telefone,
                        cliente.endereco or "-"
                    ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar: {str(e)}")
    
    def abrir_formulario_novo(self):
        """Abre formulário para criar novo cliente"""
        FormularioCliente(self, modo="novo", callback=self.carregar_clientes)
    
    def abrir_formulario_editar(self):
        """Abre formulário para editar cliente selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar.")
            return
        
        item_id = self.tree.item(selecionado)["values"][0]
        FormularioCliente(self, modo="editar", cliente_id=item_id, 
                         callback=self.carregar_clientes)
    
    def excluir_cliente(self):
        """Exclui cliente selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")
            return
        
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este cliente?"):
            try:
                item_id = self.tree.item(selecionado)["values"][0]
                cliente = Cliente.get_by_id(item_id)
                cliente.delete_instance()
                messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                self.carregar_clientes()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")


# --- CLASSE FORMULÁRIO DE CLIENTES ---

class FormularioCliente(ctk.CTkToplevel):
    def __init__(self, parent, modo="novo", cliente_id=None, callback=None):
        super().__init__(parent)
        self.title("Novo Cliente" if modo == "novo" else "Editar Cliente")
        
        # AJUSTE AQUI: Aumentamos de 350 para 450 para caber os botões com folga
        self.geometry("400x450") 
        
        self.resizable(False, False)
        self.modo = modo
        self.callback = callback
        self.cliente_id = cliente_id
        
        # Garante que a janela fique na frente (importante para Toplevel)
        self.grab_set() 
        
        self.criar_campos()
        
        if modo == "editar" and cliente_id:
            self.carregar_dados()
    
    def criar_campos(self):
        """Cria campos do formulário"""
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Nome
        ctk.CTkLabel(frame, text="Nome *", font=("Arial", 11)).pack(anchor="w", pady=(10, 0))
        self.entry_nome = ctk.CTkEntry(frame)
        self.entry_nome.pack(fill="x", pady=(5, 15))
        
        # Telefone com máscara
        ctk.CTkLabel(frame, text="Telefone * (XX) XXXXX-XXXX", font=("Arial", 11)).pack(anchor="w")
        self.entry_telefone = ctk.CTkEntry(frame)
        self.entry_telefone.pack(fill="x", pady=(5, 15))
        self.entry_telefone.bind("<KeyRelease>", self.formatar_telefone)
        
        ctk.CTkLabel(frame, text="Endereço", font=("Arial", 11)).pack(anchor="w")
        self.text_endereco = ctk.CTkTextbox(frame, height=80)
        self.text_endereco.pack(fill="x", pady=(5, 15))
        
        # Botões
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        btn_salvar = ctk.CTkButton(btn_frame, text="✓ Salvar", fg_color="#2ecc71", 
                                  text_color="#000000", font=("Arial", 11, "bold"),
                                  command=self.salvar)
        btn_salvar.pack(side="left", padx=5)
        
        btn_cancelar = ctk.CTkButton(btn_frame, text="✕ Cancelar", fg_color="#666666",
                                    command=self.destroy)
        btn_cancelar.pack(side="left", padx=5)
    
    def carregar_dados(self):
        """Carrega dados do cliente para edição"""
        try:
            cliente = Cliente.get_by_id(self.cliente_id)
            self.entry_nome.insert(0, cliente.nome)
            self.entry_telefone.insert(0, cliente.telefone)
            if cliente.endereco:
                self.text_endereco.insert("1.0", cliente.endereco)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
    
    def formatar_telefone(self, event):
        """Formata o telefone em tempo real: (XX) XXXXX-XXXX"""
        telefone = self.entry_telefone.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        
        if len(telefone) > 11:
            telefone = telefone[:11]
        
        # Formata conforme o usuário digita
        if len(telefone) == 0:
            novo_telefone = ""
        elif len(telefone) <= 2:
            novo_telefone = f"({telefone}"
        elif len(telefone) <= 7:
            novo_telefone = f"({telefone[:2]}) {telefone[2:]}"
        else:
            novo_telefone = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
        
        # Atualiza o campo sem disparar o evento novamente
        if self.entry_telefone.get() != novo_telefone:
            pos_cursor = len(self.entry_telefone.get())
            self.entry_telefone.delete(0, "end")
            self.entry_telefone.insert(0, novo_telefone)
            # Posiciona o cursor no final
            self.entry_telefone.icursor(len(novo_telefone))
    
    def salvar(self):
        """Salva ou atualiza cliente"""
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        endereco = self.text_endereco.get("1.0", "end-1c").strip()
        
        # Validação
        if not nome or not telefone:
            campos_vazios = []
            if not nome:
                campos_vazios.append("Nome")
            if not telefone:
                campos_vazios.append("Telefone")
            
            messagebox.showwarning("Campos Obrigatórios", 
                                 f"Preencha os seguintes campos: {', '.join(campos_vazios)}")
            return
        
        # Valida formato do telefone (deve ter apenas dígitos, mínimo 10)
        telefone_limpo = telefone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        if len(telefone_limpo) < 10:
            messagebox.showwarning("Telefone Inválido", 
                                 "Telefone deve ter pelo menos 10 dígitos!")
            return
        
        try:
            if self.modo == "novo":
                Cliente.create(nome=nome, telefone=telefone, endereco=endereco or None)
                messagebox.showinfo("Sucesso", "Cliente criado com sucesso!")
            else:
                cliente = Cliente.get_by_id(self.cliente_id)
                cliente.nome = nome
                cliente.telefone = telefone
                cliente.endereco = endereco or None
                cliente.save()
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            
            if self.callback:
                self.callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")


# --- CLASSE TELA DE ITENS ---

class TelaItens(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        configurar_estilo_treeview()
        
        # Header
        self.criar_header()
        
        # Treeview
        self.criar_treeview()
        
        # Botões
        self.criar_botoes_acao()
        
        # Carrega dados
        self.carregar_itens()
    
    def criar_header(self):
        """Cria barra superior"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(header_frame, text="Tabela de Preços (Itens)", 
                    font=("Arial", 20, "bold")).grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(header_frame, text="Buscar:", font=("Arial", 11)).grid(row=0, column=1, sticky="e", padx=(0, 5))
        self.entry_busca = ctk.CTkEntry(header_frame, placeholder_text="Nome do item...", width=200)
        self.entry_busca.grid(row=0, column=2, sticky="e", padx=5)
        self.entry_busca.bind("<KeyRelease>", lambda e: self.buscar_itens())
        
        self.btn_novo = ctk.CTkButton(header_frame, text="+ Novo Item", 
                                     command=self.abrir_formulario_novo)
        self.btn_novo.grid(row=0, column=3, sticky="e", padx=5)
    
    def criar_treeview(self):
        """Cria tabela de itens"""
        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Nome", "Preço"), 
                                show="headings", yscrollcommand=scrollbar.set, height=15)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Nome", width=300, anchor="w")
        self.tree.column("Preço", width=100, anchor="center")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Preço", text="Preço (R$)")
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<Double-1>", lambda e: self.abrir_formulario_editar())
    
    def criar_botoes_acao(self):
        """Cria botões de ação"""
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        self.btn_editar = ctk.CTkButton(btn_frame, text="✏️ Editar", 
                                       command=self.abrir_formulario_editar)
        self.btn_editar.pack(side="left", padx=5)
        
        self.btn_excluir = ctk.CTkButton(btn_frame, text="🗑️ Excluir", fg_color="#d32f2f",
                                        command=self.excluir_item)
        self.btn_excluir.pack(side="left", padx=5)
    
    def carregar_itens(self):
        """Carrega itens do banco"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            itens = Item.select()
            for item in itens:
                self.tree.insert("", "end", values=(
                    item.id,
                    item.nome,
                    f"R$ {item.preco:.2f}"
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar itens: {str(e)}")
    
    def buscar_itens(self):
        """Busca itens por nome"""
        try:
            busca = self.entry_busca.get().lower()
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if not busca:
                self.carregar_itens()
                return
            
            itens = Item.select()
            for item in itens:
                if busca in item.nome.lower():
                    self.tree.insert("", "end", values=(
                        item.id,
                        item.nome,
                        f"R$ {item.preco:.2f}"
                    ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar: {str(e)}")
    
    def abrir_formulario_novo(self):
        """Abre formulário novo"""
        FormularioItem(self, modo="novo", callback=self.carregar_itens)
    
    def abrir_formulario_editar(self):
        """Abre formulário de edição"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para editar.")
            return
        
        item_id = self.tree.item(selecionado)["values"][0]
        FormularioItem(self, modo="editar", item_id=item_id, 
                      callback=self.carregar_itens)
    
    def excluir_item(self):
        """Exclui item"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para excluir.")
            return
        
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este item?"):
            try:
                item_id = self.tree.item(selecionado)["values"][0]
                item = Item.get_by_id(item_id)
                item.delete_instance()
                messagebox.showinfo("Sucesso", "Item excluído com sucesso!")
                self.carregar_itens()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")


# --- CLASSE FORMULÁRIO DE ITENS ---

class FormularioItem(ctk.CTkToplevel):
    def __init__(self, parent, modo="novo", item_id=None, callback=None):
        super().__init__(parent)
        self.title("Novo Item" if modo == "novo" else "Editar Item")
        self.geometry("350x250")
        self.resizable(False, False)
        self.modo = modo
        self.callback = callback
        self.item_id = item_id
        
        self.criar_campos()
        
        if modo == "editar" and item_id:
            self.carregar_dados()
    
    def criar_campos(self):
        """Cria campos do formulário"""
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Nome do Item *", font=("Arial", 11)).pack(anchor="w", pady=(10, 0))
        self.entry_nome = ctk.CTkEntry(frame)
        self.entry_nome.pack(fill="x", pady=(5, 15))
        
        ctk.CTkLabel(frame, text="Preço (R$) *", font=("Arial", 11)).pack(anchor="w")
        self.entry_preco = ctk.CTkEntry(frame)
        self.entry_preco.pack(fill="x", pady=(5, 20))
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        btn_salvar = ctk.CTkButton(btn_frame, text="✓ Salvar", fg_color="#2ecc71",
                                  text_color="#000000", font=("Arial", 11, "bold"),
                                  command=self.salvar)
        btn_salvar.pack(side="left", padx=5)
        
        btn_cancelar = ctk.CTkButton(btn_frame, text="✕ Cancelar", fg_color="#666666",
                                    command=self.destroy)
        btn_cancelar.pack(side="left", padx=5)
    
    def carregar_dados(self):
        """Carrega dados do item"""
        try:
            item = Item.get_by_id(self.item_id)
            self.entry_nome.insert(0, item.nome)
            self.entry_preco.insert(0, f"{item.preco:.2f}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar: {str(e)}")
    
    def salvar(self):
        """Salva item"""
        nome = self.entry_nome.get().strip()
        preco_str = self.entry_preco.get().strip()
        
        # Validação
        if not nome or not preco_str:
            campos_vazios = []
            if not nome:
                campos_vazios.append("Nome")
            if not preco_str:
                campos_vazios.append("Preço")
            
            messagebox.showwarning("Campos Obrigatórios", 
                                 f"Preencha os seguintes campos: {', '.join(campos_vazios)}")
            return
        
        try:
            preco = Decimal(preco_str.replace(",", "."))
            
            if preco <= 0:
                messagebox.showwarning("Valor Inválido", "O preço deve ser maior que zero!")
                return
            
            if self.modo == "novo":
                Item.create(nome=nome, preco=preco)
                messagebox.showinfo("Sucesso", "Item criado com sucesso!")
            else:
                item = Item.get_by_id(self.item_id)
                item.nome = nome
                item.preco = preco
                item.save()
                messagebox.showinfo("Sucesso", "Item atualizado com sucesso!")
            
            if self.callback:
                self.callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")


# --- CLASSE TELA DE ORDENS DE SERVIÇO ---

class TelaOS(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        configurar_estilo_treeview()
        
        self.criar_header()
        self.criar_treeview()
        self.criar_botoes_acao()
        self.carregar_ordens()
    
    def criar_header(self):
        """Cria barra superior"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(header_frame, text="Ordens de Serviço", 
                    font=("Arial", 20, "bold")).grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(header_frame, text="Buscar:", font=("Arial", 11)).grid(row=0, column=1, sticky="e", padx=(0, 5))
        self.entry_busca = ctk.CTkEntry(header_frame, placeholder_text="Cliente ou ID...", width=200)
        self.entry_busca.grid(row=0, column=2, sticky="e", padx=5)
        self.entry_busca.bind("<KeyRelease>", lambda e: self.buscar_ordens())
        
        self.btn_novo = ctk.CTkButton(header_frame, text="+ Nova OS", 
                                     command=self.abrir_formulario_novo)
        self.btn_novo.grid(row=0, column=3, sticky="e", padx=5)
    
    def criar_treeview(self):
        """Cria tabela de OS"""
        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.tree = ttk.Treeview(tree_frame, 
                                columns=("ID", "Cliente", "Descrição", "Valor", "Status", "Entrega"), 
                                show="headings", yscrollcommand=scrollbar.set, height=15)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Cliente", width=150, anchor="w")
        self.tree.column("Descrição", width=200, anchor="w")
        self.tree.column("Valor", width=80, anchor="center")
        self.tree.column("Status", width=80, anchor="center")
        self.tree.column("Entrega", width=90, anchor="center")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Valor", text="Valor (R$)")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Entrega", text="Entrega")
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<Double-1>", lambda e: self.abrir_formulario_editar())
    
    def criar_botoes_acao(self):
        """Cria botões de ação"""
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        self.btn_editar = ctk.CTkButton(btn_frame, text="✏️ Editar", 
                                       command=self.abrir_formulario_editar)
        self.btn_editar.pack(side="left", padx=5)
        
        self.btn_excluir = ctk.CTkButton(btn_frame, text="🗑️ Excluir", fg_color="#d32f2f",
                                        command=self.excluir_os)
        self.btn_excluir.pack(side="left", padx=5)
    
    def carregar_ordens(self):
        """Carrega ordens do banco"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            ordens = OrdemServico.select()
            for ordem in ordens:
                self.tree.insert("", "end", values=(
                    ordem.id,
                    ordem.cliente.nome,
                    ordem.descricao[:40] + "..." if len(ordem.descricao) > 40 else ordem.descricao,
                    f"R$ {ordem.valor:.2f}",
                    ordem.status,
                    ordem.data_entrega.strftime("%d/%m/%Y")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar ordens: {str(e)}")
    
    def buscar_ordens(self):
        """Busca ordens"""
        try:
            busca = self.entry_busca.get().lower()
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if not busca:
                self.carregar_ordens()
                return
            
            ordens = OrdemServico.select()
            for ordem in ordens:
                if busca in ordem.cliente.nome.lower() or busca in str(ordem.id):
                    self.tree.insert("", "end", values=(
                        ordem.id,
                        ordem.cliente.nome,
                        ordem.descricao[:40] + "..." if len(ordem.descricao) > 40 else ordem.descricao,
                        f"R$ {ordem.valor:.2f}",
                        ordem.status,
                        ordem.data_entrega.strftime("%d/%m/%Y")
                    ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar: {str(e)}")
    
    def abrir_formulario_novo(self):
        """Abre formulário novo"""
        FormularioOS(self, modo="novo", callback=self.carregar_ordens)
    
    def abrir_formulario_editar(self):
        """Abre formulário de edição"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma ordem para editar.")
            return
        
        os_id = self.tree.item(selecionado)["values"][0]
        FormularioOS(self, modo="editar", os_id=os_id, callback=self.carregar_ordens)
    
    def excluir_os(self):
        """Exclui OS"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma ordem para excluir.")
            return
        
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir esta ordem?"):
            try:
                os_id = self.tree.item(selecionado)["values"][0]
                ordem = OrdemServico.get_by_id(os_id)
                ordem.delete_instance()
                messagebox.showinfo("Sucesso", "Ordem excluída com sucesso!")
                self.carregar_ordens()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")


# --- CLASSE FORMULÁRIO DE ORDENS DE SERVIÇO ---

class FormularioOS(ctk.CTkToplevel):
    def __init__(self, parent, modo="novo", os_id=None, callback=None):
        super().__init__(parent)
        self.title("Nova Ordem de Serviço" if modo == "novo" else "Editar Ordem de Serviço")
        self.geometry("500x650")
        self.resizable(False, False)
        self.modo = modo
        self.callback = callback
        self.os_id = os_id
        self.cliente_selecionado = None
        self.item_selecionado = None
        
        self.criar_campos()
        
        if modo == "editar" and os_id:
            self.carregar_dados()
    
    def criar_campos(self):
        """Cria campos do formulário"""
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cliente
        ctk.CTkLabel(frame, text="Cliente *", font=("Arial", 11)).pack(anchor="w", pady=(10, 0))
        self.combo_cliente = ctk.CTkComboBox(frame, state="readonly")
        self.combo_cliente.pack(fill="x", pady=(5, 15))
        self.carregar_clientes_combo()
        
        # Item/Preço
        ctk.CTkLabel(frame, text="Item (Serviço)", font=("Arial", 11)).pack(anchor="w")
        self.combo_item = ctk.CTkComboBox(frame, state="readonly", command=self.on_item_change)
        self.combo_item.pack(fill="x", pady=(5, 15))
        self.carregar_itens_combo()
        
        # Descrição
        ctk.CTkLabel(frame, text="Descrição *", font=("Arial", 11)).pack(anchor="w")
        self.text_descricao = ctk.CTkTextbox(frame, height=80)
        self.text_descricao.pack(fill="both", expand=True, pady=(5, 15))
        
        # Valor
        ctk.CTkLabel(frame, text="Valor (R$) *", font=("Arial", 11)).pack(anchor="w")
        self.entry_valor = ctk.CTkEntry(frame)
        self.entry_valor.pack(fill="x", pady=(5, 15))
        
        # Status
        ctk.CTkLabel(frame, text="Status *", font=("Arial", 11)).pack(anchor="w")
        self.combo_status = ctk.CTkComboBox(frame, values=["Pendente", "Pronto", "Entregue"], 
                                           state="readonly")
        self.combo_status.set("Pendente")
        self.combo_status.pack(fill="x", pady=(5, 15))
        
        # Data de Entrega
        ctk.CTkLabel(frame, text="Data de Entrega *", font=("Arial", 11)).pack(anchor="w")
        self.entry_data = ctk.CTkEntry(frame, placeholder_text="DD/MM/YYYY")
        self.entry_data.pack(fill="x", pady=(5, 15))
        
        # Botões
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        btn_salvar = ctk.CTkButton(btn_frame, text="✓ Salvar", fg_color="#2ecc71",
                                  text_color="#000000", font=("Arial", 11, "bold"),
                                  command=self.salvar)
        btn_salvar.pack(side="left", padx=5)
        
        btn_cancelar = ctk.CTkButton(btn_frame, text="✕ Cancelar", fg_color="#666666",
                                    command=self.destroy)
        btn_cancelar.pack(side="left", padx=5)
    
    def carregar_clientes_combo(self):
        """Carrega clientes no combobox"""
        try:
            clientes = Cliente.select()
            valores = [c.nome for c in clientes]
            self.combo_cliente.configure(values=valores)
            if valores:
                self.combo_cliente.set(valores[0])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar clientes: {str(e)}")
    
    def carregar_itens_combo(self):
        """Carrega itens no combobox"""
        try:
            itens = Item.select()
            valores = [f"{i.nome} (R$ {i.preco:.2f})" for i in itens]
            self.combo_item.configure(values=valores)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar itens: {str(e)}")
    
    def on_item_change(self, choice):
        """Atualiza valor quando item é selecionado"""
        try:
            if choice:
                item_nome = choice.split(" (R$")[0]
                item = Item.select().where(Item.nome == item_nome).first()
                if item:
                    self.entry_valor.delete(0, "end")
                    self.entry_valor.insert(0, f"{item.preco:.2f}")
        except Exception as e:
            pass
    
    def carregar_dados(self):
        """Carrega dados da ordem para edição"""
        try:
            ordem = OrdemServico.get_by_id(self.os_id)
            
            # Cliente
            self.combo_cliente.set(ordem.cliente.nome)
            
            # Descrição
            self.text_descricao.insert("1.0", ordem.descricao)
            
            # Valor
            self.entry_valor.insert(0, f"{ordem.valor:.2f}")
            
            # Status
            self.combo_status.set(ordem.status)
            
            # Data
            self.entry_data.insert(0, ordem.data_entrega.strftime("%d/%m/%Y"))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar: {str(e)}")
    
    def salvar(self):
        """Salva ordem"""
        cliente_nome = self.combo_cliente.get()
        descricao = self.text_descricao.get("1.0", "end-1c").strip()
        valor_str = self.entry_valor.get().strip()
        status = self.combo_status.get()
        data_str = self.entry_data.get().strip()
        
        # Validação - Descrição agora é opcional
        campos_vazios = []
        if not cliente_nome:
            campos_vazios.append("Cliente")
        if not valor_str:
            campos_vazios.append("Valor")
        if not data_str:
            campos_vazios.append("Data de Entrega")
        
        if campos_vazios:
            messagebox.showwarning("Campos Obrigatórios", 
                                 f"Preencha os seguintes campos: {', '.join(campos_vazios)}")
            return
        
        try:
            cliente = Cliente.select().where(Cliente.nome == cliente_nome).first()
            if not cliente:
                messagebox.showerror("Erro", "Cliente não encontrado!")
                return
            
            valor = Decimal(valor_str.replace(",", "."))
            
            if valor <= 0:
                messagebox.showwarning("Valor Inválido", "O valor da ordem deve ser maior que zero!")
                return
            
            data_entrega = datetime.strptime(data_str, "%d/%m/%Y").date()
            
            if self.modo == "novo":
                OrdemServico.create(
                    cliente=cliente,
                    descricao=descricao if descricao else "",  # Permite string vazia
                    valor=valor,
                    status=status,
                    data_entrega=data_entrega
                )
                messagebox.showinfo("Sucesso", "Ordem criada com sucesso!")
            else:
                ordem = OrdemServico.get_by_id(self.os_id)
                ordem.cliente = cliente
                ordem.descricao = descricao if descricao else ""  # Permite string vazia
                ordem.valor = valor
                ordem.status = status
                ordem.data_entrega = data_entrega
                ordem.save()
                messagebox.showinfo("Sucesso", "Ordem atualizada com sucesso!")
            
            if self.callback:
                self.callback()
            self.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Data inválida! Use o formato DD/MM/YYYY ou valor decimal inválido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
