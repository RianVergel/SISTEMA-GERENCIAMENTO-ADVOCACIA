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

def buscar_cliente(id_cliente):
    try:
        conn = psycopg2.connect(dbname="advocacia", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        cur.execute("SELECT nome, telefone FROM public.clientes WHERE id_cliente = %s", (id_cliente,))
        cliente = cur.fetchone()
        return cliente
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return None
    finally:
        cur.close()
        conn.close()

def salvar_cliente(id_cliente, nome, telefone):
    try:
        conn = psycopg2.connect(dbname="advocacia", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        cur.execute("UPDATE public.clientes SET nome = %s, telefone = %s WHERE id_cliente = %s", 
                    (nome, telefone, id_cliente))
        conn.commit()
        messagebox.showinfo("Info", "Cliente atualizado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        cur.close()
        conn.close()

def buscar_processo(id_cliente):
    try:
        conn = psycopg2.connect(dbname="advocacia", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        cur.execute("SELECT id_processo, numero_processo, tipo_processo, status FROM public.processos WHERE id_cliente = %s", (id_cliente,))
        processo = cur.fetchone()
        return processo
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return None
    finally:
        cur.close()
        conn.close()

def salvar_processo(id_processo, numero_processo, tipo_processo, status):
    try:
        conn = psycopg2.connect(dbname="advocacia", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        cur.execute("UPDATE public.processos SET numero_processo = %s, tipo_processo = %s, status = %s WHERE id_processo = %s", 
                    (numero_processo, tipo_processo, status, id_processo))
        conn.commit()
        messagebox.showinfo("Info", "Processo atualizado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        cur.close()
        conn.close()

def tela_editar():
    editar = tk.Toplevel()
    editar.title("Editar Cliente e Processo")
    editar.geometry("400x600")
    
    label_cliente = tk.Label(editar, text="Selecione o Cliente:", font=("Arial", 12))
    label_cliente.pack(pady=5)

    clientes = listar_clientes()
    combo_cliente = ttk.Combobox(editar, values=[cliente[1] for cliente in clientes])
    combo_cliente.pack(pady=5)

    #AUTO-COMPLETAR
    def preencher_dados(event):
        nome_cliente = combo_cliente.get()
        id_cliente = next(cliente[0] for cliente in clientes if cliente[1] == nome_cliente)

        cliente_info = buscar_cliente(id_cliente)
        if cliente_info:
            input_nome.delete(0, tk.END)
            input_nome.insert(0, cliente_info[0])

            input_telefone.delete(0, tk.END)
            input_telefone.insert(0, cliente_info[1])

        processo_info = buscar_processo(id_cliente)
        if processo_info:
            input_numero_processo.delete(0, tk.END)
            input_numero_processo.insert(0, processo_info[1])

            input_tipo.delete(0, tk.END)
            input_tipo.insert(0, processo_info[2])

            var_status.set(processo_info[3])

    combo_cliente.bind("<<ComboboxSelected>>", preencher_dados)

    #CLIENTE
    frame_cliente = tk.LabelFrame(editar, text="Editar Cliente", padx=10, pady=10)
    frame_cliente.pack(padx=10, pady=10, fill="both")

    label_nome = tk.Label(frame_cliente, text="Nome:", font=("Arial", 12))
    label_nome.pack(pady=5)
    input_nome = tk.Entry(frame_cliente)
    input_nome.pack(pady=5)

    label_telefone = tk.Label(frame_cliente, text="Telefone:", font=("Arial", 12))
    label_telefone.pack(pady=5)
    input_telefone = tk.Entry(frame_cliente)
    input_telefone.pack(pady=5)

    #PROCESSO
    frame_processo = tk.LabelFrame(editar, text="Editar Processo", padx=10, pady=10)
    frame_processo.pack(padx=10, pady=10, fill="both")

    label_numero_processo = tk.Label(frame_processo, text="Número do Processo:", font=("Arial", 12))
    label_numero_processo.pack(pady=5)
    input_numero_processo = tk.Entry(frame_processo)
    input_numero_processo.pack(pady=5)

    label_tipo = tk.Label(frame_processo, text="Tipo:", font=("Arial", 12))
    label_tipo.pack(pady=5)
    input_tipo = tk.Entry(frame_processo)
    input_tipo.pack(pady=5)

    label_status = tk.Label(frame_processo, text="Status:", font=("Arial", 12))
    label_status.pack(pady=5)

    var_status = tk.StringVar()
    checkbox_concluido = tk.Radiobutton(frame_processo, text="Concluído", variable=var_status, value="Concluído")
    checkbox_andamento = tk.Radiobutton(frame_processo, text="Em Andamento", variable=var_status, value="Em Andamento")
    checkbox_concluido.pack(pady=5)
    checkbox_andamento.pack(pady=5)

    btn_salvar = tk.Button(editar, text="Salvar Alterações", command=lambda: salvar_edicoes())
    btn_salvar.pack(pady=20)

    def salvar_edicoes():
        nome_cliente = combo_cliente.get()
        id_cliente = next(cliente[0] for cliente in clientes if cliente[1] == nome_cliente)

        salvar_cliente(id_cliente, input_nome.get(), input_telefone.get())

        processo_info = buscar_processo(id_cliente)
        if processo_info:
            id_processo = processo_info[0]
            salvar_processo(id_processo, input_numero_processo.get(), input_tipo.get(), var_status.get())

    editar.mainloop()

