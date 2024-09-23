FROM python:3.9-slim

WORKDIR /app

COPY .devcontainer/requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]