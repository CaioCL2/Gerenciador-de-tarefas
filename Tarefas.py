#Projeto SGT (Sistema de Gerenciamento de Tarefas)

import tkinter as tk
from tkinter import messagebox, simpledialog

# Lista para armazenar tarefas e descrições
tarefas = []
descricoes = []

# Função para ir à tela de adicionar tarefa
def ir_para_adicionar_tarefa():
    primeira_tela.pack_forget()  # Esconde a tela inicial
    adicionar_tela.pack()  # Mostra a tela de adicionar tarefa

# Função para adicionar uma nova tarefa
def adicionar_tarefa():
    titulo = entrada_titulo.get()
    descricao = entrada_descricao.get("1.0", tk.END).strip()
    if titulo:
        tarefas.append(titulo)
        descricoes.append(descricao)
        entrada_titulo.delete(0, tk.END)
        entrada_descricao.delete("1.0", tk.END)
        messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso.")
    else:
        messagebox.showwarning("Aviso", "Você deve inserir um título para a tarefa.")

# Função para voltar para a tela inicial
def voltar_para_inicial():
    adicionar_tela.pack_forget()  # Esconde a tela de adicionar tarefa
    lista_tela.pack_forget()  # Esconde a tela de lista de tarefas
    descricao_tela.pack_forget()  # Esconde a tela de descrição da tarefa
    primeira_tela.pack()  # Mostra a tela inicial

# Função para ir à tela de lista de tarefas
def ir_para_lista_tarefas():
    primeira_tela.pack_forget()  # Esconde a tela inicial
    atualizar_lista_tarefas()  # Atualiza a lista de tarefas
    lista_tela.pack()  # Mostra a tela de lista de tarefas

# Função para atualizar a lista de tarefas
def atualizar_lista_tarefas():
    lista_tarefas.delete(0, tk.END)
    for tarefa in tarefas:
        lista_tarefas.insert(tk.END, tarefa)

# Função para ver e editar a descrição da tarefa selecionada
def ver_descricao():
    try:
        indice_selecionado = lista_tarefas.curselection()[0]
        tarefa = tarefas[indice_selecionado]
        descricao = descricoes[indice_selecionado]
        entrada_titulo_descricao.config(state='normal')
        entrada_descricao_tarefa.config(state='normal')
        entrada_titulo_descricao.delete(0, tk.END)
        entrada_titulo_descricao.insert(0, tarefa)
        entrada_descricao_tarefa.delete("1.0", tk.END)
        entrada_descricao_tarefa.insert("1.0", descricao)
        entrada_titulo_descricao.config(state='normal')
        entrada_descricao_tarefa.config(state='normal')
        lista_tela.pack_forget()  # Esconde a tela de lista de tarefas
        descricao_tela.pack()  # Mostra a tela de descrição da tarefa
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para ver a descrição.")

# Função para salvar as edições da tarefa
def salvar_edicoes():
    try:
        indice_selecionado = lista_tarefas.curselection()[0]
        novo_titulo = entrada_titulo_descricao.get()
        nova_descricao = entrada_descricao_tarefa.get("1.0", tk.END).strip()
        if novo_titulo:
            tarefas[indice_selecionado] = novo_titulo
            descricoes[indice_selecionado] = nova_descricao
            atualizar_lista_tarefas()  # Atualiza a lista após edição
            voltar_para_inicial()  # Volta para a tela inicial
        else:
            messagebox.showwarning("Aviso", "Você deve inserir um título para a tarefa.")
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para editar.")

# Função para remover a tarefa selecionada
def remover_tarefa():
    try:
        indice_selecionado = lista_tarefas.curselection()[0]
        del tarefas[indice_selecionado]
        del descricoes[indice_selecionado]
        atualizar_lista_tarefas()  # Atualiza a lista após remoção
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para remover.")

