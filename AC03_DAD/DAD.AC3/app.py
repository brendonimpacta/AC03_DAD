from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aluno.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbimpacta:impacta#2020@dbimpacta.postgresql.dbaas.com.br/dbimpacta'
db = SQLAlchemy(app)

class Aluno(db.Model):
    __tablename__ = "tbAluno"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ra = db.Column(db.Integer, unique=True)
    nomeAluno = db.Column(db.String(50)) 
    emailAluno = db.Column(db.String(50))
    logradouro = db.Column(db.String(50))
    numero = db.Column(db.String(5))
    cep = db.Column(db.String(10))
    complemento = db.Column(db.String(20))

    def __init__(self, ra, nomeAluno, emailAluno, logradouro, numero, cep, complemento):
        self.ra = ra
        self.nomeAluno = nomeAluno
        self.emailAluno = emailAluno
        self.logradouro = logradouro
        self.numero = numero
        self.cep = cep
        self.complemento = complemento

#Routes
@app.route('/')
def index():
    alunos = Aluno.query.all()
    return render_template("index.html", alunos=alunos)

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        aluno = Aluno(request.form['ra'], request.form['nomeAluno'], request.form['emailAluno'], request.form['logradouro'], request.form['numero'], request.form['cep'], request.form['complemento'])
        db.session.add(aluno)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    aluno = Aluno.query.get(id)
    if request.method == "POST":
        aluno.nomeAluno = request.form['nomeAluno']
        aluno.emailAluno = request.form['emailAluno']
        aluno.logradouro = request.form['logradouro']
        aluno.numero = request.form['numero']
        aluno.cep = request.form['cep']
        aluno.complemento = request.form['complemento']

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', aluno=aluno)

@app.route('/delete/<int:id>')
def delete(id):
    aluno = Aluno.query.get(id)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
