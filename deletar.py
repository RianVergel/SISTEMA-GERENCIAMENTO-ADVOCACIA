import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

def listar_clientes():
    try:
        conn = psycopg2.connect(dbname="advocacia", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        cur.execute("SELECT id_cliente, nome FROM public.clientes")
        clientes = cur.fetchall()
        return clientes
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return []
    finally:
        cur.close()
        conn.close()

def listar_processos(id_cliente):
    try:
        conn = psycopg2.connect(dbname="advocacia", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        cur.execute("SELECT id_processo, numero_processo FROM public.processos WHERE id_cliente = %s", (id_cliente,))
        processos = cur.fetchall()
        return processos
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return []
    finally:
        cur.close()
        conn.close()

def deletar_cliente(id_cliente):
    try:
        conn = psycopg2.connect(dbname="advocacia", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        cur.execute("DELETE FROM public.processos WHERE id_cliente = %s", (id_cliente,))
        cur.execute("DELETE FROM public.clientes WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
        messagebox.showinfo("Info", "Cliente e processos deletados com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        cur.close()
        conn.close()

def deletar_processo(id_processo):
    try:
        conn = psycopg2.connect(dbname="advocacia", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        cur.execute("DELETE FROM public.processos WHERE id_processo = %s", (id_processo,))
        conn.commit()
        messagebox.showinfo("Info", "Processo deletado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        cur.close()
        conn.close()

def tela_deletar():
    deletar = tk.Toplevel()
    deletar.title("Deletar Cliente e Processo")
    deletar.geometry("400x400")

    # Deletar Cliente
    label_cliente = tk.Label(deletar, text="Selecione o Cliente para Deletar:", font=("Arial", 12))
    label_cliente.pack(pady=10)

    clientes = listar_clientes()
    combo_cliente = ttk.Combobox(deletar, values=[cliente[1] for cliente in clientes])
    combo_cliente.pack(pady=10)

    def confirmar_delecao_cliente():
        nome_cliente = combo_cliente.get()
        id_cliente = next((cliente[0] for cliente in clientes if cliente[1] == nome_cliente), None)

        if id_cliente:
            resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar o cliente e seus processos?")
            if resposta:
                deletar_cliente(id_cliente)
                combo_processo.set('')  # Limpa a seleção de processos
                atualizar_processos()  # Atualiza a lista de processos
        else:
            messagebox.showwarning("Aviso", "Selecione um cliente válido.")

    btn_deletar_cliente = tk.Button(deletar, text="Deletar Cliente", command=confirmar_delecao_cliente, bg="red", fg="white")
    btn_deletar_cliente.pack(pady=20)

    # Deletar Processo
    label_processo = tk.Label(deletar, text="Selecione o Processo para Deletar:", font=("Arial", 12))
    label_processo.pack(pady=10)

    combo_processo = ttk.Combobox(deletar)
    combo_processo.pack(pady=10)

    def atualizar_processos(event=None):
        nome_cliente = combo_cliente.get()
        id_cliente = next((cliente[0] for cliente in clientes if cliente[1] == nome_cliente), None)

        if id_cliente:
            processos = listar_processos(id_cliente)
            combo_processo['values'] = [f"{processo[1]} (ID: {processo[0]})" for processo in processos]
            combo_processo.set('')  # Limpa a seleção anterior

    combo_cliente.bind("<<ComboboxSelected>>", atualizar_processos)

    def confirmar_delecao_processo():
        processo_info = combo_processo.get()
        if processo_info:
            id_processo = processo_info.split(" (ID: ")[-1][:-1]  # Extrai o ID do processo

            resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar o processo?")
            if resposta:
                deletar_processo(id_processo)
                combo_processo.set('')  # Limpa a seleção após deleção
        else:
            messagebox.showwarning("Aviso", "Selecione um processo válido.")

    btn_deletar_processo = tk.Button(deletar, text="Deletar Processo", command=confirmar_delecao_processo, bg="red", fg="white")
    btn_deletar_processo.pack(pady=20)

    deletar.mainloop()
