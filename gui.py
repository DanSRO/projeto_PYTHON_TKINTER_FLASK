import tkinter as tk
import requests
import webbrowser

# Criar a janela principal
window = tk.Tk()
window.title('CRUD de Alunos e Notas')
window.geometry('400x300')

# Criar uma função para abrir o navegador com a aplicação web do Flask
def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

# Criar uma função para adicionar um novo aluno e nota usando o Flask
def add_aluno():
    nome = entry_nome.get()
    data_nasc = entry_data_nasc.get()
    sexo = entry_sexo.get()
    av1 = entry_av1.get()
    av2 = entry_av2.get()
    data = {'nome': nome, 'data_nasc': data_nasc, 'sexo': sexo, 'av1': av1, 'av2': av2}
    response = requests.post('http://127.0.0.1:5000/add', data=data)
    if response.status_code == 200:
        label_resultado['text'] = 'Aluno adicionado com sucesso!'
    else:
        label_resultado['text'] = 'Erro ao adicionar aluno!'

# Criar os widgets da interface gráfica
label_titulo = tk.Label(window, text='CRUD de Alunos e Notas', font=('Arial', 20))
label_nome = tk.Label(window, text='Nome:')
entry_nome = tk.Entry(window)

label_data_nasc = tk.Label(window, text='Data de Nascimento:')
entry_data_nasc = tk.Entry(window)

label_sexo = tk.Label(window, text='Sexo:')
entry_sexo = tk.Entry(window)

label_av1 = tk.Label(window, text='Av1:')
entry_av1 = tk.Entry(window)

label_av2 = tk.Label(window, text='Av2:')
entry_av2 = tk.Entry(window)

label_media = tk.Label(window, text='Média:')
entry_media = tk.Entry(window)

button_add = tk.Button(window, text='Adicionar', command=add_aluno)
button_web = tk.Button(window, text='Abrir no Navegador', command=open_browser)
label_resultado = tk.Label(window)

# Posicionar os widgets na janela usando o gerenciador de geometria grid
label_titulo.grid(row=0, column=0, columnspan=2, pady=10)
label_nome.grid(row=1, column=0, sticky='e')
entry_nome.grid(row=1, column=1)

label_data_nasc.grid(row=2, column=0, sticky='e')
entry_data_nasc.grid(row=2, column=1)

label_sexo.grid(row=3, column=0, sticky='e')
entry_sexo.grid(row=3, column=1)

label_av1.grid(row=4, column=0, sticky='e')
entry_av1.grid(row=4, column=1)

label_av2.grid(row=5, column=0, sticky='e')
entry_av2.grid(row=5, column=1)

label_media.grid(row=6, column=0, sticky='e')
entry_media.grid(row=6, column=1)

button_add.grid(row=7, column=0, pady=10)
button_web.grid(row=7, column=1)
label_resultado.grid(row=8, column=0, columnspan=2)

# Iniciar o loop principal da interface gráfica
window.mainloop()