import tkinter as tk  # Importa a biblioteca principal do Tkinter para a interface gráfica
from tkinter import ttk, messagebox  # Importa widgets modernos e caixas de alerta

# --- CONFIGURAÇÃO DA JANELA PRINCIPAL ---
janela = tk.Tk()  # Cria a janela principal do programa
janela.title("Conversor de Unidades - ISCAT")  # Define o título da janela
janela.geometry("400x600")  # Define a largura e altura da janela
janela.resizable(False, False)  # Bloqueia o redimensionamento da janela

# --- TÍTULO DA INTERFACE ---
titulo = tk.Label(janela, text="Conversor de Unidades", font=("Arial", 16, "bold"), pady=20)  # Cria o texto do título
titulo.pack()  # Adiciona o título à janela

# --- SEÇÃO DE CATEGORIA ---
moldura_cat = ttk.LabelFrame(janela, text=" Selecione a Categoria ", padding=10)  # Cria uma moldura para a categoria
moldura_cat.pack(padx=20, pady=10, fill="x")  # Posiciona a moldura na janela

categorias = ["Comprimento", "Massa", "Temperatura"]  # Lista de categorias disponíveis
var_categoria = tk.StringVar(value=categorias[0])  # Variável para armazenar a categoria escolhida
combo_categoria = ttk.Combobox(moldura_cat, textvariable=var_categoria, values=categorias, state="readonly")  # Cria a lista de categorias
combo_categoria.pack(fill="x")  # Adiciona a lista à moldura

# --- SEÇÃO DE CONVERSÃO ---
moldura_conv = ttk.LabelFrame(janela, text=" Dados da Conversão ", padding=10)  # Cria a moldura para os dados
moldura_conv.pack(padx=20, pady=10, fill="x")  # Posiciona a moldura

tk.Label(moldura_conv, text="Valor:").grid(row=0, column=0, sticky="w", pady=5)  # Rótulo para o campo de valor
campo_valor = ttk.Entry(moldura_conv)  # Cria a caixa de entrada para o número
campo_valor.grid(row=0, column=1, sticky="ew", pady=5)  # Posiciona a caixa de entrada

tk.Label(moldura_conv, text="De:").grid(row=1, column=0, sticky="w", pady=5)  # Rótulo para unidade de origem
var_origem = tk.StringVar()  # Variável para a unidade de origem
combo_origem = ttk.Combobox(moldura_conv, textvariable=var_origem, state="readonly")  # Lista de origem
combo_origem.grid(row=1, column=1, sticky="ew", pady=5)  # Posiciona a lista de origem

tk.Label(moldura_conv, text="Para:").grid(row=2, column=0, sticky="w", pady=5)  # Rótulo para unidade de destino
var_destino = tk.StringVar()  # Variável para a unidade de destino
combo_destino = ttk.Combobox(moldura_conv, textvariable=var_destino, state="readonly")  # Lista de destino
combo_destino.grid(row=2, column=1, sticky="ew", pady=5)  # Posiciona a lista de destino

# --- RÓTULO DE RESULTADO ---
rotulo_resultado = tk.Label(janela, text="Resultado: -", font=("Arial", 12, "bold"), fg="blue", pady=10)  # Cria o texto do resultado
rotulo_resultado.pack()  # Adiciona o resultado à janela

# --- LÓGICA DE ATUALIZAÇÃO DE UNIDADES  ---
# Esta parte define o que acontece quando a categoria muda
def atualizar_listas(event=None):  # Nota: O Tkinter exige uma função para eventos, mas a lógica interna é linear
    escolha = var_categoria.get()  # Verifica qual categoria foi selecionada
    if escolha == "Comprimento":  # Se for comprimento
        unidades = ["Quilômetro (km)", "Metro (m)", "Centímetro (cm)"]  # Define unidades de medida
    elif escolha == "Massa":  # Se for massa
        unidades = ["Quilograma (kg)", "Grama (g)"]  # Define unidades de peso
    else:  # Se for temperatura
        unidades = ["Celsius (°C)", "Fahrenheit (°F)"]  # Define unidades de calor
    combo_origem['values'] = unidades  # Atualiza a lista de origem
    combo_destino['values'] = unidades  # Atualiza a lista de destino
    combo_origem.current(0)  # Seleciona o primeiro item por padrão
    combo_destino.current(1)  # Seleciona o segundo item por padrão

combo_categoria.bind("<<ComboboxSelected>>", atualizar_listas)  # Liga a mudança de categoria à atualização
atualizar_listas()  # Executa uma vez no início para preencher as listas

# --- LÓGICA DE CONVERSÃO (EXECUTADA PELO BOTÃO) ---
def executar_conversao():  # Nota: O comando do botão exige uma função no Tkinter
    try:  # Inicia tratamento de erro para valores não numéricos
        v = float(campo_valor.get())  # Pega o valor digitado e converte para decimal
        cat = var_categoria.get()  # Pega a categoria atual
        orig = var_origem.get()  # Pega a unidade de origem
        dest = var_destino.get()  # Pega a unidade de destino
        res = 0.0  # Inicializa a variável de resultado

        if orig == dest:  # Se as unidades forem iguais
            res = v  # O resultado é o próprio valor
        elif cat == "Comprimento":  # Lógica para Comprimento
            if "km" in orig: m = v * 1000  # De km para metros
            elif "cm" in orig: m = v / 100  # De cm para metros
            else: m = v  # Já está em metros
            if "km" in dest: res = m / 1000  # De metros para km
            elif "cm" in dest: res = m * 100  # De metros para cm
            else: res = m  # Fica em metros
        elif cat == "Massa":  # Lógica para Massa
            if "kg" in orig: res = v * 1000  # De kg para g
            else: res = v / 1000  # De g para kg
        elif cat == "Temperatura":  # Lógica para Temperatura
            if "°C" in orig: res = (v * 9/5) + 32  # De Celsius para Fahrenheit
            else: res = (v - 32) * 5/9  # De Fahrenheit para Celsius
        
        rotulo_resultado.config(text=f"Resultado: {res:.2f}")  # Mostra o resultado na tela
    except ValueError:  # Se o utilizador não digitar um número
        messagebox.showerror("Erro", "Insira um número válido!")  # Mostra mensagem de erro

# --- BOTÃO CONVERTER ---
botao = ttk.Button(janela, text="CALCULAR CONVERSÃO", command=executar_conversao)  # Cria o botão de ação
botao.pack(pady=10)  # Adiciona o botão à janela

# --- RODAPÉ ---
tk.Label(janela, text="Félix D. Filipe D. Luciano C. - ISCAT", font=("Arial", 8, "italic")).pack(side="bottom", pady=10)  # Texto final

janela.mainloop()  # Mantém a janela aberta e funcionando
