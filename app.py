from flask import Flask, request
import os
import csv
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Caminho do arquivo CSV que armazenará os dados
CSV_FILE = 'dados_formulario.csv'

# Criar o CSV com cabeçalhos se não existir ainda
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Data_Hora', 'Nome', 'Sobrenome', 'Nascimento', 'Telefone', 'Motivo', 'Foto', 'Curriculo'])


@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/submit', methods=['POST'])
def submit():
    nome = request.form['nome']
    sobrenome = request.form['sobrenome']
    data_nascimento = request.form['data']
    telefone = request.form['telefone']
    motivo = request.form['motivo']

    foto = request.files['foto']
    curriculo = request.files['curriculo']

    # Criar nomes únicos para os arquivos enviados
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nome_base = f"{nome}_{sobrenome}_{timestamp}"

    foto_filename = f"{nome_base}_foto.jpg" if foto.filename else ''
    curriculo_filename = f"{nome_base}_curriculo.pdf" if curriculo.filename else ''

    # Salvar os arquivos
    if foto and foto.filename:
        foto.save(os.path.join(UPLOAD_FOLDER, foto_filename))

    if curriculo and curriculo.filename:
        curriculo.save(os.path.join(UPLOAD_FOLDER, curriculo_filename))

    # Salvar os dados no CSV
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            nome,
            sobrenome,
            data_nascimento,
            telefone,
            motivo,
            foto_filename,
            curriculo_filename
        ])

    return f"<h2>Obrigado, {nome}! Seus dados foram salvos com sucesso.</h2>"


if __name__ == '__main__':
    app.run(debug=True)