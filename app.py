#Aqui importamos as bibliotecas ou libs que irão ser usadas no projeto
#Antes do projeto podem ser instaladas na raiz do projeto usando o pip ou o terminal python
from datetime import datetime
from dateutil.relativedelta import relativedelta

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)

# Criar o banco de dados e a tabela
engine = create_engine('sqlite:///alunos.db', echo=True)
Base = declarative_base()

#Criar a classe aluno que será a base para toda a aplicação
class Aluno(Base):
    __tablename__ = 'alunos'

    cpf = Column(Integer, primary_key=True)
    nome = Column(String)
    data_nasc = Column(String)
    idade = Column(Integer)
    sexo = Column(String)
    av1 = Column(Integer)
    av2 = Column(Integer)
    media = Column(Integer)

#__repr()__ serve para representar um objeto como uma string. 
# Não precisa ser chamado diretamente. 
# Toda vez que o Python precisa resolver um objeto como string, __repr__() será chamado automaticamente.
# A vantagem é poder reescrevê-lo(string) como quiser
    def __repr__(self):
        return f'<Aluno {self.nome} - {self.data_nasc} - {self.idade}- {self.sexo} - {self.av1} - {self.av2} - {self.media}>'

# criar todos os dados
Base.metadata.create_all(engine)

# Criar a sessão do banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# Rota para mostrar todos os alunos e notas
@app.route('/')
def index():
    alunos = session.query(Aluno).all()
    return render_template('index.html', alunos=alunos)

# função para calcular a média
def calcular_media(av1,av2):
    media = str((float(av1)+float(av2))/2)
    return media

# Rota para adicionar um novo aluno e nota
@app.route('/add', methods=['GET', 'POST'])
def add():
    
    # Se o método for o post
    if request.method == 'POST':
        nome = request.form['nome']
        data_nasc = request.form['data_nasc']
        sexo = request.form['sexo']
        av1 = request.form['av1']
        av2 = request.form['av2']
        # Cálculo da idade com base no ano de 2023
        data_nasc_datetime = datetime.strptime(data_nasc, '%d/%m/%Y')        
        # instanciar aluno com dados vindos do post
        aluno = Aluno(nome=nome, data_nasc=data_nasc, idade = relativedelta(datetime(2023, 1, 1), data_nasc_datetime).years, sexo=sexo, av1=av1, av2=av2, media=calcular_media(av1,av2))
        session.add(aluno)
        session.commit()
        # retorna e redireciona para a index com os dados inseridos
        return redirect(url_for('index'))
    else:
        # caso não retorna para a página adicionar
        return render_template('add.html')

# Rota para editar um aluno e nota existente
# Get para pegar o dado e post para postar após a edição
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    aluno = session.query(Aluno).get(id)
    if request.method == 'POST':
        aluno.nome = request.form['nome']
        aluno.data_nasc = request.form['data_nasc']
        aluno.sexo = request.form['sexo']
        aluno.av1 = request.form['av1']
        aluno.av2 = request.form['av2']        
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('edit.html', aluno=aluno)

# Rota para deletar um aluno e nota existente
@app.route('/delete/<int:cpf>')
# Aqui foi usado o cpf pois é a chave primária
def delete(cpf):
    aluno = session.query(Aluno).get(cpf)
    session.delete(aluno)
    session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)