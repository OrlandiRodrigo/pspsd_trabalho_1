FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc libffi-dev

COPY modulo_b_frota/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install grpcio grpcio-tools

COPY contratos_grpc /app/contratos_grpc
COPY modulo_b_frota /app/

RUN python -m grpc_tools.protoc -I=contratos_grpc --python_out=. --grpc_python_out=. contratos_grpc/frota.proto

EXPOSE 50052
CMD ["python", "servidor_frota.py"]