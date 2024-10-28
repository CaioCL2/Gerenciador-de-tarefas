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
        self.root.geometry("900x600")
        self.root.resizable(False, False)  # Impede o redimensionamento da janela

        # Centraliza a janela na tela
        self.centralizar_janela()

        # Senha padrão
        self.senha = "12345"

        # Carregar as tarefas do arquivo
        self.tarefas = self.carregar_tarefas()
        self.tarefa_selecionada = None
        self.tarefa_selecionada_indice = None
        
        # Carregar imagem de fundo
        self.background_image = ctk.CTkImage(Image.open("assets/inicial.png"), size=(505, 610))
        self.icone_check = ctk.CTkImage(Image.open("assets/Check circle.png"), size=(30, 30))  # ícone de "check"
        self.icone_caneta = ctk.CTkImage(Image.open("assets/Pen.png"), size=(30, 30))   # ícone de caneta

        # Exibe a tela inicial
        self.tela_inicial()
        
    def carregar_fundo(self):
        label_background = ctk.CTkLabel(self.root, image=self.background_image)
        label_background.place(relwidth=1, relheight=1)
        
    def centralizar_janela(self):
        width = 900
        height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

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
        btn_voltar = ctk.CTkButton(self.root, text="Voltar", font=("Arial", 12), command=comando)
        btn_voltar.place(x=10, y=10)

    def tela_inicial(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.tarefa_selecionada = None
        self.tarefa_selecionada_indice = None
        
        
        frame_esquerda = ctk.CTkFrame(self.root, width=450, height=600, fg_color="white")
        frame_esquerda.place(x=0, y=0)
        
        frame_direita = ctk.CTkFrame(self.root, width=450, height=600, fg_color="#A0C4FF")
        frame_direita.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        label_imagem = ctk.CTkLabel(frame_esquerda, image=self.background_image)
        label_imagem.place(relx=0.5, rely=0.5, anchor="center")
        
         # Ícones acima do título
        icone_check_label = ctk.CTkLabel(frame_direita, image=self.icone_check, text="")
        icone_check_label.place(relx=0.11, y=170)
        
         # Ícones acima do título
        icone_check_label = ctk.CTkLabel(frame_direita, image=self.icone_check, text="")
        icone_check_label.place(relx=0.11, y=235)
        
         # Ícones acima do título
        icone_check_label = ctk.CTkLabel(frame_direita, image=self.icone_check, text="")
        icone_check_label.place(relx=0.11, y=300)
        
        icone_caneta_label = ctk.CTkLabel(frame_direita, image=self.icone_caneta, text="")
        icone_caneta_label.place(relx=0.7, y=35)

        label = ctk.CTkLabel(frame_direita, text="Tasks To Do", font=("Roboto", 45), text_color="#312D6F")
        label.pack(pady=(60, 40))

        btn_add_tarefa = ctk.CTkButton(frame_direita, text="Adicionar Tarefa", font=("Arial", 12), width=245, height=44, command=self.tela_adicionar_tarefa, fg_color="#5856D6", hover_color="#4644ab")
        btn_add_tarefa.pack(pady=10)

        btn_ver_tarefas = ctk.CTkButton(frame_direita, text="Ver Todas as Tarefas", font=("Arial", 12), width=245, height=44, command=self.tela_lista_tarefas, fg_color="#5856D6", hover_color="#4644ab")
        btn_ver_tarefas.pack(pady=10)

        btn_redefinir_senha = ctk.CTkButton(frame_direita, text="Redefinir Senha", font=("Arial", 12), width=245, height=44, command=self.tela_solicitar_senha_redefinir, fg_color="#5856D6", hover_color="#4644ab")
        btn_redefinir_senha.pack(pady=10)

    def mover_proximo_campo(self, event, campo_atual, campo_proximo):
        if campo_atual.get() == "":
            messagebox.showerror("Erro", "Este campo não pode ficar em branco.")
        else:
            campo_proximo.focus()

    def validar_prazo(self, event, campo_prazo, proximo_campo):
        if not re.match(r"\d{2}/\d{2}/\d{4}", campo_prazo.get()):
            messagebox.showerror("Erro", "A data deve estar no formato dd/mm/yyyy.")
        else:
            proximo_campo.focus()

    def salvar_ao_press_enter(self, event, nome, tipo, prazo, prioridade, status, descricao):
        self.salvar_tarefa(nome.get(), tipo.get(), prazo.get(), prioridade.get(), status.get(), descricao.get("1.0", "end-1c"))

    def tela_adicionar_tarefa(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame_principal = ctk.CTkFrame(self.root, fg_color="#D6D6F5", corner_radius=10, width=900, height=600)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        self.adicionar_botao_voltar(self.tela_inicial)
        ctk.CTkLabel(frame_principal, text="Cadastrar Tarefa", font=("Arial", 20, "bold"), text_color="#312D6F").pack(pady=(10,20))
        
        ctk.CTkLabel(frame_principal, text="Nome", font=("Arial", 12), text_color="black", anchor="w").pack(fill="x", padx=20)
        nome_entry = ctk.CTkEntry(frame_principal, placeholder_text="Nome da tarefa", font=("Arial", 12), height=35, fg_color="#FFF", text_color="black", border_color="#555")
        nome_entry.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(frame_principal, text="Tipo", font=("Arial", 12), text_color="black", anchor="w").pack(fill="x", padx=20)
        tipo_var = ctk.StringVar()
        tipo_menu = ctk.CTkComboBox(frame_principal, variable=tipo_var, values=["Pessoal", "Empresarial", "Acadêmico"], font=("Arial", 12), height=35, fg_color="#FFF", text_color="black")
        tipo_menu.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(frame_principal, text="Prioridade", font=("Arial", 12), text_color="black", anchor="w").pack(fill="x", padx=20)
        prioridade_var = ctk.StringVar()
        prioridade_menu = ctk.CTkComboBox(frame_principal, variable=prioridade_var, values=["Baixa", "Média", "Alta"], font=("Arial", 12), height=35, state="readonly", fg_color="#FFF", text_color="black")
        prioridade_menu.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(frame_principal, text="Descrição", font=("Arial", 12), text_color="black", anchor="w").pack(fill="x", padx=20)
        descricao_entry = ctk.CTkTextbox(frame_principal, font=("Arial", 12), height=100, fg_color="#FFF", text_color="black")
        descricao_entry.pack(fill="x", padx=20, pady=(0, 10))

        linha_inferior = ctk.CTkFrame(frame_principal, fg_color="#D6D6F5")
        linha_inferior.pack(fill="x", padx=70, pady=(0, 10))

        ctk.CTkLabel(linha_inferior, text="Prazo", font=("Arial", 12), text_color="black", anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 10))
        prazo_entry = ctk.CTkEntry(linha_inferior, placeholder_text="dd/mm/yyyy", font=("Arial", 12), width=200, height=35, fg_color="#FFF", text_color="black")
        prazo_entry.grid(row=1, column=0, sticky="w")

        ctk.CTkLabel(linha_inferior, text="Status", font=("Arial", 12), text_color="black", anchor="w").grid(row=0, column=1, sticky="e", padx=(0, 165))
        status_var = ctk.StringVar(value="Em processo")
        status_menu = ctk.CTkComboBox(linha_inferior, variable=status_var, values=["Em processo", "Concluída", "Pendente"], font=("Arial", 12), width=200, height=35, fg_color="#FFF", text_color="black")
        status_menu.grid(row=1, column=1, sticky="e")

        # Configura as colunas para expandir conforme o frame
        linha_inferior.columnconfigure(0, weight=1)
        linha_inferior.columnconfigure(1, weight=1)

        nome_entry.bind("<Return>", lambda event: self.mover_proximo_campo(event, nome_entry, tipo_menu))
        tipo_menu.bind("<Return>", lambda event: self.mover_proximo_campo(event, tipo_menu, prazo_entry))
        prazo_entry.bind("<Return>", lambda event: self.validar_prazo(event, prazo_entry, prioridade_menu))
        prioridade_menu.bind("<Return>", lambda event: self.mover_proximo_campo(event, prioridade_menu, status_menu))
        status_menu.bind("<Return>", lambda event: self.mover_proximo_campo(event, status_menu, descricao_entry))
        descricao_entry.bind("<Return>", lambda event: self.salvar_ao_press_enter(event, nome_entry, tipo_var, prazo_entry, prioridade_var, status_var, descricao_entry))

        btn_salvar = ctk.CTkButton(frame_principal, text="Salvar Tarefa", font=("Arial", 12), width=200, fg_color="#4A3CB1", hover_color="#3A2B8C", command=lambda: self.salvar_tarefa(nome_entry.get(), tipo_var.get(), prazo_entry.get(), prioridade_var.get(),status_var.get(), descricao_entry.get("1.0", "end-1c")))
        btn_salvar.pack(pady=20)

    def salvar_tarefa(self, nome, tipo, prazo, prioridade, status, descricao):
        if not nome or not tipo or not prazo or not prioridade or not status or not descricao.strip():
            messagebox.showerror("Erro", "Preencha todos os campos.")
        elif not re.match(r"\d{2}/\d{2}/\d{4}", prazo):
            messagebox.showerror("Erro", "A data deve estar no formato dd/mm/yyyy.")
        else:
            self.tarefas.append({"nome": nome, "tipo": tipo, "prazo": prazo, "prioridade": prioridade, "status": status, "descricao": descricao})
            self.salvar_tarefas()
            messagebox.showinfo("Sucesso", "Tarefa cadastrada com sucesso!")
            self.tela_inicial()

    def tela_lista_tarefas(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    
        # Configurações principais
        frame_principal = ctk.CTkFrame(self.root, fg_color="#D6D6F5", corner_radius=10)
        frame_principal.pack(fill="both", expand=True)
        
        self.adicionar_botao_voltar(self.tela_inicial)

        # Título da página
        label = ctk.CTkLabel(frame_principal, text="Lista de Tarefas", font=("Arial", 20, "bold"),     text_color="#312D6F")
        label.pack(pady=(10, 20))

        # Frame da lista de tarefas
        frame_lista = ctk.CTkFrame(frame_principal, fg_color="#E8E8F5", corner_radius=10)
        frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

        # Configuração da Treeview
        colunas = ("Nome", "Tipo", "Prazo", "Prioridade", "Status")
        self.lista_tarefas = ttk.Treeview(frame_lista, columns=colunas, show='headings', height=13)
        self.lista_tarefas.column("Nome", width=150, anchor="center")
        self.lista_tarefas.column("Tipo", width=100, anchor="center")
        self.lista_tarefas.column("Prazo", width=150, anchor="center")
        self.lista_tarefas.column("Prioridade", width=100, anchor="center")
        self.lista_tarefas.column("Status", width=150, anchor="center")

        for col in colunas:
            self.lista_tarefas.heading(col, text=col)

        self.lista_tarefas.pack(fill="both", expand=True, padx=10, pady=10)

        # Inserindo tarefas
        for tarefa in self.tarefas:
            self.lista_tarefas.insert("", "end", values=(tarefa["nome"], tarefa["tipo"], tarefa["prazo"],  tarefa["prioridade"], tarefa["status"]))

        if self.tarefa_selecionada_indice in self.lista_tarefas.get_children():
          self.lista_tarefas.selection_set(self.tarefa_selecionada_indice)


        # Botões para ações na lista
        frame_botoes = ctk.CTkFrame(frame_principal, fg_color="#D6D6F5")
        frame_botoes.pack(pady=(10, 20), padx=20)

        btn_editar_tarefa = ctk.CTkButton(frame_botoes, text="Editar tarefa", font=("Arial", 12), width=150,   fg_color="#645CBB", text_color="#FFFFFF", command=self.ver_descricao_tarefa)
        btn_editar_tarefa.grid(row=0, column=0, padx=10, pady=10)

        btn_ver_detalhes = ctk.CTkButton(frame_botoes, text="Detalhes", font=("Arial", 12), width=150,     fg_color="#645CBB", text_color="#FFFFFF", command=self.tela_detalhes_tarefa)
        btn_ver_detalhes.grid(row=0, column=1, padx=10, pady=10)

        btn_marcar_concluida = ctk.CTkButton(frame_botoes, text="Marcar como concluída", font=("Arial", 12),   width=150, fg_color="#645CBB", text_color="#FFFFFF", command=self.marcar_concluida)
        btn_marcar_concluida.grid(row=1, column=0, padx=10, pady=10)

        btn_remover = ctk.CTkButton(frame_botoes, text="Excluir", font=("Arial", 12), width=150,   fg_color="#645CBB", text_color="#FFFFFF", command=self.tela_solicitar_senha_para_remover)
        btn_remover.grid(row=1, column=1, padx=10, pady=10)

    def ver_descricao_tarefa(self):
        self.selecionar_tarefa()
        if self.tarefa_selecionada is None:
            messagebox.showerror("Erro", "Selecione uma tarefa para editar.")
            return
        self.tela_descricao_tarefa()

    def tela_detalhes_tarefa(self):
        # Seleciona a tarefa
        self.selecionar_tarefa()
        if self.tarefa_selecionada is None:
            messagebox.showerror("Erro", "Selecione uma tarefa para ver os detalhes.")
            return

        tarefa = self.tarefas[self.tarefa_selecionada]

        # Limpa a tela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Adiciona botão para voltar
    
        # Frame principal para centralizar o conteúdo
        frame_principal = ctk.CTkFrame(self.root, fg_color="#D6D6F5", corner_radius=10)
        frame_principal.pack(fill="both", expand=True)

        self.adicionar_botao_voltar(self.tela_lista_tarefas)
        
        # Título
        titulo_label = ctk.CTkLabel(frame_principal, text="Detalhes da Tarefa", font=("Arial", 20, "bold"), text_color="#312D6F")
        titulo_label.pack(pady=(10, 20))

        # Detalhes da tarefa
        ctk.CTkLabel(frame_principal, text=f"Nome: {tarefa['nome']}", font=("Arial", 14), text_color="black").pack(pady=(5, 10))
        ctk.CTkLabel(frame_principal, text="Descrição:", font=("Arial", 14), text_color="black").pack(pady=(5, 10))

        # Textbox para a descrição
        descricao_entry = ctk.CTkTextbox(frame_principal, font=("Arial", 12), height=100, fg_color="#FFF", text_color="black", corner_radius=5)
        descricao_entry.insert("1.0", tarefa["descricao"])
        descricao_entry.configure(state="disabled")
        descricao_entry.pack(fill="x", padx=20, pady=(0, 20))

    def tela_descricao_tarefa(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame_principal = ctk.CTkFrame(self.root, fg_color="#D6D6F5", corner_radius=10, width=900, height=600)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        self.adicionar_botao_voltar(self.tela_lista_tarefas)
        
        tarefa = self.tarefas[self.tarefa_selecionada]
        
        ctk.CTkLabel(frame_principal, text="Cadastrar Tarefa", font=("Arial", 20, "bold"), text_color="#312D6F").pack(pady=(10,20))
        
        ctk.CTkLabel(frame_principal, text="Nome", font=("Arial", 12), text_color="black", anchor="w").pack(fill="x", padx=20)
        nome_entry = ctk.CTkEntry(frame_principal, placeholder_text="Nome da tarefa", font=("Arial", 12), fg_color="#FFF", text_color="black", border_color="#555")
        nome_entry.insert(0, tarefa["nome"])
        nome_entry.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(frame_principal, text="Tipo", font=("Arial", 12), text_color="black", anchor="w").pack(fill="x", padx=20)
        tipo_var = ctk.StringVar(value=tarefa["tipo"])
        tipo_menu = ctk.CTkComboBox(frame_principal, variable=tipo_var, values=["Pessoal", "Empresarial", "Acadêmico"], font=("Arial", 12), fg_color="#FFF", text_color="black")
        tipo_menu.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(frame_principal, text="Prioridade", font=("Arial", 12), text_color="black", anchor="w").pack(fill="x", padx=20)
        prioridade_var = ctk.StringVar(value=tarefa["prioridade"])
        prioridade_menu = ctk.CTkComboBox(frame_principal, variable=prioridade_var, values=["Baixa", "Média", "Alta"], font=("Arial", 12), state="readonly", fg_color="#FFF", text_color="black")
        prioridade_menu.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(frame_principal, text="Descrição", font=("Arial", 12), text_color="black", anchor="w").pack(fill="x", padx=20)
        descricao_entry = ctk.CTkTextbox(frame_principal, font=("Arial", 12), height=60, fg_color="#FFF", text_color="black")
        descricao_entry.insert("1.0", tarefa["descricao"])
        descricao_entry.pack(fill="x", padx=20, pady=(0, 10))

        linha_inferior = ctk.CTkFrame(frame_principal, fg_color="#D6D6F5")
        linha_inferior.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(linha_inferior, text="Prazo", font=("Arial", 12), text_color="black", anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 10))
        prazo_entry = ctk.CTkEntry(linha_inferior, placeholder_text="dd/mm/yyyy", font=("Arial", 12), fg_color="#FFF", text_color="black")
        prazo_entry.insert(0, tarefa["prazo"])
        prazo_entry.grid(row=1, column=0, sticky="we")

        ctk.CTkLabel(linha_inferior, text="Status", font=("Arial", 12), text_color="black", anchor="w").grid(row=0, column=1, sticky="w", padx=(10, 0))
        status_var = ctk.StringVar(value="Em processo")
        status_menu = ctk.CTkComboBox(linha_inferior, variable=status_var, values=["Em processo", "Concluída", "Pendente"], font=("Arial", 12), fg_color="#FFF", text_color="black")
        status_menu.grid(row=1, column=1, sticky="we")

        # Mapear Enter para mover entre os campos na tela de edição
        nome_entry.bind("<Return>", lambda event: self.mover_proximo_campo(event, nome_entry, tipo_menu))
        tipo_menu.bind("<Return>", lambda event: self.mover_proximo_campo(event, tipo_menu, prazo_entry))
        prazo_entry.bind("<Return>", lambda event: self.validar_prazo(event, prazo_entry, prioridade_menu))
        prioridade_menu.bind("<Return>", lambda event: self.mover_proximo_campo(event, prioridade_menu, status_menu))
        status_menu.bind("<Return>", lambda event: self.mover_proximo_campo(event, status_menu, descricao_entry))
        descricao_entry.bind("<Return>", lambda event: self.salvar_edicao_tarefa(nome_entry.get(), tipo_var.get(), prazo_entry.get(), prioridade_var.get(), status_var.get(), descricao_entry.get("1.0", "end-1c")))


        btn_salvar = ctk.CTkButton(frame_principal, text="Salvar Tarefa", font=("Arial", 12), width=200, fg_color="#4A3CB1", hover_color="#3A2B8C", command=lambda: self.salvar_edicao_tarefa(nome_entry.get(), tipo_var.get(), prazo_entry.get(), prioridade_var.get(),status_var.get(), descricao_entry.get("1.0", "end-1c")))
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
     
     # Frame estilizado para a tela de redefinição de senha
     frame = ctk.CTkFrame(senha_popup, fg_color="#e0e5f5", corner_radius=15, border_color="#C9B6F2", border_width=2)
     frame.pack(fill="both", expand=True)

     ctk.CTkLabel(frame, text="Digite a senha para remover a tarefa:", font=("Arial", 14), text_color="#000000").pack(pady=10)

     senha_entry = ctk.CTkEntry(frame, show="*", font=("Arial", 12), fg_color="#e0e5f5", text_color="#000000")
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
     btn_confirmar = ctk.CTkButton(frame, text="Confirmar", font=("Arial", 12), text_color="#FFF",
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
     senha_popup.geometry("350x350")
     senha_popup.resizable(False, False)
 
     self.centralizar_janela_popover(senha_popup)
 
     # Frame estilizado para a tela de redefinição de senha
     frame = ctk.CTkFrame(senha_popup, fg_color="#e0e5f5", corner_radius=15, border_color="#C9B6F2", border_width=2)
     frame.pack(fill="both", expand=True)
 
     # Título da tela com ícone de alerta
     ctk.CTkLabel(frame, text="🔒 Autenticação de Senha", font=("Arial", 14, "bold"), text_color="#666666").pack(pady=(5, 0))
 
     # Texto de instrução
     ctk.CTkLabel(frame, text="Digite a senha para redefinir:", font=("Arial", 12), text_color="#666666").pack(pady=(5, 5))
 
     # Campo de entrada para a senha
     senha_entry = ctk.CTkEntry(frame, show="*", font=("Arial", 12), width=200)
     senha_entry.pack(pady=5)
     senha_entry.focus()  # Foco automático no campo de senha
 
     # Ao pressionar "Enter", verifica a senha
     senha_entry.bind("<Return>", lambda event: self.verificar_senha(senha_entry.get(), senha_popup, self.tela_redefinir_senha))
 
     # Botão Confirmar estilizado
     btn_confirmar = ctk.CTkButton(frame, text="Confirmar", font=("Arial", 14), 
                                 text_color="white", fg_color="#706FCF", hover_color="#5B5ABB",
                                 command=lambda: self.verificar_senha(senha_entry.get(), senha_popup, self.tela_redefinir_senha))
     btn_confirmar.pack(pady=5)

    def tela_redefinir_senha(self):
     for widget in self.root.winfo_children():
        widget.destroy()

     # Configuração da borda e título
     frame = ctk.CTkFrame(self.root, fg_color="#e0e5f5", corner_radius=15, border_color="#C9B6F2", border_width=2)
     frame.pack(fill="both", expand=True)

     self.adicionar_botao_voltar(self.tela_inicial)

     ctk.CTkLabel(frame, text="🔒 Redefinir senha", font=("Arial", 24, "bold"), text_color="#000000").pack(pady=(10, 70))

    # Campo da senha atual
     ctk.CTkLabel(frame, text="Senha atual:", font=("Arial", 12), text_color="#000000").pack(pady=(10, 5))
     senha_atual_entry = ctk.CTkEntry(frame, show="*", font=("Arial", 12), width=250, height=30 ,fg_color="#FFFFFF", text_color="#000000")
     senha_atual_entry.pack(pady=5)
     senha_atual_entry.focus()

    # Campo da nova senha
     ctk.CTkLabel(frame, text="Nova senha:", font=("Arial", 12), text_color="#000000").pack(pady=(10, 5))
     nova_senha_entry = ctk.CTkEntry(frame, show="*", font=("Arial", 12), width=250, height=30 , fg_color="#FFFFFF", text_color="#000000")
     nova_senha_entry.pack(pady=5)

    # Campo para confirmar a nova senha
     ctk.CTkLabel(frame, text="Confirmar nova senha:", font=("Arial", 12), text_color="#000000").pack(pady=(10, 5))
     confirmar_nova_senha_entry = ctk.CTkEntry(frame, show="*", font=("Arial", 12), width=250, height=30 , fg_color="#FFFFFF", text_color="#000000")
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
     btn_salvar_senha = ctk.CTkButton(frame, text="Redefinir Senha", font=("Arial", 12), width=300, height=40 ,text_color="white", fg_color="#706FCF", hover_color="#5B5ABB",
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