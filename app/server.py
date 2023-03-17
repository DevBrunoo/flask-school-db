import requests

# URL base da sua aplicação Flask
base_url = 'http://localhost:5000'

# Teste de cadastro de uma nova turma
turma = {'nome': 'Turma 1', 'alunos': ['Alice', 'Bob'], 'disciplinas': ['Matemática', 'História']}
response = requests.post(f'{base_url}/turmas', json=turma)
print(response.json())

# Teste de cadastro de um novo professor
professor = {'nome': 'Prof. João', 'disciplinas': ['Matemática', 'Física']}
response = requests.post(f'{base_url}/professores', json=professor)
print(response.json())

# Teste de remoção de um aluno
response = requests.delete(f'{base_url}/alunos/Alice')
print(response.json())

# Teste de remoção de um professor
response = requests.delete(f'{base_url}/professores/Prof. João')
print(response.json())
