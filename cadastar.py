import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2

def tela_cadastrar():
    cadastrar = tk.Toplevel()
    cadastrar.title("Cadastrar Cliente e Processo")
    cadastrar.geometry("400x700")

    #CLIENTE
    frame_cliente = tk.LabelFrame(cadastrar, text="Cadastro de Cliente", padx=10, pady=10)
    frame_cliente.pack(padx=10, pady=10, fill="both")

    label_nome = tk.Label(frame_cliente, text="Nome:", font=("Arial", 12))
    label_nome.pack(pady=5)
    input_nome = tk.Entry(frame_cliente)
    input_nome.pack(pady=5)

    label_telefone = tk.Label(frame_cliente, text="Telefone:", font=("Arial", 12))
    label_telefone.pack(pady=5)
    input_telefone = tk.Entry(frame_cliente)
    input_telefone.pack(pady=5)

    btn_salvar_cliente = tk.Button(frame_cliente, text="Salvar Cliente", command=lambda: salvar_cliente(
        input_nome.get(), input_telefone.get()
    ))
    btn_salvar_cliente.pack(pady=20)

    #PROCESSO
    frame_processo = tk.LabelFrame(cadastrar, text="Cadastro de Processo", padx=10, pady=10)
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

    status_var = tk.IntVar()

    checkbox_concluido = tk.Radiobutton(frame_processo, text="Concluído", variable=status_var, value=1)
    checkbox_concluido.pack(pady=5)

    checkbox_andamento = tk.Radiobutton(frame_processo, text="Em Andamento", variable=status_var, value=0)
    checkbox_andamento.pack(pady=5)

    label_cliente = tk.Label(frame_processo, text="Selecione o Cliente:", font=("Arial", 12))
    label_cliente.pack(pady=5)
    
    combo_cliente = ttk.Combobox(frame_processo)
    combo_cliente.pack(pady=5)
    combo_cliente['values'] = listar_clientes()  #PREENCHER COMBOBOX

    btn_salvar_processo = tk.Button(frame_processo, text="Salvar Processo", command=lambda: salvar_processo(
        input_numero_processo.get(), 
        input_tipo.get(), 
        "Concluído" if status_var.get() == 1 else "Em Andamento",
        combo_cliente.get()
    ))
    btn_salvar_processo.pack(pady=20)

def listar_clientes():
    try:
        conn = psycopg2.connect(dbname="advocacia", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        cur.execute("SELECT nome FROM public.clientes")
        clientes = cur.fetchall()
        return [cliente[0] for cliente in clientes]
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return []
    finally:
        cur.close()
        conn.close()

def salvar_cliente(nome, telefone):
    try:
        conn = psycopg2.connect(dbname="advocacia", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        
        cur.execute("INSERT INTO public.clientes (nome, telefone) VALUES (%s, %s)", 
                    (nome, telefone))
        conn.commit()
        messagebox.showinfo("Info", f"Cliente {nome} cadastrado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        cur.close()
        conn.close()

def salvar_processo(numero_processo, tipo_processo, status, nome_cliente):
    try:
        conn = psycopg2.connect(dbname="advocacia", user="postgres", password="admin", host="localhost")
        cur = conn.cursor()
        
        cur.execute("SELECT id_cliente FROM public.clientes WHERE nome = %s", (nome_cliente,))
        id_cliente = cur.fetchone()
        
        if id_cliente:
            cur.execute("INSERT INTO public.processos (numero_processo, tipo_processo, status, id_cliente) VALUES (%s, %s, %s, %s)", 
                        (numero_processo, tipo_processo, status, id_cliente[0]))
            conn.commit()
            messagebox.showinfo("Info", f"Processo {numero_processo} cadastrado com sucesso!")
        else:
            messagebox.showerror("Erro", "Cliente não encontrado!")

    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        cur.close()
        conn.close()
