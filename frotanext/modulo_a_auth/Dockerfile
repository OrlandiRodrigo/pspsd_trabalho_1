FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc libffi-dev

COPY modulo_a_auth/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install grpcio grpcio-tools

COPY contratos_grpc /app/contratos_grpc
COPY modulo_a_auth /app/

RUN python -m grpc_tools.protoc -I=contratos_grpc --python_out=. --grpc_python_out=. contratos_grpc/autenticacao.proto

EXPOSE 50051
CMD ["python", "servidor_autenticacao.py"]