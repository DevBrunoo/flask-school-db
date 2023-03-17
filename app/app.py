from flask import Flask, jsonify, request, render_template
import sqlite3
import os

app = Flask(__name__)

# Define o caminho do arquivo de banco de dados
DATABASE = os.path.join(os.getcwd(), "school.db")
DATABASE = 'school.db'

# Função para conectar ao banco de dados
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# Rota principal
@app.route('/')
def home():
    return render_template("homepage.html")

# Função para criar o banco de dados
def create_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('escola.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()

# Rota para criar o banco de dados
@app.route('/create_db', methods=['POST'])
def create_database():
    create_db()
    return jsonify({'message': 'Database created successfully!'})

# Rota para cadastrar uma nova turma
@app.route('/turmas', methods=['POST'])
def criar_turma():
    data = request.get_json()
    turma_nome = data['turma_nome']
    ano = data['ano']
    periodo = data['periodo']
    disciplinas = data['disciplinas']
    alunos = data['alunos']
    db = get_db()
    turma_id = db.execute('INSERT INTO turmas (turma_nome, ano, periodo) VALUES (?, ?, ?)',
                          (turma_nome, ano, periodo)).lastrowid
    for disciplina in disciplinas:
        db.execute('INSERT INTO turma_disciplinas (turma_id, disciplina_id) VALUES (?, ?)',
                   (turma_id, disciplina))
    for aluno in alunos:
        db.execute('INSERT INTO turma_alunos (turma_id, aluno_id) VALUES (?, ?)',
                   (turma_id, aluno))
    db.commit()
    db.close()
    return jsonify({'message': 'Turma criada com sucesso!'})

# Rota para cadastrar um novo aluno
@app.route('/alunos', methods=['POST'])
def criar_aluno():
    data = request.get_json()
    nome = data['nome']
    matricula = data.get('matricula')
    turma_id = data['turma_id']
    if not matricula:  # Verifica se matricula é None ou vazio
        return jsonify({'erro': 'O campo matricula é obrigatório'}), 400
    db = get_db()
    db.execute('INSERT INTO alunos (nome, matricula, turma_id) VALUES (?, ?, ?)',
               (nome, matricula, turma_id))
    db.commit()
    db.close()
    return jsonify({'message': 'Aluno criado com sucesso!'})

# Rota para cadastrar uma nova disciplina
@app.route('/disciplinas', methods=['POST'])
def criar_disciplina():
    data = request.get_json()
    nome = data['nome']
    db = get_db()
    db.execute('INSERT INTO disciplinas (nome) VALUES (?)',
               (nome,))
    db.commit()
    db.close()
    return jsonify({'message': 'Disciplina criada com sucesso!'})

# Rota para cadastrar um novo professor
@app.route('/professores', methods=['POST'])
def criar_professor():
    data = request.get_json()
    nome = data['nome']
    disciplinas = data['disciplinas']
    db = get_db()
   

    professor_id = db.execute('INSERT INTO professores (nome) VALUES (?)',
                              (nome,)).lastrowid
    for disciplina in disciplinas:
        db.execute('INSERT INTO professor_disciplinas (professor_id, disciplina_id) VALUES (?, ?)',
                   (professor_id, disciplina))
    db.commit()
    db.close()
    return jsonify({'message': 'Professor criado com sucesso!'})

# Rota para remover um aluno
@app.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def remover_aluno(aluno_id):
    db = get_db()
    db.execute('DELETE FROM turma_alunos WHERE aluno_id = ?', (aluno_id,))
    db.execute('DELETE FROM alunos WHERE id = ?', (aluno_id,))
    db.commit()
    db.close()
    return jsonify({'message': 'Aluno removido com sucesso!'})

# Rota para remover um professor
@app.route('/professores/<int:professor_id>', methods=['DELETE'])
def remover_professor(professor_id):
    db = get_db()
    db.execute('DELETE FROM professor_disciplinas WHERE professor_id = ?', (professor_id,))
    db.execute('DELETE FROM professores WHERE id = ?', (professor_id,))
    db.commit()
    db.close()
    return jsonify({'message': 'Professor removido com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)
