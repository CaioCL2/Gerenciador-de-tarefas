import tkinter as tk
from tkinter import messagebox, ttk
import pickle
import re

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

        # Exibe a tela inicial
        self.tela_inicial()

    def centralizar_janela(self):
        # Centraliza a janela na tela 
        width = 900
        height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def salvar_tarefas(self):
        # Salva as tarefas no arquivo
        with open('tarefas.pkl', 'wb') as file:
            pickle.dump(self.tarefas, file)

    def carregar_tarefas(self):
        # Carrega as tarefas do arquivo
        try:
            with open('tarefas.pkl', 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return []

    def adicionar_botao_voltar(self, comando):
        # Adiciona um botão 'Voltar' no canto superior esquerdo
        btn_voltar = tk.Button(self.root, text="Voltar", font=("Arial", 12), command=comando)
        btn_voltar.place(x=10, y=10)

    def tela_inicial(self):
        # Exibe a tela inicial
        for widget in self.root.winfo_children():
            widget.destroy()

        # Reinicializa a seleção da tarefa ao voltar para a tela inicial
        self.tarefa_selecionada = None
        self.tarefa_selecionada_indice = None

        # Título
        label = tk.Label(self.root, text="SGT - Sistema de Gerenciamento de Tarefas", font=("Arial", 20))
        label.pack(pady=40)

        # Botões
        btn_add_tarefa = tk.Button(self.root, text="Cadastrar Tarefa", font=("Arial", 12), width=20, command=self.tela_adicionar_tarefa)
        btn_add_tarefa.pack(pady=10)

        btn_ver_tarefas = tk.Button(self.root, text="Ver Todas as Tarefas", font=("Arial", 12), width=20, command=self.tela_lista_tarefas)
        btn_ver_tarefas.pack(pady=10)

        btn_redefinir_senha = tk.Button(self.root, text="Redefinir Senha", font=("Arial", 12), width=20, command=self.tela_solicitar_senha_redefinir)
        btn_redefinir_senha.pack(pady=10)

    def tela_adicionar_tarefa(self):
        # Exibe a tela de adicionar tarefa
        for widget in self.root.winfo_children():
            widget.destroy()

        self.adicionar_botao_voltar(self.tela_inicial)

        tk.Label(self.root, text="Cadastrar Tarefa", font=("Arial", 16)).pack(pady=5)
        tk.Label(self.root, text="Nome da Tarefa", font=("Arial", 12)).pack(pady=5)
        nome_entry = tk.Entry(self.root, font=("Arial", 12))
        nome_entry.pack(pady=5)

        tk.Label(self.root, text="Tipo da Tarefa", font=("Arial", 12)).pack(pady=5)
        tipo_var = tk.StringVar()
        tipo_menu = ttk.Combobox(self.root, textvariable=tipo_var, values=["Pessoal", "Empresarial", "Acadêmico"], font=("Arial", 12), state="readonly")
        tipo_menu.pack(pady=5)

        tk.Label(self.root, text="Prazo (dd/mm/yyyy)", font=("Arial", 12)).pack(pady=5)
        prazo_entry = tk.Entry(self.root, font=("Arial", 12))
        prazo_entry.pack(pady=5)

        tk.Label(self.root, text="Prioridade", font=("Arial", 12)).pack(pady=5)
        prioridade_var = tk.StringVar()
        prioridade_menu = ttk.Combobox(self.root, textvariable=prioridade_var, values=["Baixa", "Média", "Alta"], font=("Arial", 12), state="readonly")
        prioridade_menu.pack(pady=5)

        tk.Label(self.root, text="Status", font=("Arial", 12)).pack(pady=5)
        status_var = tk.StringVar(value="Pendente")
        status_menu = ttk.Combobox(self.root, textvariable=status_var, values=["Pendente", "Concluída", "Parcialmente Concluída"], font=("Arial", 12), state="readonly")
        status_menu.pack(pady=5)

        tk.Label(self.root, text="Descrição", font=("Arial", 12)).pack(pady=5)
        descricao_entry = tk.Text(self.root, font=("Arial", 12), height=5, width=40)
        descricao_entry.pack(pady=5)

        btn_salvar = tk.Button(self.root, text="Salvar Tarefa", font=("Arial", 12), width=20,
                               command=lambda: self.salvar_tarefa(nome_entry.get(), tipo_var.get(), prazo_entry.get(), 
                                                                  prioridade_var.get(), status_var.get(), descricao_entry.get("1.0", "end-1c")))
        btn_salvar.pack(pady=20)

    def salvar_tarefa(self, nome, tipo, prazo, prioridade, status, descricao):
        # Salva a tarefa na lista e no arquivo 
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
        # Exibe a lista de tarefas
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

        # Preenche a lista com as tarefas
        for tarefa in self.tarefas:
            self.lista_tarefas.insert("", "end", values=(tarefa["nome"], tarefa["tipo"], tarefa["prazo"], tarefa["prioridade"], tarefa["status"]))

        # Restaura a seleção da tarefa se já tiver sido selecionada
        if self.tarefa_selecionada_indice is not None:
            self.lista_tarefas.selection_set(self.tarefa_selecionada_indice)

        # Botões de ações
        btn_ver_detalhes = tk.Button(self.root, text="Ver Detalhes da Tarefa", font=("Arial", 12), width=20, command=self.tela_detalhes_tarefa)
        btn_ver_detalhes.pack(pady=10)

        btn_marcar_concluida = tk.Button(self.root, text="Marcar como Concluída", font=("Arial", 12), width=20, command=self.marcar_concluida)
        btn_marcar_concluida.pack(pady=10)

        btn_editar_tarefa = tk.Button(self.root, text="Editar Tarefa", font=("Arial", 12), width=20, command=self.ver_descricao_tarefa)
        btn_editar_tarefa.pack(pady=10)

        btn_remover = tk.Button(self.root, text="Remover", font=("Arial", 12), width=20, command=self.tela_solicitar_senha_para_remover)
        btn_remover.pack(pady=10)

    def ver_descricao_tarefa(self):
        # Exibe a tela para editar a tarefa selecionada
        self.selecionar_tarefa()
        if self.tarefa_selecionada is None:
            messagebox.showerror("Erro", "Selecione uma tarefa para editar.")
            return
        self.tela_descricao_tarefa()

    def tela_detalhes_tarefa(self):
        # Exibe uma tela com o nome e a descrição da tarefa selecionada 
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
        # Exibe a tela para editar os detalhes da tarefa selecionada
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

        btn_salvar = tk.Button(self.root, text="Salvar Alterações", font=("Arial", 12), width=20,
                               command=lambda: self.salvar_edicao_tarefa(nome_entry.get(), tipo_var.get(), prazo_entry.get(), 
                                                                         prioridade_var.get(), status_var.get(), descricao_entry.get("1.0", "end-1c")))
        btn_salvar.pack(pady=20)

    def salvar_edicao_tarefa(self, nome, tipo, prazo, prioridade, status, descricao):
        # Salva as edições feitas na tarefa 
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
        # Seleciona uma tarefa na lista de tarefas 
        try:
            selected_item = self.lista_tarefas.selection()[0]
            self.tarefa_selecionada = self.lista_tarefas.index(selected_item)
            self.tarefa_selecionada_indice = selected_item  # Armazena o identificador da tarefa
        except IndexError:
            self.tarefa_selecionada = None
            self.tarefa_selecionada_indice = None

    def tela_solicitar_senha_para_remover(self):
        # Exibe uma tela para solicitar a senha antes de remover a tarefa
        senha_popup = tk.Toplevel(self.root)
        senha_popup.title("Autenticação de Senha")
        senha_popup.geometry("300x150")
        senha_popup.resizable(False, False)  # Impede o redimensionamento da janela

        # Centraliza a janela de senha
        self.centralizar_janela_popover(senha_popup)

        tk.Label(senha_popup, text="Digite a senha para remover a tarefa:", font=("Arial", 12)).pack(pady=10)
        senha_entry = tk.Entry(senha_popup, show="*", font=("Arial", 12))
        senha_entry.pack(pady=5, ipadx=10, ipady=2)

        btn_confirmar = tk.Button(senha_popup, text="Confirmar", font=("Arial", 12), command=lambda: self.verificar_senha(senha_entry.get(), senha_popup, self.remover_tarefa))
        btn_confirmar.pack(pady=10)

    def centralizar_janela_popover(self, popup):
        # Centraliza a janela pop-up na tela 
        popup_width = 300
        popup_height = 150
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    def verificar_senha(self, senha_digitada, popup, acao_sucesso):
        # Verifica se a senha digitada está correta e executa uma ação se estiver correta
        if senha_digitada == self.senha:
            popup.destroy()
            acao_sucesso()
        else:
            messagebox.showerror("Erro", "Senha incorreta!")

    def remover_tarefa(self):
        # Remove a tarefa selecionada
        self.selecionar_tarefa()
        if self.tarefa_selecionada is None:
            messagebox.showerror("Erro", "Selecione uma tarefa para remover.")
            return
        self.tarefas.pop(self.tarefa_selecionada)
        self.salvar_tarefas()
        messagebox.showinfo("Sucesso", "Tarefa removida com sucesso.")
        self.tela_lista_tarefas()

    def tela_solicitar_senha_redefinir(self):
        # Solicita a senha antes de redirecionar para a tela de redefinir senha
        senha_popup = tk.Toplevel(self.root)
        senha_popup.title("Autenticação de Senha")
        senha_popup.geometry("300x150")
        senha_popup.resizable(False, False)  # Impede o redimensionamento da janela

        # Centraliza a janela de redefinição
        self.centralizar_janela_popover(senha_popup)

        tk.Label(senha_popup, text="Digite a senha para redefinir:", font=("Arial", 12)).pack(pady=10)
        senha_entry = tk.Entry(senha_popup, show="*", font=("Arial", 12))
        senha_entry.pack(pady=5, ipadx=10, ipady=2)

        btn_confirmar = tk.Button(senha_popup, text="Confirmar", font=("Arial", 12), command=lambda: self.verificar_senha(senha_entry.get(), senha_popup, self.tela_redefinir_senha))
        btn_confirmar.pack(pady=10)

    def tela_redefinir_senha(self):
        # Exibe a tela de redefinição de senha
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

    def redefinir_senha(self, senha_atual, nova_senha, confirmar_nova_senha):
        # Redefine a senha se a senha atual estiver correta e as novas senhas coincidirem
        if senha_atual == self.senha:
            if nova_senha == confirmar_nova_senha and nova_senha.strip():
                self.senha = nova_senha
                messagebox.showinfo("Sucesso", "Senha redefinida com sucesso!")
                self.tela_inicial()
            else:
                messagebox.showerror("Erro", "As novas senhas não coincidem ou estão em branco!")
        else:
            messagebox.showerror("Erro", "Senha atual incorreta!")

    def marcar_concluida(self):
        # Alterna o status da tarefa entre 'Pendente', 'Parcialmente Concluída' e 'Concluída'
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
        messagebox.showinfo("Sucesso", f"Status alterado para {self.tarefas[self.tarefa_selecionada]['status']}.")
        self.tela_lista_tarefas()

    def selecionar_tarefa(self):
        # Seleciona uma tarefa na lista de tarefas 
        try:
            selected_item = self.lista_tarefas.selection()[0]
            self.tarefa_selecionada = self.lista_tarefas.index(selected_item)
            self.tarefa_selecionada_indice = selected_item  # Armazena o identificador da tarefa
        except IndexError:
            self.tarefa_selecionada = None
            self.tarefa_selecionada_indice = None

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaGerenciamentoTarefas(root)
    root.mainloop()
