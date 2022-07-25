from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema.sqlite3'

db = SQLAlchemy(app)


class Sistema(db.Model):
    cod = db.Column('cod', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    categoria = db.Column(db.String(150))
    quantidade = db.Column(db.Integer)

    def __init__(self, nome, categoria, quantidade):
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade


@app.route('/')
def index():
    sistema = Sistema.query.all()
    return render_template('index.html', sistema=sistema)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        sistema = Sistema(request.form['nome'], request.form['categoria'], request.form['quantidade'])
        db.session.add(sistema)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:cod>', methods=['GET', 'POST'])
def edit(cod):
    sistema = Sistema.query.get(cod)
    if request.method == 'POST':
        sistema.nome = request.form['nome']
        sistema.categoria = request.form['categoria']
        sistema.quantidade = request.form['quantidade']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', sistema=sistema)


@app.route('/delete/<int:cod>')
def delete(cod):
    sistema = Sistema.query.get(cod)
    db.session.delete(sistema)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)