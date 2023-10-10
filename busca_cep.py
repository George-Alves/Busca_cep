import requests
import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('cep_database.db')
cur = conn.cursor()

def valida_cep(cep):
    if len(cep) == 8 and cep.isdigit():
        return True
    else:
        return False

def busca_cep_api(cep):
    if valida_cep(cep):
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'erro' not in data:
                return data
            else:
                raise Exception("CEP não encontrado na API.")
        else:
            raise Exception("Erro na solicitação para a API.")
    else:
        raise ValueError("CEP inválido. Por favor, digite um CEP válido.")

def busca_faixa_cep(uf):
    cur.execute('SELECT FaixaInicio, FaixaFim FROM CEP WHERE UF = ?', (uf,))
    faixas_cep = cur.fetchall()

    if faixas_cep:
        faixas = []
        for faixa_inicio, faixa_fim in faixas_cep:
            faixas.append((faixa_inicio, faixa_fim))
        return faixas
    else:
        raise Exception(f'Nenhuma informação encontrada para a UF {uf}')

def buscar():
    resultado_label.config(text="")
    cep_uf = entrada_cep.get().strip()

    try:
        if len(cep_uf) == 8 and valida_cep(cep_uf):
            resultado = busca_cep_api(cep_uf)
            resultado_label.config(text=f"CEP: {resultado['cep']}\n"
                                         f"Logradouro: {resultado['logradouro']}\n"
                                         f"Complemento: {resultado['complemento']}\n"
                                         f"Bairro: {resultado['bairro']}\n"
                                         f"Cidade: {resultado['localidade']}\n"
                                         f"Estado: {resultado['uf']}")
        elif len(cep_uf) == 2:  # Caso os dois primeiros dígitos sejam fornecidos para buscar a faixa de CEP
            uf = cep_uf.upper()
            faixas = busca_faixa_cep(uf)
            resultado_text = "Faixas de CEP para a UF {}:\n".format(uf)
            for faixa_inicio, faixa_fim in faixas:
                resultado_text += f'{faixa_inicio} - {faixa_fim}\n'
            resultado_label.config(text=resultado_text)
        else:
            raise ValueError("CEP inválido. Por favor, digite um CEP válido.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))


# Configuração da interface gráfica
root = tk.Tk()
root.title("Busca de CEP")

largura_fonte = 12
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

label = tk.Label(frame, text="Digite o CEP ou UF desejada:", font=("Arial", largura_fonte))
label.grid(row=0, column=0, sticky="w")

entrada_cep = tk.Entry(frame, font=("Arial", largura_fonte))
entrada_cep.grid(row=0, column=1)

buscar_button = tk.Button(frame, text="Buscar", command=buscar, font=("Arial", largura_fonte))
buscar_button.grid(row=0, column=2, padx=10)

resultado_label = tk.Label(frame, text="", font=("Arial", largura_fonte))
resultado_label.grid(row=1, column=0, columnspan=3, pady=10, sticky="w")

# Centraliza os resultados de pesquisa
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()

conn.close()
