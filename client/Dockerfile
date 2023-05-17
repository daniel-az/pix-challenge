# Imagem base do Python
FROM python:3.9

# Copiar os arquivos do código-fonte para o diretório de trabalho no contêiner
COPY . /app

# Definir o diretório de trabalho
WORKDIR /app

# Instalar as dependências
RUN pip install -r requirements.txt

# Comando para iniciar a aplicação quando o contêiner for executado
CMD ["python", "-u", "consumer.py"]
