import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import pickle
import re
from PIL import Image

class SistemaGerenciamentoTarefas:
    def __init__(self, root):
        self.root = root
        self.root.title("SGT - Sistema de Gerenciamento de Tarefas")
        self.root.geometry("1050x610")
        self.root.iconbitmap("assets/Icon.png")  # Certifique-se de que o caminho esteja correto
        self.senha = "12345"
        self.tarefas = self.carregar_tarefas()
        self.tarefa_selecionada = None
        self.tarefa_selecionada_indice = None

        # Carregar imagem de fundo
        self.background_image = ctk.CTkImage(Image.open("assets/inicial.png"), size=(505, 610))
        
        self.tela_inicial()

    def carregar_fundo(self):
        label_background = ctk.CTkLabel(self.root, image=self.background_image)
        label_background.place(relwidth=1, relheight=1)

    def salvar_tarefas(self):
        with open('tarefas.pkl', 'wb') as file:
            pickle.dump(self.tarefas, file)

    def carregar_tarefas(self):
        try:
            with open('tarefas.pkl', 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return []

    def adicionar_botao_voltar(self, comando):
        btn_voltar = ctk.CTkButton(self.root, text="Voltar", font=("Arial", 12), command=comando, fg_color="#3A5357", hover_color="#2B4145")
        btn_voltar.place(x=10, y=10)

    def tela_inicial(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame_esquerda = ctk.CTkFrame(self.root, width=526, height=610, fg_color="white")
        frame_esquerda.place(x=0, y=0)
        
        frame_direita = ctk.CTkFrame(self.root, width=525, height=610, fg_color="#A0C4FF")
        frame_direita.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        label_imagem = ctk.CTkLabel(frame_esquerda, image=self.background_image)
        label_imagem.place(relx=0.5, rely=0.5, anchor="center")

        label_titulo = ctk.CTkLabel(frame_direita, text="Tasks To Do", font=("Roboto", 45), padx=10, pady=10, text_color="#312D6F")
        label_titulo.pack(pady=(80, 50))

        btn_add_tarefa = ctk.CTkButton(frame_direita, text="Adicionar Tarefa", font=("Arial", 12), width=245, height=44, command=self.tela_adicionar_tarefa, fg_color="#5856D6", hover_color="#4644ab")
        btn_add_tarefa.pack(pady=10)

        btn_ver_tarefas = ctk.CTkButton(frame_direita, text="Ver Todas as Tarefas", font=("Arial", 12), width=245, height=44, command=self.tela_lista_tarefas, fg_color="#5856D6", hover_color="#4644ab")
        btn_ver_tarefas.pack(pady=10)

        btn_redefinir_senha = ctk.CTkButton(frame_direita, text="Redefinir Senha", font=("Arial", 12), width=245, height=44, command=self.tela_solicitar_senha_redefinir, fg_color="#5856D6", hover_color="#4644ab")
        btn_redefinir_senha.pack(pady=10)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def tela_adicionar_tarefa(self):
        self.root.configure(bg="#8497F6")
        for widget in self.root.winfo_children():
            widget.destroy()

        frame_principal = ctk.CTkFrame(self.root, fg_color="#D6D6F5", corner_radius=10, width=1050, height=610)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame_principal, text="Cadastrar Tarefa", font=("Arial", 20, "bold"), text_color="#312D6F").pack(pady=(10, 20))
        
        ctk.CTkLabel(frame_principal, text="Nome", font=("Arial", 12), text_color="black", anchor="w").pack(fill="x", padx=20)
        nome_entry = ctk.CTkEntry(frame_principal, placeholder_text="Nome da tarefa", font=("Arial", 12), fg_color="#FFF", text_color="black", border_color="#555")
        nome_entry.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(frame_principal, text="Tipo", font=("Arial", 12), text_color="black", anchor="w").pack(fill="x", padx=20)
        tipo_var = ctk.StringVar()
        tipo_menu = ctk.CTkComboBox(frame_principal, variable=tipo_var, values=["Pessoal", "Empresarial", "Acadêmico"], font=("Arial", 12), fg_color="#FFF", text_color="black")
        tipo_menu.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(frame_principal, text="Descrição", font=("Arial", 12), text_color="black", anchor="w").pack(fill="x", padx=20)
        descricao_entry = ctk.CTkTextbox(frame_principal, font=("Arial", 12), height=60, fg_color="#FFF", text_color="black")
        descricao_entry.pack(fill="x", padx=20, pady=(0, 10))

        linha_inferior = ctk.CTkFrame(frame_principal, fg_color="#D6D6F5")
        linha_inferior.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(linha_inferior, text="Prazo", font=("Arial", 12), text_color="black", anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 10))
        prazo_entry = ctk.CTkEntry(linha_inferior, placeholder_text="dd/mm/yyyy", font=("Arial", 12), fg_color="#FFF", text_color="black")
        prazo_entry.grid(row=1, column=0, sticky="we")

        ctk.CTkLabel(linha_inferior, text="Status", font=("Arial", 12), text_color="black", anchor="w").grid(row=0, column=1, sticky="w", padx=(10, 0))
        status_var = ctk.StringVar(value="Em processo")
        status_menu = ctk.CTkComboBox(linha_inferior, variable=status_var, values=["Em processo", "Concluída", "Pendente"], font=("Arial", 12), fg_color="#FFF", text_color="black")
        status_menu.grid(row=1, column=1, sticky="we")

        btn_salvar = ctk.CTkButton(frame_principal, text="Salvar", font=("Arial", 12), width=200, fg_color="#4A3CB1", hover_color="#3A2B8C", command=lambda: self.salvar_tarefa(
            nome_entry.get(),
            tipo_var.get(),
            prazo_entry.get(),
            status_var.get(),
            descricao_entry.get("1.0", "end-1c")
        ))
        btn_salvar.pack(pady=(20, 10))


    def tela_lista_tarefas(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.adicionar_botao_voltar(self.tela_inicial)

        label = tk.Label(self.root, text="Lista de Tarefas", font=("Arial", 16))
        label.pack(pady=20)

        frame_lista = tk.Frame(self.root)
        frame_lista.pack(pady=10)

        colunas = ("Nome", "Tipo", "Prazo", "Prioridade", "Status")
        self.lista_tarefas = ttk.Treeview(frame_lista, columns=colunas, show='headings', height=13)
        self.lista_tarefas.column("Nome", width=195)
        self.lista_tarefas.column("Tipo", width=145)
        self.lista_tarefas.column("Prazo", width=195)
        self.lista_tarefas.column("Prioridade", width=145)
        self.lista_tarefas.column("Status", width=195)

        for col in colunas:
            self.lista_tarefas.heading(col, text=col)

        self.lista_tarefas.pack()

        for tarefa in self.tarefas:
            self.lista_tarefas.insert("", "end", values=(tarefa["nome"], tarefa["tipo"], tarefa["prazo"], tarefa["prioridade"], tarefa["status"]))

        if self.tarefa_selecionada_indice is not None:
            self.lista_tarefas.selection_set(self.tarefa_selecionada_indice)

        btn_ver_detalhes = tk.Button(self.root, text="Ver Detalhes da Tarefa", font=("Arial", 12), width=20, command=self.tela_detalhes_tarefa)
        btn_ver_detalhes.pack(pady=10)

        btn_marcar_concluida = tk.Button(self.root, text="Marcar como Concluída", font=("Arial", 12), width=20, command=self.marcar_concluida)
        btn_marcar_concluida.pack(pady=10)

        btn_editar_tarefa = tk.Button(self.root, text="Editar Tarefa", font=("Arial", 12), width=20, command=self.ver_descricao_tarefa)
        btn_editar_tarefa.pack(pady=10)

        btn_remover = tk.Button(self.root, text="Remover", font=("Arial", 12), width=20, command=self.tela_solicitar_senha_para_remover)
        btn_remover.pack(pady=10)

    def ver_descricao_tarefa(self):
        self.selecionar_tarefa()
        if self.tarefa_selecionada is None:
            messagebox.showerror("Erro", "Selecione uma tarefa para editar.")
            return
        self.tela_descricao_tarefa()

    def tela_detalhes_tarefa(self):
        self.selecionar_tarefa()
        if self.tarefa_selecionada is None:
            messagebox.showerror("Erro", "Selecione uma tarefa para ver os detalhes.")
            return

        tarefa = self.tarefas[self.tarefa_selecionada]

        for widget in self.root.winfo_children():
            widget.destroy()

        self.adicionar_botao_voltar(self.tela_lista_tarefas)

        tk.Label(self.root, text="Detalhes da Tarefa", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Nome: {tarefa['nome']}", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.root, text="Descrição:", font=("Arial", 14)).pack(pady=5)

        descricao_entry = tk.Text(self.root, font=("Arial", 12), height=5, width=40)
        descricao_entry.insert("1.0", tarefa["descricao"])
        descricao_entry.config(state="disabled")
        descricao_entry.pack(pady=10)

    def tela_descricao_tarefa(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.adicionar_botao_voltar(self.tela_lista_tarefas)

        tarefa = self.tarefas[self.tarefa_selecionada]

        tk.Label(self.root, text="Editar Tarefa", font=("Arial", 16)).pack(pady=5)
        tk.Label(self.root, text="Nome da Tarefa", font=("Arial", 12)).pack(pady=5)
        nome_entry = tk.Entry(self.root, font=("Arial", 12))
        nome_entry.insert(0, tarefa["nome"])
        nome_entry.pack(pady=5)

        tk.Label(self.root, text="Tipo da Tarefa", font=("Arial", 12)).pack(pady=5)
        tipo_var = tk.StringVar(value=tarefa["tipo"])
        tipo_menu = ttk.Combobox(self.root, textvariable=tipo_var, values=["Pessoal", "Empresarial", "Acadêmico"], font=("Arial", 12), state="readonly")
        tipo_menu.pack(pady=5)

        tk.Label(self.root, text="Prazo", font=("Arial", 12)).pack(pady=5)
        prazo_entry = tk.Entry(self.root, font=("Arial", 12))
        prazo_entry.insert(0, tarefa["prazo"])
        prazo_entry.pack(pady=5)

        tk.Label(self.root, text="Prioridade", font=("Arial", 12)).pack(pady=5)
        prioridade_var = tk.StringVar(value=tarefa["prioridade"])
        prioridade_menu = ttk.Combobox(self.root, textvariable=prioridade_var, values=["Baixa", "Média", "Alta"], font=("Arial", 12), state="readonly")
        prioridade_menu.pack(pady=5)

        tk.Label(self.root, text="Status", font=("Arial", 12)).pack(pady=5)
        status_var = tk.StringVar(value=tarefa["status"])
        status_menu = ttk.Combobox(self.root, textvariable=status_var, values=["Pendente", "Concluída", "Parcialmente Concluída"], font=("Arial", 12), state="readonly")
        status_menu.pack(pady=5)

        tk.Label(self.root, text="Descrição", font=("Arial", 12)).pack(pady=5)
        descricao_entry = tk.Text(self.root, font=("Arial", 12), height=5, width=40)
        descricao_entry.insert("1.0", tarefa["descricao"])
        descricao_entry.pack(pady=5)

        # Mapear Enter para mover entre os campos na tela de edição
        nome_entry.bind("<Return>", lambda event: self.mover_proximo_campo(event, nome_entry, tipo_menu))
        tipo_menu.bind("<Return>", lambda event: self.mover_proximo_campo(event, tipo_menu, prazo_entry))
        prazo_entry.bind("<Return>", lambda event: self.validar_prazo(event, prazo_entry, prioridade_menu))
        prioridade_menu.bind("<Return>", lambda event: self.mover_proximo_campo(event, prioridade_menu, status_menu))
        status_menu.bind("<Return>", lambda event: self.mover_proximo_campo(event, status_menu, descricao_entry))
        descricao_entry.bind("<Return>", lambda event: self.salvar_edicao_tarefa(nome_entry.get(), tipo_var.get(), prazo_entry.get(), prioridade_var.get(), status_var.get(), descricao_entry.get("1.0", "end-1c")))

        btn_salvar = tk.Button(self.root, text="Salvar Alterações", font=("Arial", 12), width=20,
                               command=lambda: self.salvar_edicao_tarefa(nome_entry.get(), tipo_var.get(), prazo_entry.get(),
                                                                         prioridade_var.get(), status_var.get(), descricao_entry.get("1.0", "end-1c")))
        btn_salvar.pack(pady=20)

    def salvar_edicao_tarefa(self, nome, tipo, prazo, prioridade, status, descricao):
        if not nome or not tipo or not prazo or not prioridade or not status or not descricao.strip():
            messagebox.showerror("Erro", "Preencha todos os campos.")
        elif not re.match(r"\d{2}/\d{2}/\d{4}", prazo):
            messagebox.showerror("Erro", "A data deve estar no formato dd/mm/yyyy.")
        else:
            self.tarefas[self.tarefa_selecionada] = {"nome": nome, "tipo": tipo, "prazo": prazo, "prioridade": prioridade, "status": status, "descricao": descricao}
            self.salvar_tarefas()
            messagebox.showinfo("Sucesso", "Tarefa editada com sucesso!")
            self.tela_lista_tarefas()

    def selecionar_tarefa(self):
        try:
            selected_item = self.lista_tarefas.selection()[0]
            self.tarefa_selecionada = self.lista_tarefas.index(selected_item)
            self.tarefa_selecionada_indice = selected_item  # Armazena o identificador da tarefa
        except IndexError:
            self.tarefa_selecionada = None
            self.tarefa_selecionada_indice = None

    def tela_solicitar_senha_para_remover(self):
     self.selecionar_tarefa()

     if self.tarefa_selecionada is None:
        messagebox.showerror("Erro", "Selecione uma tarefa para remover.")
        return

     senha_popup = tk.Toplevel(self.root)
     senha_popup.title("Autenticação de Senha")
     senha_popup.geometry("300x150")
     senha_popup.resizable(False, False)

     self.centralizar_janela_popover(senha_popup)

     tk.Label(senha_popup, text="Digite a senha para remover a tarefa:", font=("Arial", 12)).pack(pady=10)

     senha_entry = tk.Entry(senha_popup, show="*", font=("Arial", 12))
     senha_entry.pack(pady=5, ipadx=10, ipady=2)
     senha_entry.focus()  # Foco automático no campo de senha

    # Função para verificar a senha e remover a tarefa
     def acao_remover_tarefa():
        if senha_entry.get() == self.senha:
            senha_popup.destroy()  # Fecha a janela de senha
            self.remover_tarefa()  # Remove a tarefa
        else:
            messagebox.showerror("Erro", "Senha incorreta!")

    # Bind para pressionar "Enter" e remover a tarefa
     senha_entry.bind("<Return>", lambda event: acao_remover_tarefa())

    # Botão para confirmar e remover a tarefa
     btn_confirmar = tk.Button(senha_popup, text="Confirmar", font=("Arial", 12),
                              command=acao_remover_tarefa)
     btn_confirmar.pack(pady=10)

    def centralizar_janela_popover(self, popup):
        popup_width = 300
        popup_height = 150
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    def verificar_senha(self, senha_digitada, popup, acao_sucesso):
        if senha_digitada == self.senha:
            popup.destroy()
            acao_sucesso()
        else:
            messagebox.showerror("Erro", "Senha incorreta!")

    def remover_tarefa(self):
        self.tarefas.pop(self.tarefa_selecionada)
        self.salvar_tarefas()
        messagebox.showinfo("Sucesso", "Tarefa removida com sucesso.")
        self.tela_lista_tarefas()

    def tela_solicitar_senha_redefinir(self):
     senha_popup = tk.Toplevel(self.root)
     senha_popup.title("Autenticação de Senha")
     senha_popup.geometry("300x150")
     senha_popup.resizable(False, False)

     self.centralizar_janela_popover(senha_popup)

     tk.Label(senha_popup, text="Digite a senha para redefinir:", font=("Arial", 12)).pack(pady=10)
     senha_entry = tk.Entry(senha_popup, show="*", font=("Arial", 12))
     senha_entry.pack(pady=5, ipadx=10, ipady=2)
     senha_entry.focus()  # Foco automático no campo de senha

     senha_entry.bind("<Return>", lambda event: self.verificar_senha(senha_entry.get(), senha_popup, self.tela_redefinir_senha))

     btn_confirmar = tk.Button(senha_popup, text="Confirmar", font=("Arial", 12), 
                              command=lambda: self.verificar_senha(senha_entry.get(), senha_popup, self.tela_redefinir_senha))
     btn_confirmar.pack(pady=10)


    def tela_redefinir_senha(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.adicionar_botao_voltar(self.tela_inicial)

        tk.Label(self.root, text="Redefinição de Senha", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Senha atual:", font=("Arial", 12)).pack(pady=5)
        senha_atual_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        senha_atual_entry.pack(pady=5)

        tk.Label(self.root, text="Nova senha:", font=("Arial", 12)).pack(pady=5)
        nova_senha_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        nova_senha_entry.pack(pady=5)

        tk.Label(self.root, text="Confirmar nova senha:", font=("Arial", 12)).pack(pady=5)
        confirmar_nova_senha_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        confirmar_nova_senha_entry.pack(pady=5)

        btn_salvar_senha = tk.Button(self.root, text="Redefinir Senha", font=("Arial", 12),
                                     command=lambda: self.redefinir_senha(senha_atual_entry.get(), nova_senha_entry.get(), confirmar_nova_senha_entry.get()))
        btn_salvar_senha.pack(pady=20)

    def tela_redefinir_senha(self):
     for widget in self.root.winfo_children():
        widget.destroy()

     self.adicionar_botao_voltar(self.tela_inicial)

     tk.Label(self.root, text="Redefinição de Senha", font=("Arial", 16)).pack(pady=10)

    # Campo da senha atual
     tk.Label(self.root, text="Senha atual:", font=("Arial", 12)).pack(pady=5)
     senha_atual_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
     senha_atual_entry.pack(pady=5)
     senha_atual_entry.focus()  # Foco automático no campo de senha atual

    # Campo da nova senha
     tk.Label(self.root, text="Nova senha:", font=("Arial", 12)).pack(pady=5)
     nova_senha_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
     nova_senha_entry.pack(pady=5)

    # Campo para confirmar a nova senha
     tk.Label(self.root, text="Confirmar nova senha:", font=("Arial", 12)).pack(pady=5)
     confirmar_nova_senha_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
     confirmar_nova_senha_entry.pack(pady=5)

    # Função para redefinir a senha com validação
     def acao_redefinir_senha():
        senha_atual = senha_atual_entry.get()
        nova_senha = nova_senha_entry.get()
        confirmar_nova_senha = confirmar_nova_senha_entry.get()

        # Verifica se algum campo está vazio
        if not senha_atual.strip() or not nova_senha.strip() or not confirmar_nova_senha.strip():
            messagebox.showerror("Erro", "Preencha todos os campos!")
        # Verifica se a senha atual está correta
        elif senha_atual == self.senha:
            # Verifica se a nova senha é igual à senha atual
            if nova_senha == self.senha:
                messagebox.showerror("Erro", "A nova senha não pode ser a mesma que a senha atual!")
            # Verifica se as senhas não coincidem
            elif nova_senha != confirmar_nova_senha:
                messagebox.showerror("Erro", "As senhas não coincidem!")
            # Se a nova senha for válida, redefine a senha
            else:
                self.senha = nova_senha
                messagebox.showinfo("Sucesso", "Senha redefinida com sucesso!")
                self.tela_inicial()  # Retorna à tela inicial
        else:
            messagebox.showerror("Erro", "Senha atual incorreta!")

    # Bind para mover o foco e redefinir senha ao pressionar "Enter"
     senha_atual_entry.bind("<Return>", lambda event: nova_senha_entry.focus())  # Pressiona "Enter" e vai para nova senha
     nova_senha_entry.bind("<Return>", lambda event: confirmar_nova_senha_entry.focus())  # Vai para o campo de confirmar senha
     confirmar_nova_senha_entry.bind("<Return>", lambda event: acao_redefinir_senha())  # Redefine a senha ao pressionar "Enter"

    # Botão para redefinir senha
     btn_salvar_senha = tk.Button(self.root, text="Redefinir Senha", font=("Arial", 12),
                                 command=acao_redefinir_senha)
     btn_salvar_senha.pack(pady=20)

    def marcar_concluida(self):
        self.selecionar_tarefa()
        if self.tarefa_selecionada is None:
            messagebox.showerror("Erro", "Selecione uma tarefa para alterar o status.")
            return

        status_atual = self.tarefas[self.tarefa_selecionada]['status']
        if status_atual == "Pendente":
            self.tarefas[self.tarefa_selecionada]['status'] = "Parcialmente Concluída"
        elif status_atual == "Parcialmente Concluída":
            self.tarefas[self.tarefa_selecionada]['status'] = "Concluída"
        else:
            self.tarefas[self.tarefa_selecionada]['status'] = "Pendente"

        self.salvar_tarefas()
        messagebox.showinfo("Sucesso", f"Tarefa marcada como {self.tarefas[self.tarefa_selecionada]['status']}.")
        self.tela_lista_tarefas()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaGerenciamentoTarefas(root)
    root.mainloop()
