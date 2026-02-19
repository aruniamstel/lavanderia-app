import customtkinter as ctk
from models import Cliente

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Caçula - Cadastro de Clientes")
        self.geometry("400x500")

        # --- Elementos da Interface ---
        self.label_titulo = ctk.CTkLabel(self, text="Novo Cliente", font=("Roboto", 20, "bold"))
        self.label_titulo.pack(pady=20)

        # Campo Nome
        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Nome Completo", width=300)
        self.entry_nome.pack(pady=10)

        # Campo Telefone
        self.entry_fone = ctk.CTkEntry(self, placeholder_text="Telefone (41) 99999-9999", width=300)
        self.entry_fone.pack(pady=10)

        # Campo Endereço (Textbox para ser maior)
        self.label_end = ctk.CTkLabel(self, text="Endereço (Opcional):")
        self.label_end.pack()
        self.entry_endereco = ctk.CTkTextbox(self, width=300, height=80)
        self.entry_endereco.pack(pady=10)

        # Botão Salvar
        self.btn_salvar = ctk.CTkButton(self, text="Salvar no Banco", command=self.salvar_cliente)
        self.btn_salvar.pack(pady=20)

    def salvar_cliente(self):
        # 1. Captura os dados da tela
        nome = self.entry_nome.get()
        fone = self.entry_fone.get()
        # No Textbox do CTk, você pega do início "1.0" até o fim "end"
        end = self.entry_endereco.get("1.0", "end-1c")

        if nome and fone:
            # 2. Salva no SQLite via Peewee (muito simples!)
            novo_cliente = Cliente.create(nome=nome, telefone=fone, endereco=end)
            
            # 3. Feedback visual (no console por enquanto)
            print(f"✅ Cliente {novo_cliente.nome} salvo com ID {novo_cliente.id}!")
            
            # Limpa os campos
            self.entry_nome.delete(0, 'end')
            self.entry_fone.delete(0, 'end')
            self.entry_endereco.delete("1.0", "end")
        else:
            print("❌ Preencha nome e telefone!")

if __name__ == "__main__":
    app = App()
    app.mainloop()