# Função para editar a tarefa selecionada
def editar_tarefa():
    try:
        indice_selecionado = lista_tarefas.curselection()[0]
        titulo_novo = simpledialog.askstring("Editar Tarefa", "Novo título da tarefa:")
        descricao_nova = simpledialog.askstring("Editar Descrição", "Nova descrição da tarefa:")
        if titulo_novo is not None:
            tarefas[indice_selecionado] = titulo_novo
            if descricao_nova is not None:
                descricoes[indice_selecionado] = descricao_nova
            atualizar_lista_tarefas()  # Atualiza a lista após edição
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para editar.")

# Inicializa a janela principal
janela = tk.Tk()
janela.title("Gerenciador de Tarefas")

# Configura a geometria da janela para abrir no centro da tela
largura_janela = 400
altura_janela = 400

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

pos_x = (largura_tela / 2) - (largura_janela / 2)
pos_y = (altura_tela / 2) - (altura_janela / 2)

janela.geometry(f"{largura_janela}x{altura_janela}+{int(pos_x)}+{int(pos_y)}")

# Função para criar o botão de voltar no canto superior esquerdo
def criar_botao_voltar(tela):
    voltar_btn = tk.Button(tela, text="Voltar", command=voltar_para_inicial, width=10)
    voltar_btn.pack(side=tk.TOP, anchor='nw', padx=5, pady=5)

# Tela 1: Tela Inicial
primeira_tela = tk.Frame(janela)

tk.Label(primeira_tela, text="Gerenciador de Tarefas", font=("Arial", 16)).pack(pady=10)

tk.Button(primeira_tela, text="Adicionar Tarefa", command=ir_para_adicionar_tarefa).pack(pady=5)
tk.Button(primeira_tela, text="Ver Todas as Tarefas", command=ir_para_lista_tarefas).pack(pady=5)

primeira_tela.pack()

# Tela 2: Adicionar Tarefa
adicionar_tela = tk.Frame(janela)
criar_botao_voltar(adicionar_tela)

tk.Label(adicionar_tela, text="Adicionar Nova Tarefa", font=("Arial", 16)).pack(pady=10)

tk.Label(adicionar_tela, text="Título:").pack()
entrada_titulo = tk.Entry(adicionar_tela, width=40)
entrada_titulo.pack(pady=5)

tk.Label(adicionar_tela, text="Descrição:").pack()
entrada_descricao = tk.Text(adicionar_tela, height=4, width=40)
entrada_descricao.pack(pady=5)

tk.Button(adicionar_tela, text="Adicionar Tarefa", command=adicionar_tarefa).pack(pady=10)

# Tela 3: Lista de Tarefas
lista_tela = tk.Frame(janela)
criar_botao_voltar(lista_tela)

tk.Label(lista_tela, text="Lista de Tarefas", font=("Arial", 16)).pack(pady=10)

lista_tarefas = tk.Listbox(lista_tela, selectmode=tk.SINGLE, width=50, height=10)
lista_tarefas.pack(pady=10)

tk.Button(lista_tela, text="Ver Descrição", command=ver_descricao).pack(pady=5)
tk.Button(lista_tela, text="Remover Tarefa", command=remover_tarefa).pack(pady=5)
tk.Button(lista_tela, text="Editar Tarefa", command=editar_tarefa).pack(pady=5)

# Tela 4: Descrição da Tarefa
descricao_tela = tk.Frame(janela)
criar_botao_voltar(descricao_tela)

tk.Label(descricao_tela, text="Descrição da Tarefa", font=("Arial", 16)).pack(pady=10)

tk.Label(descricao_tela, text="Título:").pack()
entrada_titulo_descricao = tk.Entry(descricao_tela, width=40)
entrada_titulo_descricao.pack(pady=5)
entrada_titulo_descricao.config(state='normal')

tk.Label(descricao_tela, text="Descrição:").pack()
entrada_descricao_tarefa = tk.Text(descricao_tela, height=4, width=40)
entrada_descricao_tarefa.pack(pady=5)
entrada_descricao_tarefa.config(state='normal')

tk.Button(descricao_tela, text="Salvar Alterações", command=salvar_edicoes).pack(pady=10)

# Inicializa a interface gráfica
janela.mainloop()
