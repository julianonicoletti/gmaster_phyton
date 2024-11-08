from flask import Flask, request, jsonify
from flask_cors import CORS
from io import StringIO
import pandas as pd
import json
import numpy as np
from io import BytesIO, StringIO
from sqlalchemy import create_engine
import chardet

app = Flask(__name__)
CORS(app)

# configurações de conexão ao PostgreSQL
# ?? como obter essas informações no frontend ??????
DB_USER = "hanke_teste_user"
DB_PASSWORD = "oEGQTaisuqsyARbJ2kH1nY3Cnorjf5o8"
DB_HOST = "dpg-csllk423esus73b4vik0-a.oregon-postgres.render.com"
DB_PORT = "5432"  # porta padrão do PostgreSQL
DB_NAME = "hanke_teste"

# Função para conectar ao PostgreSQL
def get_db_connection():
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    return engine

@app.route('/')
def home():
    return "Servidor de upload está funcionando. Use a rota /upload para enviar arquivos."


# Rota para upload de arquivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    try:
        # Processa diferentes tipos de arquivos
        if file.filename.endswith('.xlsx'):
            print("Tentando ler o arquivo XLSX...")
            # Usamos BytesIO para ler o conteúdo binário do arquivo XLSX
            df = pd.read_excel(BytesIO(file.read()))
            for col in df.select_dtypes(include=['datetime']):
                df[col] = df[col].astype(str)
            data = df.to_dict(orient='records')
            print("Arquivo XLSX lido com sucesso.")

        elif file.filename.endswith('.json'):
            print("Tentando ler o arquivo JSON...")
            try:
                # Carregar o JSON diretamente
                data = json.load(file)
                
                # Verifica se os dados são uma lista de dicionários
                if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                    print("Arquivo JSON lido com sucesso.")
                    df = pd.DataFrame(data)
                else:
                    print("Estrutura de JSON inesperada. Esperado: lista de dicionários.")
                    return jsonify({"error": "Formato de JSON inválido. Esperado uma lista de objetos."}), 400

            except json.JSONDecodeError as e:
                print(f"Erro de decodificação JSON: {e}")
                return jsonify({"error": "Erro ao decodificar o arquivo JSON."}), 400

            except Exception as e:
                print(f"Erro ao processar o arquivo JSON: {e}")
                return jsonify({"error": f"Erro ao processar o arquivo JSON: {str(e)}"}), 500

        elif file.filename.endswith('.xml'):
            print("Tentando ler o arquivo XML...")
            import xml.etree.ElementTree as ET
            tree = ET.parse(file)
            root = tree.getroot()
            data = [{child.tag: child.text for child in elem} for elem in root]
            print("Arquivo XML lido com sucesso.")

        elif file.filename.endswith('.csv'):
            print("Tentando ler o arquivo CSV...")
            
             # Detecta automaticamente a codificação dos bytes do arquivo
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']  # Obtém a codificação detectada
            
            print(f'Codificação detectada: {encoding}')
            
            content = raw_data.decode(encoding, errors='replace')
            # Usamos StringIO para ler o conteúdo de texto do arquivo CSV
            df = pd.read_csv(StringIO(content), sep=';', on_bad_lines='skip', quotechar='"', skipinitialspace=True)
            df = df.where(pd.notnull(df), 'N/A')
            print(df.head())
            
            #retirar valores NaN ou null que impedem a conversão para JSON
            #df = df.applymap(lambda x: None if isinstance(x, float) and np.isnan(x) else x)
            
            
            data = df.to_dict(orient='records')  # Converte o DataFrame para uma lista de dicionários
            print("Arquivo CSV lido com sucesso.")

        else:
            print("Tipo de arquivo não suportado.")
            return jsonify({"error": "File type not supported"}), 400

        data = df.to_dict(orient='records')
        for item in data:
            for key, value in item.items():
                if isinstance(value, (int, float)):
                    item[key] = str(value)
                elif pd.isna(value):
                    item[key] = "N/A"
            return jsonify(data)

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return jsonify({"error": f"Failed to process the file: {str(e)}"}), 500


# Rota para carregamento do Banco de dados
@app.route('/load_from_db', methods=['POST'])
def load_from_db():
    try:
        table_name = request.args.get("table")  # Nome da tabela enviado como parâmetro
        if not table_name:
            return jsonify({"error": "Nome da tabela não fornecido"}), 400

        engine = get_db_connection()
        
        print("Dados do Banco de dados carregados com sucesso!")
        df = pd.read_sql_table(table_name, con=engine)
        
        df = df.map(lambda x: None if isinstance(x, float) and np.isnan(x) else x)
        
        data = df.to_dict(orient="records")
        return jsonify(data)
    
    except Exception as e:
        print(f"Erro ao carregar dados do banco de dados: {e}")
        return jsonify({"error": f"Erro ao carregar dados do banco de dados: {str(e)}"}), 500


# Rota para limpeza de dados
@app.route('/clean_data', methods=['POST'])
def clean_data():
    try:
        # Recebe os dados brutos enviados pelo frontend
        data = request.get_json()
        df = pd.DataFrame(data)

        # Funções de Limpeza de Dados
        df.replace(r'^\s*$', np.nan, regex=True, inplace=True)  # Substituir células em branco por NaN
        df.dropna(how='all', inplace=True)  # Remover linhas totalmente vazias
        df.fillna(method='ffill', inplace=True)  # Preencher NaN com o valor anterior (forward fill)

        # Converter colunas de data para string para evitar problemas com JSON
        for col in df.select_dtypes(include=['datetime']):
            df[col] = df[col].astype(str)
        
        print(df)    

        cleaned_data = df.to_dict(orient='records')
        return jsonify(cleaned_data)

    except Exception as e:
        print(f"Erro ao limpar os dados: {e}")
        return jsonify({"error": f"Erro ao limpar os dados: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
