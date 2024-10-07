import tkinter as tk
from tkinter import messagebox

from cadastar import tela_cadastrar
from consultar import tela_consultar
from editar import tela_editar
from deletar import tela_deletar

def abrir_cadastrar():
    tela_cadastrar()

def abrir_consultar():
    tela_consultar()

def abrir_atualizar():
    tela_editar()

def abrir_deletar():
    tela_deletar()

def tela_principal():
    root = tk.Tk()
    root.title("Sistema de Gestão de Advocacia")
    root.geometry("300x300")

    title_label = tk.Label(root, text="Selecione uma Opção", font=("Arial", 16))
    title_label.pack(pady=20)

    btn_cadastrar = tk.Button(root, text="Cadastrar", command=abrir_cadastrar, width=20)
    btn_cadastrar.pack(pady=5)

    btn_consultar = tk.Button(root, text="Consultar", command=abrir_consultar, width=20)
    btn_consultar.pack(pady=5)

    btn_atualizar = tk.Button(root, text="Atualizar", command=abrir_atualizar, width=20)
    btn_atualizar.pack(pady=5)

    btn_deletar = tk.Button(root, text="Deletar", command=abrir_deletar, width=20)
    btn_deletar.pack(pady=5)

    root.mainloop()

tela_principal()
