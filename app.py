from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Criar o banco de dados e a tabela
engine = create_engine('sqlite:///alunos.db', echo=True)
Base = declarative_base()

class Aluno(Base):
    __tablename__ = 'alunos'

    cpf = Column(Integer, primary_key=True)
    nome = Column(String)
    data_nasc = Column(String)
    sexo = Column(String)
    av1 = Column(Integer)
    av2 = Column(Integer)
    media = Column(Integer)

    def __repr__(self):
        return f'<Aluno {self.nome} - {self.data_nasc} - {self.sexo} - {self.av1} - {self.av2} - {self.media}>'

Base.metadata.create_all(engine)

# Criar a sessão do banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# Rota para mostrar todos os alunos e notas
@app.route('/')
def index():
    alunos = session.query(Aluno).all()
    return render_template('index.html', alunos=alunos)

# Rota para adicionar um novo aluno e nota
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nome = request.form['nome']
        data_nasc = request.form['data_nasc']
        sexo = request.form['sexo']
        av1 = request.form['av1']
        av2 = request.form['av2']
        aluno = Aluno(nome=nome, data_nasc=data_nasc, sexo=sexo, av1=av1, av2=av2)
        session.add(aluno)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('add.html')

# Rota para editar um aluno e nota existente
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
def delete(cpf):
    aluno = session.query(Aluno).get(cpf)
    session.delete(aluno)
    session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)