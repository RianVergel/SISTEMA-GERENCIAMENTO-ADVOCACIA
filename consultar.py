import tkinter as tk
from tkinter import ttk
import psycopg2

def tela_consultar():
    consultar = tk.Toplevel()
    consultar.title("Consultar Clientes e Processos")
    consultar.geometry("1200x600")

    #CLIENTES
    frame_clientes = tk.LabelFrame(consultar, text="Clientes", padx=10, pady=10)
    frame_clientes.pack(padx=10, pady=10, fill="both")

    tree_clientes = ttk.Treeview(frame_clientes, columns=("ID", "Nome", "Telefone"), show='headings')
    tree_clientes.heading("ID", text="ID")
    tree_clientes.heading("Nome", text="Nome")
    tree_clientes.heading("Telefone", text="Telefone")
    tree_clientes.pack(fill="both")

    #PREENCHER TABELA CLIENTES
    for cliente in listar_clientes():
        tree_clientes.insert("", tk.END, values=cliente)

    #PROCESSOS
    frame_processos = tk.LabelFrame(consultar, text="Processos", padx=10, pady=10)
    frame_processos.pack(padx=10, pady=10, fill="both")

    tree_processos = ttk.Treeview(frame_processos, columns=("ID", "Número do Processo", "Tipo", "Status", "Cliente"), show='headings')
    tree_processos.heading("ID", text="ID")
    tree_processos.heading("Número do Processo", text="Número do Processo")
    tree_processos.heading("Tipo", text="Tipo")
    tree_processos.heading("Status", text="Status")
    tree_processos.heading("Cliente", text="Cliente")
    tree_processos.pack(fill="both")

    #PREENCHER TABELA PROCESSOS
    for processo in listar_processos():
        tree_processos.insert("", tk.END, values=processo)

def listar_clientes():
    try:
        conn = psycopg2.connect(dbname="advocacia", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        cur.execute("SELECT id_cliente, nome, telefone FROM public.clientes")
        return cur.fetchall()
    except Exception as e:
        return []
    finally:
        cur.close()
        conn.close()

def listar_processos():
    try:
        conn = psycopg2.connect(dbname="advocacia", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id_processo, p.numero_processo, p.tipo_processo, p.status, c.nome
            FROM public.processos p
            JOIN public.clientes c ON p.id_cliente = c.id_cliente
        """)
        return cur.fetchall()
    except Exception as e:
        print("deu ruim")
        return []
    finally:
        cur.close()
        conn.close()
